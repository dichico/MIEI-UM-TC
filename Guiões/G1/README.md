# Guião 1 - Ambiente de Desenvolvimento
**Criptografia de um Ficheiro**

O Fernet é um método de criptografia simétrica que se certifica de que uma mensagem codificada não possa ser manipulada ou lida sem a sua devida chave.

O objetivo deste guião prático é essencialmente compreender como funciona este mecanismo de cifra autenticada e como assegura a *confidencialidade* e *integridade* dos dados armazenados num ficheiro.

--- 

## Resolução do Guião

**Para começar a resolução do trabalho proposto, o grupo desenvolveu um ficheiro de texto com a mensagem a cifrar, seguindo o seguinte pensamento:**

1. Criação de uma chave ```Fernet``` codificada que é depois guardada num ficheiro.

Esta chave ```Fernet``` deve ser mantida em segredo, dado que é através dela que o texto é cifrado e posteriormente decifrado. 

2. Abertura/*Parse* do texto a ser cifrado. A este texto é aplicada a criptografia em si, que resulta num *token* ```Fernet```. A informação cifrada é escrita num outro ficheiro.

Este *token* ```Fernet``` possui garantias de *privacidade* e *autenticidade*.

3. Estanto o texto cifrado, abre-se o ficheiro desse mesmo assim como o ficheiro da chave ```Fernet```. Com estas duas informações, faz-se o oposto, decifrando-se e obtendo-se assim o texto original. 

---

## Dificuldades do Guião
 
Este método ```Fernet``` tornou-se simples de utilizar, dado que já faz todo o trabalho difícil no processo de criptografia de um ficheiro. Apenas foi preciso conhecer o propósito de cada método usado, os seus parâmetros e ainda os seus valores de retorno. 