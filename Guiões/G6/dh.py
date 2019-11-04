from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# Número primo e valor de gerador dado pelo professor

P = 99494096650139337106186933977618513974146274831566768179581759037259788798151499814653951492724365471316253651463342255785311748602922458795201382445323499931625451272600173180136123245441204133515800495917242011863558721723303661523372572477211620144038809673692512025566673746993593384600667047373692203583
G = 44157404837960328768872680677686802650999163226766694797650810379076416463147265401084491113667624054557335394761604876882446924929840681990106974314935015501571333024773172440352475358750668213444607353872754650805031912866692119819377041901642732455911509867728218394542745330014071040326856846990119719675

# Generate some parameters. These can be reused.
# parameters = dh.generate_parameters(generator=2, key_size=2048,
#                                     backend=default_backend())

parameters = dh.DHParameterNumbers(P, G, None).parameters(backend=default_backend())

# Generate a private key for use in the exchange.
server_private_key = parameters.generate_private_key()

# In a real handshake the peer is a remote client. For this
# example we'll generate another local private key though. Note that in
# a DH handshake both peers must agree on a common set of parameters.

peer_private_key = parameters.generate_private_key()

shared_key = server_private_key.exchange(peer_private_key.public_key())

# Perform key derivation.
derived_key = HKDF(
algorithm=hashes.SHA256(),
length=32,
salt=None,
info=b'handshake data',
backend=default_backend()
).derive(shared_key)

# And now we can demonstrate that the handshake performed in the
# opposite direction gives the same final value

same_shared_key = peer_private_key.exchange(
server_private_key.public_key()
)

same_derived_key = HKDF(
algorithm=hashes.SHA256(),
length=32,
salt=None,
info=b'handshake data',
backend=default_backend()
).derive(same_shared_key)

print(derived_key == same_derived_key)