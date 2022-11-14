package main

import (
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"log"
	"os"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/golang-jwt/jwt/v4"
	"github.com/kelseyhightower/envconfig"
)

const QoS = 1

var onPublish mqtt.MessageHandler = func(c mqtt.Client, msg mqtt.Message) {
	log.Printf("Published message: %s on topic %s", msg.Payload(), msg.Topic())
}

var onMessage mqtt.MessageHandler = func(c mqtt.Client, msg mqtt.Message) {
	log.Printf("Received message: %s on topic %s", msg.Payload(), msg.Topic())
}

var onConnect mqtt.OnConnectHandler = func(c mqtt.Client) {
	log.Printf("onConnect")
}

var onConnectionLost mqtt.ConnectionLostHandler = func(c mqtt.Client, err error) {
	log.Printf("onConnectionLost: %v", err)
}

func newTLSConfig(cfg *config) *tls.Config {
	certPool := x509.NewCertPool()

	ca, err := os.ReadFile(cfg.CAFile)
	if err != nil {
		log.Fatalf("ioutil.ReadFile: %v", err)
	}

	certPool.AppendCertsFromPEM(ca)

	return &tls.Config{
		RootCAs:    certPool,
		MinVersion: tls.VersionTLS12,
		MaxVersion: tls.VersionTLS12,
	}
}

func newJWT(cfg *config) string {
	claims := jwt.RegisteredClaims{
		ExpiresAt: jwt.NewNumericDate(time.Now().Add(24 * time.Hour)),
		IssuedAt:  jwt.NewNumericDate(time.Now()),
		Audience:  []string{cfg.ProjectID},
	}
	log.Printf("JWT claims: %+v", claims)

	token := jwt.NewWithClaims(jwt.SigningMethodRS256, claims)

	ss, err := token.SignedString(cfg.ClientPrivateKey())
	if err != nil {
		log.Fatalf("token.SignedString: %v", err)
	}

	return ss
}

func newClient(cfg *config) mqtt.Client {
	opts := mqtt.NewClientOptions()
	opts.AddBroker(cfg.Broker())
	opts.SetTLSConfig(newTLSConfig(cfg))
	opts.SetClientID(cfg.ClientID())
	opts.SetUsername("unused")
	opts.SetPassword(newJWT(cfg))
	opts.SetProtocolVersion(4)
	opts.SetDefaultPublishHandler(onPublish)
	opts.OnConnect = onConnect
	opts.OnConnectionLost = onConnectionLost

	log.Printf("options: %+v", opts)

	return mqtt.NewClient(opts)
}

func main() {
	cfg := getConfig()
	log.Printf("config: %+v", cfg)

	client := newClient(cfg)

	if token := client.Connect(); token.Wait() && token.Error() != nil {
		log.Fatalf("client.Connect: %v", token.Error())
	}

	token := client.Subscribe(cfg.Topic(), QoS, onMessage)
	token.Wait()
	log.Printf("Subscribed to topic %s", cfg.Topic())

	for i := 0; ; i++ {
		msg := fmt.Sprintf("Message %d", i)
		token := client.Publish(cfg.Topic(), QoS, false, msg)
		token.Wait()
		time.Sleep(time.Second)
	}
}

type config struct {
	Host                 string `default:"mqtt.2030.ltsapis.goog"`
	Port                 int    `default:"8883"`
	ProjectID            string `required:"true" split_words:"true"`
	Region               string `required:"true"`
	RegistryID           string `required:"true" split_words:"true"`
	DeviceID             string `required:"true" split_words:"true"`
	ClientPrivateKeyFile string `required:"true" split_words:"true"`
	CAFile               string `required:"true" split_words:"true"`
}

func getConfig() *config {
	c := &config{}

	if err := envconfig.Process("", c); err != nil {
		log.Fatalf("envconfig.Process: %v", err)
	}

	return c
}

func (cfg *config) Broker() string {
	return fmt.Sprintf("ssl://%s:%d", cfg.Host, cfg.Port)
}

func (cfg *config) ClientID() string {
	return fmt.Sprintf("projects/%s/locations/%s/registries/%s/devices/%s",
		cfg.ProjectID, cfg.Region, cfg.RegistryID, cfg.DeviceID,
	)
}

func (cfg *config) Topic() string {
	return fmt.Sprintf("/devices/%s/events", cfg.DeviceID)
}

func (cfg *config) ClientPrivateKey() *rsa.PrivateKey {
	pemBytes, err := os.ReadFile(cfg.ClientPrivateKeyFile)
	if err != nil {
		log.Fatalf("os.ReadFile: %v", err)
	}

	block, _ := pem.Decode(pemBytes)

	keyIf, err := x509.ParsePKCS8PrivateKey(block.Bytes)
	if err != nil {
		log.Fatalf("x509.ParsePKCS8PrivateKey: %v", err)
	}

	key, ok := keyIf.(*rsa.PrivateKey)
	if !ok {
		log.Fatalf("Invalid RSA key")
	}

	return key
}
