# Guião 5 - Comunicação Cliente-Servidor

Até então estivemos a tentar entender como poderíamos manter uma proteção ao nível dos segredos criptográficos. Começamos pelo mais base, com o mecanismo de cifra autenticada ```Fernet```, aprofundando depois esse estudo para outras vertentes, por aplicação de outras técnicas criptográficas disponíveis.

Neste guião pretende-se garantir simultaneamente a ```confidencialidade``` dos dados e a ```integridade``` da informação, numa aplicação que estabelece uma comunicação entre um número arbitário de Clientes e determinado Servidor. Para isso, deverá usar-se uma Cifra por Blocos no modo mais apropriado para a tratamento dos dados.

---

## Resolução do Guião

Para se realizar este guião, foi escolhida a implementação ```Fernet```, dado que sabemos que garante aquilo que é pedido. Alternativamente, usa-se também a Cifra ```ChaCha20```, mas sem combinar com um MAC, tendo em conta que apenas se pretende implementar a base da cifra para permitir uma comunicação "minimamente" fiável.

**Assim, existem duas pastas que representam as duas versões do programa:**

1. [**```Fernet```**]( [https://github.com/uminho-miei-crypto/1920-G9/tree/master/Gui%C3%B5es/G5/Fernet](https://github.com/uminho-miei-crypto/1920-G9/tree/master/Guiões/G5/Fernet)) - Quando se inicia a classe [Server.py](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G5/Fernet/Server.py), guarda-se uma chave ```Fernet``` num ficheiro de texto. Assim, cada classe [Cliente.py](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G5/Fernet/Client.py) poderá ter a mesma chave, permitindo que o processo de encriptação e desencriptação ocorra da forma esperada.

   ```python
   # Encrypt Message to send to Server.
   f = Fernet(key)
   encryptMessage = f.encrypt(textInput)
   ```

   ```python
   # Decrypt Message received from Client.
   f = Fernet(key)
   decryptMessage = f.decrypt(msg)
   ```
   
2. [**```ChaCha20```**]( [https://github.com/uminho-miei-crypto/1920-G9/tree/master/Gui%C3%B5es/G5/Fernet](https://github.com/uminho-miei-crypto/1920-G9/tree/master/Guiões/G5/Fernet)) - Quando se inicia a classe [Server.py](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G5/ChaCha20/Server.py), guarda-se uma *key* juntamente com um *nonce* gerados aleatoriamente num ficheiro nomeado de [keyAndNonce.key](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G5/ChaCha20/keyAndNonce.key). Isto é importante para garantir que o processo de encriptar e desencriptar funcione, já que é necessário que ambos sejam os mesmos nos dois lados do programa. 

   Assim, quando uma classe [Cliente.py](https://github.com/uminho-miei-crypto/1920-G9/blob/master/Gui%C3%B5es/G5/ChaCha20/Client.py) é inciada, lê-se esse ficheiro e extrai-se individualmente a *key* e o *nonce*, aplicando-se o algoritmo ```ChaCha20``` para se conseguir criar a Cifra essencial a ambos os processos.
   
   ```python
   # Encrypt Message to send to Server.
   algorithm = algorithms.ChaCha20(keyAndNonce[:32], keyAndNonce[32:])
cipher = Cipher(algorithm, mode=None, backend = default_backend())
   
   encryptor = cipher.encryptor()
   encryptMessage = encryptor.update(textInput)
   ```
   
   ```python
   # Decrypt Message received from Client.
   algorithm = algorithms.ChaCha20(key, nonce)
   cipher = Cipher(algorithm, mode=None, backend = default_backend())
   
   decryptor = cipher.decryptor()
   decryptMessage = decryptor.update(msg)
   ```

---

## Observações Finais

Nada a apontar.
