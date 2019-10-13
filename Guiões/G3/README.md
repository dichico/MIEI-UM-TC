# Guião 3 - Implementação de Cifra Autenticada

Até então, temos utilizado a cifra autenticada ```Fernet```, que por si só, acaba por fazer grande parte do trabalho no que toca à criptografia de uma dada informação. Com a realização deste Guião, vamos mais "baixo nível", na tentativa de entender como é que as propriedades conferidas por esta cifra autenticada podem efetivamente ser estabelecidas por recorrência a técnicas criptográficas existentes. 

**Para esse fim, vamos desenvolver três versões de cifras pela diferente combinação entre uma cifra simétrica e de um MAC:**

1. [encrypt and MAC](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G3/EncryptAndMAC.py).
2. [encrypt then MAC](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G3/EncryptThenMAC.py).
3. [MAC then encrypt](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G3/MACThenEncrypt.py).

--- 

## Resolução do Guião

- ### **encrypt and MAC**

Este método não garante qualquer integridade sobre o texto cifrado, uma vez que o MAC (*Message Authentication Code*) é aplicado sobre o texto simples.

Ter em conta que o MAC se trata de uma informação curta usada para confirmar que uma mensagem veio de certo remetente, não tendo sido alterada. Isto acaba por proteger a integridade dos dados e a sua autenticidade, permitindo verificar possíveis alterações no conteúdo da mensagem.

Com isso em mente, facilmente se entende que este método abre as portas para alguns ataques em relação ao texto cifrado, dado que apenas conseguimos verificar erros no toca ao texto original/limpo. 

**Pelo conhecimento do método, foram criados os seguintes passos para a obtenção da solução:**

1. Recolhem-se os valores aleatórios do *Salt* e *Nonce* com 16 bits. O *Salt* será usado na criação da instância da classe *PBKDF2HMAC* e o *Nonce* servirá para participar do algoritmo ```ChaCha20```.
2. Cria-se a instância mencionada anteriormente, seguindo-se os mesmos passos do [Guião 2](https://github.com/uminho-miei-crypto/1920-G9/tree/master/Gui%C3%B5es/G2), em que se pede uma *passphrase* ao utilizador e depois se obtém uma chave derivada. Esta chave derivada de 64 bits é dividida em duas com 32 bits cada - a chave de encriptação e a chave para o MAC.
3. Com as duas chaves e por aplicação do algoritmo ```ChaCha20``` e da função ```HMAC-Sha256```, conseguimos obter o criptograma e a *tag* MAC, respetivamente. Ambos são guardados num ficheiro, finalizando-se assim a parte de encriptação da informação.

Para se desencriptar é só recorrer ao método *decryptor()*, obtendo-se a mensagem que em si foi encriptada anteriormente.

- ###  **encrypt then MAC**

Este método fornece integridade sobre o texto cifrado, dado que o texto limpo passa originalmente pela cifra, e o MAC é calculado já sobre o criptograma. Isso faz com que este seja o modo mais eficiente/recomendado para proteger a informação e o mais simples de provar toda a segurança em termos da criptografia.

Por aplicação desta implementação, um texto cifrado inválido não pode servir de ataque, já que o MAC opera sobre o texto cifrado impossibilitando a denúncia de informações acerca do tempo original.

**Em termos de algoritmo de resolução, é similar ao anterior, diferindo apenas no cálculo do MAC:**

  - No algoritmo do método anterior, tratáva-mos da parte do criptograma e depois do cálculo da *tag* MAC. Ambos eram aplicados sobre o texto limpo.

  ```
      ...
      mensagemEncriptada = encryptor.update(textoCifrar)

    # Parte HMAC.
    mac = hmac.HMAC(chaveMAC, hashes.SHA256(), 
                    backend = default_backend())
    mac.update(textoCifrar)
  ```

  - Neste método, o MAC é calculado sobre o criptograma.

  ```
      ...
      mensagemEncriptada = encryptor.update(textoCifrar)

    # Parte HMAC já com o criptograma.
    mac = hmac.HMAC(chaveMAC, hashes.SHA256(), 
                    backend = default_backend())
    mac.update(mensagemEncriptada)
  ```

- ### **MAC then ecnrypt**

Este método não fornence, igualmente ao método encrypt and MAC, qualquer integridade sobre o texto cifrado, pois não existe forma de saber se a mensagem foi "atacada"/modificada até a mesma ser decifrada. Isto acontece porque primeiro é calculado o MAC sobre o texto limpo, e só depois é cifrado (texto limpo e tag de autenticação).

---

## Observações Finais

