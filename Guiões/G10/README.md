ainda me falta algumas coisas

## Criação de CA Root e certificados personalizados usando OpenSSL
```
openssl genrsa -out chaveCA.key -aes256 -passout pass:DiCert

openssl req -new -x509 -key chaveCA.key -out CA.pem

openssl genrsa -aes256 -passout pass:Server -out chaveServer.key

openssl genrsa -aes256 -passout pass:Server -out chaveCliente.key

openssl req -new -key chaveServer.key -out Server.csr 

openssl req -new -key chaveCliente.key -out Cliente.csr

openssl x509 -req -in Server.csr -CA CA.pem -CAkey chaveCA.key -out Server.pem -CAcreateserial

openssl x509 -req -in Cliente.csr -CA DiCert.pem -CAkey chaveCA.key -out Cliente.pem -CAcreateserial
```

## Criação da PKCS12 do Cliente e Servidor com a sua chave privada e certificado
```
openssl pkcs12 -export -out Cliente.p12 -inkey chaveCliente.key -in Cliente.pem

openssl pkcs12 -export -out Server.p12 -inkey chaveServer.key -in Server.pem
```