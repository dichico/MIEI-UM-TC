# Guião 9 -  Finalização do protocolo *StS* usando certificados

O protocolo *Station-to-Station* consiste numa espécie de "contrato" em termos de chave criptográfica. Baseia-se no protocolo *Diffie-Hellman*, adicionando segurança em termos de ataques intermediários.

Através do uso de **certificados X509**, espera-se assim alterar a metodologia das assinaturas no protocolo do [Guião 7](https://github.com/uminho-miei-crypto/1920-G9/tree/master/Gui%C3%B5es/G7) anterior, permitindo que as mensagens enviadas pelo canal público sejam agora encriptadas e também assinadas com os certificados do Cliente e Servidor respetivamente, além da sua verificação sobre o *Certificate Authority* (CA).

---

## Resolução do Guião

De modo a simplificar o funcionamento do programa, foi desenvolvida um ficheiro adicional em Python [**OpenSSLWorker.py**](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G9/OpenSSLWorker.py), contendo todos os métodos que tratam de todo o requisito adicional pretendido para este Guião. 

Nesse ficheiro adicional temos o *import* da biblioteca Python usada adicionalmente, chamada de [PyOpenSSL](https://www.pyopenssl.org/en/stable/) que nos forneceu alguns métodos fundamentais para a manipulação e leitura dos ficheiros dos certificados fornecidos pelo professor.

Antes de começar a programar a melhor maneira para implementar o enunciado, utilizou-se a ferramenta *OpenSSL* na linha de comandos para converter o CA fornecido em `DER` (formato binário para guardar certificados e/ou chaves) para o formato usado mais recentemente ``PEM`.

```bash
> openssl x509 -inform DER -outform PEM -in CA.cer -out CAPEM.cer
```

No ficheiro [**OpenSSLWorker.py**](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G9/OpenSSLWorker.py) temos a inicialização da leitura dos ficheiros fornecidos, ou seja a CA.pem (agora em formato `PEM`) e os certificados `Cliente1.p12` e `Servidor.p12` utilizando da biblioteca [PyOpenSSL](https://www.pyopenssl.org/en/stable/) os métodos `crypto.load_certificate()` e `load_pkcs12()`.

```python
# Abertura dos vários ficheiros e transformação para instâncias do PyOpenSSL
with open('Certificados/CA.pem', 'r') as ca_file:
    ca_pem = ca_file.read()
ca = crypto.load_certificate(crypto.FILETYPE_PEM, ca_pem)

# Abertura do PKCS12 com o certificado e chave privada do cliente.
with open('Certificados/Cliente1.p12', 'rb') as client_file:
    clientPKCS12 = client_file.read()
p12Client = crypto.load_pkcs12(clientPKCS12, bytes('1234', 'utf-8'))
```
Com os objetos agora em Python podemos obter os seus certificados e chaves privadas inseridas nas *keystores* PKCS12.

No caso do *Certificate Authority* (CA) foi colocado num objeto `X509`

---

## Observações Finais
 ...