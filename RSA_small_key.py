import requests
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse, long_to_bytes

# Recuperados con la herramienta msieve, ver msieve.log
p = 300653542617790731163576108228308119467
q = 338422795365762647757884077303702508663

def get_challenge(email):
    url = f"https://ciberseguridad.diplomatura.unc.edu.ar/cripto/rsa-small/{email}/challenge"
    response = requests.get(url)
    return json.loads(response.text)

def decrypt_message(ciphertext, n, e, p, q):
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    c = int.from_bytes(base64.b64decode(ciphertext), 'big')
    m = pow(c, d, n)
    return long_to_bytes(m)

def remove_pkcs1_padding(decrypted):
    return decrypted[decrypted.index(b'\x00', 2) + 1:]

def send_answer(email, message):
    url = f"https://ciberseguridad.diplomatura.unc.edu.ar/cripto/rsa-small/{email}/answer"
    response = requests.post(url, data={'message': message})
    return response.text


def main():
    email = "benjamin.picech@mi.unc.edu.ar"

    challenge = get_challenge(email)
    ciphertext = challenge['ciphertext']
    n = challenge['publicKey']['n']
    e = challenge['publicKey']['e']

    print(f"Ciphertext: {ciphertext}")
    print(f"n: {n}")
    print(f"e: {e}")
    print(f"Factors: p = {p}, q = {q}")
    decrypted = decrypt_message(ciphertext, n, e, p, q)
    message = remove_pkcs1_padding(decrypted)
    print(f"Decrypted message: {message.decode()}")

    # Send the answer
    response = send_answer(email, message)
    print(f"Server response: {response}")

if __name__ == "__main__":
    main()
