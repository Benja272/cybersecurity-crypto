import base64
import requests
from datetime import datetime
from hashlib import md5
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import serialization, hashes, padding as symmetric_padding
from cryptography.hazmat.backends import default_backend

def descript_message(message, date):
    iv = message[128:144]
    print("IV len ", len(iv))
    print("IV: ", iv)
    print("Date: ", date.timestamp(), date)
    print("Date in ms: ", date.timestamp() * 1_000_000)
    print("Text len: ", len(message[144:]))
    # Recorremos los posibles valores de la fecha en microsegundos.
    for i in range(1_000_000):
        ps_date = int(date.timestamp() * 1_000_000 + i)
        if i==1 or i==999_999:
          print(ps_date)
          print(datetime.fromtimestamp(ps_date/1000000).isoformat())

        key_seed = ps_date.to_bytes(8,"big")
        key = md5(key_seed).digest()
        # Obtenemos una instancia del descifrador
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        # Desciframos
        decrypted = decryptor.update(message[144:]) + decryptor.finalize()
        try:
          # Quitamos el padding
          unpadder = symmetric_padding.PKCS7(128).unpadder()
          unpadded = unpadder.update(decrypted)
          unpadded += unpadder.finalize()

          print(unpadded.decode('ascii'))
          print(key.hex())
          print("--------------")
        except Exception as error:
          error_msg = error.__str__()
          # if error_msg != "Invalid padding bytes.":
          #   if (error_msg[error_msg.find("position") + 9] != "0"):
          #     print(error)
          continue



server = "https://ciberseguridad.diplomatura.unc.edu.ar/cripto/timerand/"
email = "benjamin.picech@mi.unc.edu.ar"
date_format = "%a %b %d %H:%M:%S %Z %Y"
response = requests.get(f"{server}/{email}/challenge")
challenge = response.text
for line in challenge.splitlines():
    if line.startswith("Date: "):
        date = line[6:]

encoded = challenge.splitlines()[-1]
decoded = base64.b64decode(encoded)
date_obj = datetime.strptime(date, date_format)
print(date_obj)
print(challenge.splitlines())
print("Trying decode cipher text")
descript_message(decoded, date_obj)