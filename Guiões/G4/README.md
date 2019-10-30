# Guião 4 - Animação de Modelos de Segurança

Um ataque *Chosen Plaintext Attack* é um modelo de ataque para análise de segurança onde se presume que o atacante pode obter os textos cifrados para textos limpos arbitários.

Esta ideia é formalizada de modo a permitir que o atacante consiga interagir com o *oracle* criptográfico, tentando assim revelar parte da *key* secreta.

---

## Resolução do Guião

Para este Guião, a ideia base era animar o modelo \```IND-CPA```, permitindo com isto obter uma ideia da importância deste tipo de ataque (e outros) no contexto da criptografia de *keys* públicas, onde a *key* é pública e o atacante pode encriptar qualquer *Chosen Plaintext* à escolha.



**No geral, o ataque consistiu na escolha de textos limpos por parte do atacante, sendo realizado da seguinte forma:**

1. O atacante escolhe/possui 2 *plain text* pré-determinados;
2. O atacante envia esses 2 textos para o *oracle* criptográfico;
3. O *oracle* encripta os *plain text*, enviando-os de volta ao atacante;
4. O atacante recebe os 2 textos encriptados.



Com base nestes textos encriptados, o atacante pode então tentar extrair a *key* usada pelo oráculo para tentar fazer o processo inverso, descobrindo qual texto encriptado corresponde ao seu texto limpo.

Esta ideia geral de um ataque ```IND-CPA``` foi transposta para código em *Python*, no qual foram desenvolvidas duas classes essenciais que visam colocar em prática o ataque e facilitar o processo. A ideia era adptar este "programa" para testes com outras cifras/ataques, mas dada a complexidade em entender como fazê-lo, foi apenas desenvolvida a base do requerido. 



**Vejamos então os ficheiros/classes *Python* desenvolvido**:



​	**1. adversario.py**

Este ficheiro representa a classe do Adversário, contendo os dois métodos necessários para que ele faça a escolha dos seus textos limpos e tente adivinhar a qual desses textos pretence o criptograma enviado para si.



- A função *choose* atribui os valores dos textos limpos, fazendo já a encriptação desses mesmos, dado que lhe é passado o *oracle* para que possa fazer isto.

```python
def choose(self, enc_oracle):
	return enc_oracle(self.m[0]), enc_oracle(self.m[1])
```

- Tendo em conta que o atacante tem acesso ao Enck(.), então ele pode facilmente obter um c0 <- Enck(m0) e um c1 <- Enck(m1). Com estes dois, ele pode fazer uma comparação com o criptograma recebido e perceber a qual das mensagens corresponde.

```python
def guess(self, enc_oracle, c):
	c0 = enc_oracle(self.m[0])
   	c1 = enc_oracle(self.m[1])
   	
	if c == c0: return 0
	else: return 1
```



---

## Observações Finais

