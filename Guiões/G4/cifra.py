class Cifra:

    def keygen(self):
        return Fernet.generate_key()

    def enc(self, key, text):
        f = Fernet(key)
        return f.encrypt(text)