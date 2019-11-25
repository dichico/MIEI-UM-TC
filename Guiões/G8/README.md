# DOCUMENTAR DEPOIS
> openssl x509 -in CA.cer -inform DER (adicionar -email no fim também)

Passar o CA para PEM dado que estmaos a trabalhar com openssl e ele usa PEM por omissão.
> openssl x509 -inform DER -outform PEM -in CA.cer -out CAPEM.cer

> openssl pkcs12 -in Servidor.p12 -info

Buscar os certificados do Cliente e Servidor e gravar em PEM.
Para depois verificarmos se esse ceritficado ficou assinado pelo principal CA.cer.
> openssl pkcs12 -in Cliente1.p12 -clcerts -out clienteInfo.txt
> openssl pkcs12 -in Servidor.p12 -clcerts -out servidorInfo.txt

> openssl verify
