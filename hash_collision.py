import requests
from hashlib import sha256
import itertools


def generate_bytes(length=5):
    all_printable_bytes = list(range(33, 127))
    for item in itertools.product(all_printable_bytes, repeat=length):
        yield bytes(item)


server = "https://ciberseguridad.diplomatura.unc.edu.ar/cripto"
email = "benjamin.picech@mi.unc.edu.ar"
a = 0
msg = email.encode() + a.to_bytes(1, "big")
possible_bytes = generate_bytes()
hashes = {}
while(True):
    print(msg)
    hash = sha256(msg).hexdigest()[:12]
    if hashes.get(hash, False):
        print("Colision")
        print(hash, msg)
        print(sha256(hashes[hash]).hexdigest()[:12], hashes[hash])
        msg1 = msg
        msg2 = hashes[hash]
        break
    else:
        hashes[hash] = msg
        msg = email.encode() + possible_bytes.__next__()

# msg1 = b"benjamin.picech@mi.unc.edu.ar!/n>6"
# msg2 = b"benjamin.picech@mi.unc.edu.ar!+Bk<"

response = requests.post(
    f"{server}/collision/{email}/answer",
    files={"message1": msg1, "message2": msg2})
print(response.status_code)
print(response.text)

