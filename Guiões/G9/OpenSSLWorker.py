from OpenSSL import crypto

with open('Certificados/CAPEM.cer', 'r') as ca_file:
    ca_pem = ca_file.read()


# A criação duma X509 Store para guardar o nosso Certificate Authority (CA)
store = crypto.X509Store()
ca = crypto.load_certificate(crypto.FILETYPE_PEM, ca_pem)
store.add_cert(ca)

def clientCertVerify():
    
    # Abertura do PKCS12 com o certificado do cliente lá dentro.
    with open('Certificados/Cliente1.p12', 'rb') as client_file:
        clientPKCS12 = client_file.read()
    
    p12Client = crypto.load_pkcs12(clientPKCS12, bytes('1234', 'utf-8'))
    certificateClient = p12Client.get_certificate()

    # Criação dum X509StoreContext entre a nossa store o certificado a verificar.
    store_ctx = crypto.X509StoreContext(store, certificateClient)

    # Verificação do chain of trust.
    try:
        store_ctx.verify_certificate()
        print("Verificado o chain of trust do cliente")
    except Exception:
        print("Não se conseguiu verificar.")

def serverCertVerify():
    
    # Abertura do PKCS12 com o certificado do cliente lá dentro.
    with open('Certificados/Servidor.p12', 'rb') as servidor_file:
        servidorPKCS12 = servidor_file.read()
    
    p12Servidor = crypto.load_pkcs12(servidorPKCS12, bytes('1234', 'utf-8'))
    certificateServidor = p12Servidor.get_certificate()

    # Criação dum X509StoreContext entre a nossa store o certificado a verificar.
    store_ctx = crypto.X509StoreContext(store, certificateServidor)

    # Verificação do chain of trust.
    try:
        store_ctx.verify_certificate()
        print("Verificado o chain of trust do servidor.")
    except Exception:
        print("Não se conseguiu verificar.")