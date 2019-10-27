import random
import string

class Adversario:

    m = ["Texto Limpo 1", "Texto Limpo 2"]

    def choose(self):

        return self.m[0], self.m[1];

    def guess(self, enc_oracle, c):
        
        c0 = enc_oracle(self.m[0])
        c1 = enc_oracle(self.m[1])
        print("----GUESS----")
        print(c0)
        print()
        print(c1)
        print("-------")
        if c == c0: return 0
        else: return 1