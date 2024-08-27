import requests
import base64

server = "https://ciberseguridad.diplomatura.unc.edu.ar/cripto"
email = "benjamin.picech@mi.unc.edu.ar"
data = "datatatatatataa"
data_64 = base64.b64encode(data.encode())
response = requests.post(f"{server}/stream-bitflip/{email}/register", files={"email": email, "data": data_64})
challenge = response.text
print(challenge)
decoded = base64.b64decode(challenge)
print(f"Longitud del texto codificado: {len(challenge)}")
print(f"Longitud del mensaje decodificado: {len(decoded)}")
nonce = decoded[:16]
def xor(a,b):
    return bytes(x^y for x,y in zip(a,b))
new_role = xor(b"a;role=user",decoded[-11:])
new_role = xor(b";role=admin",new_role)
decoded = decoded[:-11] + new_role
print(f"Longitud del mensaje decodificado: {len(decoded)}")
print(f"Nonce: {nonce}")
decoded = base64.b64encode(decoded)
print(f"Longitud del mensaje codificado: {len(decoded)}")
print(str(decoded))




response = requests.post(f"{server}/stream-bitflip/{email}/answer", files={"message": decoded})
print(response.text)
