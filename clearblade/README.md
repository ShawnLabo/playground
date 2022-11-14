ClearBlade IoT Core
===================

## Create key pairs

[Creating key pairs - ClearBlade IoT Core - Confluence](https://clearblade.atlassian.net/wiki/spaces/IC/pages/2202763333/Creating+key+pairs)

```sh
openssl genpkey -algorithm RSA -out rsa_private.pem \
  -pkeyopt rsa_keygen_bits:2048
openssl rsa -in rsa_private.pem -pubout \
  -out rsa_public.pem
openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout rsa_private.pem \
  -out rsa_cert.pem -subj "/CN=unused"
```

* `rsa_private.pem` デバイスで保持する
* `rsa_public.pem` ClearBlade IoT CoreのデバイスのPublic Keyとしてアップロードする
