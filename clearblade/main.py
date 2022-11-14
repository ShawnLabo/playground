import datetime
import os
import ssl

from paho.mqtt import client as mqtt
import jwt


HOST = "mqtt.2030.ltsapis.goog"
# HOST = "us-central1-mqtt.clearblade.com"
PORT = 8883
USERNAME = "unused"
CIPHER = "ECDHE-ECDSA-AES128-GCM-SHA256"
JWT_ALGORITHM = "RS256"


# https://clearblade.atlassian.net/wiki/spaces/IC/pages/2202206402/Using+JSON+Web+Tokens
# https://pyjwt.readthedocs.io/en/latest/usage.html#encoding-decoding-tokens-with-rs256-rsa
# https://pyjwt.readthedocs.io/en/latest/api.html
def make_jwt(project_id: str, private_key: str) -> str:
    claims = {
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
        "aud": project_id,
    }
    print(f"{claims=}")

    return jwt.encode(claims, private_key, algorithm=JWT_ALGORITHM)


# https://clearblade.atlassian.net/wiki/spaces/IC/pages/2202566686/Publishing+over+MQTT#Configuring-MQTT-clients
def make_client_id(project_id: str,
                   region: str,
                   registry_id: str,
                   device_id: str) -> str:

    return f"projects/{project_id}/locations/{region}/registries/{registry_id}/devices/{device_id}"


# https://clearblade.atlassian.net/wiki/spaces/IC/pages/2202566686/Publishing+over+MQTT#Publishing-telemetry-events
def make_topic_name(device_id: str) -> str:
    return f"/devices/{device_id}/events"


def on_connect(client, userdata, flags, rc):
    print(f"on_connect: {mqtt.connack_string(rc)}")


def on_disconnect(client, userdata, rc):
    print(f"on_disconnect: {mqtt.error_string(rc)} ({rc})")


def on_publish(client, userdata, mid):
    print(f"on_publish: {mid}")


def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    print(f"on_message: Received message '{payload}' on topic '{message.topic}'")


def main(project_id: str,
         region: str,
         registry_id: str,
         device_id: str,
         client_private_key_file: str,
         ca_file: str) -> None:

    with open(client_private_key_file, "r") as f:
        private_key = f.read()

    jwt = make_jwt(project_id=project_id, private_key=private_key)
    print(f"{jwt=}")

    client_id = make_client_id(project_id=project_id,
                               region=region,
                               registry_id=registry_id,
                               device_id=device_id)
    print(f"{client_id=}")

    topic = make_topic_name(device_id=device_id)
    print(f"{topic=}")

    # https://github.com/eclipse/paho.mqtt.python#constructor--reinitialise
    client = mqtt.Client(client_id)

    # https://clearblade.atlassian.net/wiki/spaces/IC/pages/2202566686/Publishing+over+MQTT#Using-a-long-term-MQTT-domain
    # https://github.com/eclipse/paho.mqtt.python#tls_set
    # https://docs.python.org/ja/3/library/ssl.html#ssl.SSLContext.set_ciphers
    # client.tls_set(ca_certs=ca_file,
    #                certfile=client_cert_file,
    #                keyfile=client_private_key_file,
    #                tls_version=ssl.PROTOCOL_TLSv1_2,
    #                ciphers=CIPHER)
    client.tls_set(ca_certs=ca_file,
                   tls_version=ssl.PROTOCOL_TLSv1_2)

    client.username_pw_set(USERNAME, jwt)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_message = on_message

    print("Connecting...")

    # https://github.com/eclipse/paho.mqtt.python#connect--reconnect--disconnect
    client.connect(HOST, PORT)

    client.subscribe(topic)

    # https://github.com/eclipse/paho.mqtt.python#publishing
    payload = "Hello"
    client.publish(topic=topic, payload=payload)

    print(f"Published message: {payload=}")

    client.loop_forever()


if __name__ == "__main__":
    main(
        project_id=os.environ["PROJECT_ID"],
        region=os.environ["REGION"],
        registry_id=os.environ["REGISTRY_ID"],
        device_id=os.environ["DEVICE_ID"],
        client_private_key_file=os.environ["CLIENT_PRIVATE_KEY_FILE"],
        ca_file=os.environ["CA_FILE"],
    )
