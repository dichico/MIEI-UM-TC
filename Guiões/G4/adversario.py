class Adversario:
    
    m = [0, 1]

    def __init__(self, m0, m1):
        self.m[0] = m0
        self.m[1] = m1
    
    def choose(self, enc_oracle):

        self.m[1] = enc_oracle
        self.m[0] = 0

        return self.m[0], self.m[1]

    def guess(self, enc_oracle, c):
        return enc_oracle==c