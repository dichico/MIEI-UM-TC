# Guião 8 -  Manipulação de Certificados X509

Este Guião serve de preparação para o [Guião 9](https://github.com/uminho-miei-crypto/1920-G9/tree/master/Guiões/G9), tendo em conta que a ideia passa por estudar a forma de manipular certificados em *Pyhton*, chegando-se à fase final de validação. 

**Para isso, são fornecidos três ficheiros:**

1. Uma *keystore* PKCS12 que contém o Certificado (juntamente com a Chave Privada) para o Servidor;
2. Uma *keystore* PKCS12 que contém o Certificado (juntamente com a Chave Privada) para o Cliente;
3. O Certificado (formato DER) da CA utilizada neste Guião.

Com estes ficheiros, usaram-se os três sub-comandos mencionados, na tentativa de entender como poderia ser feito o processo de manipulação de cada um dos Certificados e de que modo a informação poderia ser extraída e convertida num ficheiro legível para futura validação.

---

## Resolução do Guião

Invocando o openSSL conseguimos depois trabalhar com os seus sub-comandos. Para isso apenas é necessário escrever ```openssl```no terminal, ficando ele pronto para interpretar todos os sub-comandos que do openSSL fazem parte.

- ### **Comando x509**

1. **Revelação da informação do Certificado como *ouput* no terminal**

```python
OpenSSL> x509 -in CA.cer -inform DER
```

Ao adicionarmos ```-email``` no fim, conseguimos ainda obter a informação acerca do email da pessoa responsável pelo mesmo.

```python
OpenSSL> x509 -in CA.cer -inform DER -email
```

2. **Extração da informacão em modo PEM** - Criação de um novo Ficheiro

Outra coisa que pode ser feita é a transformação da CA para o modo PEM, o que torna o ficheiro de *output* gerado perfeitamente legível, facilitando a extração/leitura do Certificado nele contido.

***Esta conversão é importante, dado que estamos a trabalhar com openSSL e ele usa PEM por omissão.***

```python
OpenSSL> x509 -inform DER -outform PEM -in CA.cer -out sslCACert.pem
```

- ### **Comando pkcs12**

1. **Revelação da informação do Certificado como *ouput* no terminal**

Este primeiro comando possibilita a visualização em modo terminal de toda a informação contida nos ficheiros em formato **.p12**. Neste caso, visualiza-se o Certificado, bem como informações extra acerca do email, tipo de encriptação e ainda outros atributos como o *localKeyID*.

Se formos mais além na introdução da *passphrase*, conseguimos também visualizar a Chave Privada Encriptada da entidade em causa.

```python
OpenSSL> pkcs12 -in Servidor.p12 -info
```

2. **Extração da informacão em modo PEM** - Criação de um novo Ficheiro

Tal como acontece na parte da CA, pode na mesma ser extraída toda a informação que é mostrada pelo *output* do terminal, ou seja, os Certificados do Cliente e Servidor, bem como as suas Chaves Privada.

A ideia passa também por guardar tudo isto em modo PEM para que se consiga prosseguir para o passo final da verificação/validação.

```python
OpenSSL> pkcs12 -in Cliente1.p12 -clcerts -out sslCAServidorCert.pem
OpenSSL> pkcs12 -in Servidor.p12 -clcerts -out sslCAClienteCert.pem
```

- ### **Comando verify**

Este sub-comando foi o mais difícil de entender, dado que existem um conjunto de regras/promenores que fazem a diferença na altura de se verificar/validar os certificados em si.

> *The Common Name value used for the server and client certificates/keys must each differ from the Common Name value used for the CA certificate. Otherwise, the certificate and key files will not work for servers compiled using OpenSSL.*

Isto implica que os nomes dados aos ficheiros no formato **.pem** gerados anteriormente tenham um nome diferente do que é considerado o *Common Name value*.

**Dessa forma, foram dedicado os seguintes nomes:**

1. **Certificado CA**: sslCACert.pem
2. **Certificado Servidor**: sslCAServidorCert.pem
3. **Certificado Cliente**: sslCAClienteCert.pem

Estando estes ficheiros criados, pode-se executar o comando de verificação e perceber que o Certificado do Cliente e Servidor foram assinados pelo Certificado principal CA.

```python
OpenSSL> verify -CAfile sslCACert.pem sslCAServidoCert.pem sslCAClienteCert.pem
```

---

## Observações Finais

O comando ```verify``` foi o mais difícil de entender, tendo em conta que era necessário atentar em alguns detalhes. 

Os outros dois foram relativamente simples pela simples recorrência ao "manual"  existente para cada um deles. 