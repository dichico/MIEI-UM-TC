# Guião 2 - Protecção de Segredos Criptográficos

Como visto no guião anterior, o ```Fernet``` garante a *confidencialidade* e *integridade* da informação. Com o objetivo de criar todo um processo de criptografia de um ficheiro, armazenávamos a chave ```Fernet``` num ficheiro à parte, aplicando depois essa mesma chave ao texto já cifrado.
Com isto, ficou explícito o dual uso da chave, tanto para cifrar como para decifrar a informação.

O inconveniente de todo este processo é estarmos a guardar a chave num ficheiro totalmente desprotegido, pondo assim em causa a segurança dos segredos criptográficos.

**O objetivo desde guião passa por aplicar duas formas diferentes de proteger os segredos criptográficos, criando assim duas novas estratégias na criptografia da informação:**

1. [pdkdf2.py](pdkdf2.py) refere-se à utilização do método *Password Based Key Derivation Functions (PBKDF)*.
2. [scrypt.py](scrypt.py) refere-se à utilização do método *Scrypt*.

--- 

## Resolução do Guião

**No que toca à utilização do método *PBKDF*, a ideia passa por gerar uma espécie de segredo criptográfico através de uma *password* que é solicitada ao utilizador. Com isto, conseguimos garantir que a *password* não é diretamente utilizada como chave criptográfica tal como acontecia com a chave ```Fernet``` do Guião 1.**

**Assim, para o *PBKDF*, seguiram-se os seguintes passos:**

1. Criação de um *Salt* aleatório - valor seguro com 16 bits, que é guardado num ficheiro. O *Salt* é depois usado como entrada adicional na função *PBKDF2HMAC*.
2. Desenvolvimento da classe *PBKDF2HMAC* em si, com definição das características necessárias - como o número de iterações, algortimo e salt.
3. Solicitação da *passphrase* ao utilizador.
4. Aplicação da *passphrase* ao algoritmo criado anteriormente. 

Nesta fase, o *PBKDF2* aplica uma função à *password* do utilizador, juntamente com o valor do *Salt* inicial, repetindo o processo tantas vezes quanto o número de iterações definido.

Como resultado desta aplicação será produzida uma chave derivada que irá ser udada como chave criptográfica no restante do processo.

5. Tendo a chave criptográfica, o processo é agora o mesmo que o do Guião 1. A única diferença é que não estamos a usar/armazenar a chave original, mas sim uma chave derivada.


---

---

## Dificuldades do Guião
 
