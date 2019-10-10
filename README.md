# Tecnologia Criptográfica
Repositório criado para a Unidade Curricular Tecnologia Criptográfica, do perfil **Criptografia e Segurança da Informação**, que irá conter as resoluções de todos os trabalhos práticos propostos assim como uma breve descrição das decisões tomadas e possíveis dificuldades encontradas no decorrer de cada um dos guiões.

---

## **Composição do Grupo**
* Diogo Araújo, A78485 - [dichico](https://github.com/dichico)
* Diogo Nogueira, A78957 - [diogoesnog](https://github.com/diogoesnog)

---

## **Lista dos Guiões**

- **Guião 1** [O Ambiente de Desenvolvimento](https://github.com/uminho-miei-crypto/1920-G9/tree/master/Gui%C3%B5es/G1)   
  - Preparação do repositório da Unidade Curricular no ```Github```.
  - Instalação da biblioteca de suporte ```cryptography``` para se usar ao longo dos guiões.
  - Proposta de exercício para se criar uma **cifra autenticada de um ficheiro** através da ```Fernet```.

- **TCP 2** [Protecção de Segredos Criptográficos](https://github.com/uminho-miei-crypto/1920-G9/tree/master/Gui%C3%B5es/G2)
  - Discussão da necessidade de evitar armazenar segredos criptográficos em ficheiros sem qualquer tipo de proteção.
  - **Estudo de duas estratégias para evitar utilização de ficheiros desprotegidos:**
    - Evitar o armazenamento da chave - *Password Based Key Derivation Functions (PBKDF)*;
    - Armazenar o ficheiro de forma protegida - *KeyStore*.