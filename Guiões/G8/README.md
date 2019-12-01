# Guião 8 -  Manipulação de Certificados X509

Este Guião serve de preparação para o Guião 9, dado que a ideia passa por estudar toda a forma de manipular certificados em *Pyhton*, chegando à fase final de validação. 

**Para isso, são fornecidos três ficheiros:**

1. Uma *keystore* PKCS12 que contém o Certificado (juntamente com a chave privada) para o Servidor;
2. Uma *keystore* PKCS12 que contém o Certificado (juntamente com a chave privada) para o Cliente;
3. O Certificado (formato DER) da CA utilizada neste Guião.

Com estes ficheiros, foi-se recorrendo aos três sub-comandos mencionados, na tentativa de entender como poderia ser feito o processo de manipulação de cada um dos Certificados e de que modo a informação poderia ser extraída consoante a necessidade futura na nossa aplicação Cliente e Servidor.

---

## Resolução do Guião

Invocando o openSSL em si conseguimos depois trabalhar com os seus sub-comandos. 

```python
> openssl
```

1. **Comando x509**

Através do comando abaixo conseguimos obter o *output* no terminal daquilo que é o Certificado da CA em si. 

```python
OpenSSL> x509 -in CA.cer -inform DER
```

Ao adicionarmos ```-email``` no fim, conseguimos ainda obter a informação acerca do email da pessoa responsável pelo mesmo.

```python
OpenSSL> x509 -in CA.cer -inform DER -email
```

Outra coisa que pode ser feita é a transformação da CA para o modo PEM, o que torna o ficheiro de *output* gerado perfeitamente legível, facilitando a extração/leitura do Certificado nele contido.

```python
OpenSSL> x509 -inform DER -outform PEM -in CA.cer -out CAPEM.cer
```

**Esta conversão é importante, dado que estamos a trabalhar com openSSL e ele usa PEM por omissão.**



2. **Comando pkcs12**

Este primeiro comando possibilita a visualização em modo terminal de toda a informação contida nos ficheiros em formato **.p12**. Assim, visualiza-se o Certificado, bem como informações extra acerca do email, tipo de encriptação e ainda outros atributos como o *localKeyID*.

Além do Certificado, se formos mais além na introdução da *passphrase*, conseguimos também visualizar a Chave Privada Encriptada da entidade em causa.

```python
OpenSSL> pkcs12 -in Servidor.p12 -info
```

Tal como acontece na parte da CA, pode na mesma ser extraída toda a informação que é mostrada pelo *output* do terminal, ou seja, os Certificados do Cliente e Servidor, bem como as suas Chaves Privada.

A ideia passa também por guardar tudo isto em modo PEM. Assim, podemos verificar se esses Certificados foram assinados pela principal CA.cer.

```python
OpenSSL> openssl pkcs12 -in Cliente1.p12 -clcerts -out clienteInfo.txt
OpenSSL> openssl pkcs12 -in Servidor.p12 -clcerts -out servidorInfo.txt
```

---

## Observações Finais


