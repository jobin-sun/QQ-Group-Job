openssl req -x509 -new -out certfile.crt -keyout keyfile.key -days 365
# avoid to enter pem password, strip the password
openssl rsa -in keyfile.key -out keyfile.key
