# DOCUMENTAR DEPOIS
> openssl pkcs12 -in Servidor.p12 -info
> openssl x509 -in CA.cer -inform DER (adicionar -email no fim também)
> openssl x509 -inform DER -outform PEM -in CA.cer -out CAPEM.cer