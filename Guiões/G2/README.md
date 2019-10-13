# Guião 2 - Protecção de Segredos Criptográficos

Como visto no guião anterior, o ```Fernet``` garante a *confidencialidade* e *integridade* da informação. Com o objetivo de criar todo um processo de criptografia de um ficheiro, armazenávamos a chave ```Fernet``` num ficheiro à parte, aplicando depois essa mesma chave ao texto já cifrado.
Com isto, ficou explícito o dual uso da chave, tanto para cifrar como para decifrar a informação.

O inconveniente de todo este processo é estarmos a guardar a chave num ficheiro totalmente desprotegido, pondo assim em causa a segurança dos segredos criptográficos.

**O objetivo desde guião passa por aplicar duas formas diferentes de proteger os segredos criptográficos, criando assim duas novas estratégias na criptografia da informação:**

1. [pdkdf2.py](pdkdf2.py) refere-se à utilização do método *Password Based Key Derivation Functions (PBKDF)*.
2. [scrypt.py](scrypt.py) refere-se à utilização do método *Scrypt*.

--- 

## Resolução do Guião

**No que toca à utilização do méotodo *PBKDF*, a ideia passa por gerar uma espécie de segredo criptográfico através de uma *password* que é solicitada ao utilizador. Com isto, conseguimos garantir que a *password* não é diretamente utilizada como chave criptográfica como acontecia com a chave ```Fernet```:**

1. Criação de um *Salt* aleatório - valor seguro com 16 bits, que é depois guardado num ficheiro.
2. 

---

## Dificuldades do Guião
 
