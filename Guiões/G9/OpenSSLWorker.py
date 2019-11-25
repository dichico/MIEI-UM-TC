from OpenSSL import crypto



with open('CAPEM.cer', 'r') as ca_file:
    trusted_cert_pem = ca_file.read()

with open('Cliente1.p12', 'rb') as client_file:
    clientPKCS12 = client_file.read()

p12Client = crypto.load_pkcs12(clientPKCS12, bytes('1234', 'utf-8'))

cert = p12Client.get_certificate()

certificateClient = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

# Create and fill a X509Store with trusted certs
store = crypto.X509Store()
trusted_cert = crypto.load_certificate(crypto.FILETYPE_PEM, trusted_cert_pem)
store.add_cert(trusted_cert)

# Create a X590StoreContext with the cert and trusted certs
# and verify the the chain of trust
store_ctx = crypto.X509StoreContext(store, certificateClient)

try:
    store_ctx.verify_certificate()
    print("Verificado o chain of trust.")
except X509StoreContextError:
    print("Não se conseguiu verificar.")

