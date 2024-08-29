import requests
import urllib.parse
from cryptography.hazmat.primitives import padding as symmetric_padding

server = "https://ciberseguridad.diplomatura.unc.edu.ar/cripto/cbc-mac/"
email = "benjamin.picech@mi.unc.edu.ar"

def get_challenge():
    response = requests.get(f"{server}{email}/challenge")
    print(response.content)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Error al obtener el desafío")

def send_response(query):
    encoded_query = urllib.parse.quote(query, safe='=&@%')
    print(f"Query codificada: {encoded_query}")
    response = requests.get(f"{server}{email}/answer?{encoded_query}")
    return response.text

def pad_message(message, block_size):
    padder = symmetric_padding.PKCS7(block_size * 8).padder()
    print(message)
    padded_data = padder.update(message) + padder.finalize()
    print(padded_data)
    return padded_data

def generate_forged_query(challenge):
    components = challenge.split("&")
    original_mac = components[-1].split("=")[1]
    original_query = "&".join(components[:-1])

    repetitions = 10
    mac_bytes = bytes.fromhex(original_mac)
    block_size = len(mac_bytes)
    print(original_query)

    query_bytes = original_query.encode()

    padded_query = pad_message(query_bytes, block_size)

    first_block_xor_mac = bytearray(padded_query[:block_size])
    for j in range(min(len(first_block_xor_mac), block_size)):
        first_block_xor_mac[j] ^= mac_bytes[j]

    forged_blocks = padded_query
    for i in range(repetitions):
        if(i != repetitions - 1):
            forged_blocks += first_block_xor_mac + padded_query[block_size:]
        else:
            forged_blocks += first_block_xor_mac + query_bytes[block_size:]

    forged_query = forged_blocks + b"&mac=" + original_mac.encode()
    return forged_query

# Obtener el desafío original
challenge = get_challenge()
print(f"Desafío original: {challenge}")

# Generar la query forjada
forged_query = generate_forged_query(challenge)
print(f"Query forjada: {forged_query}")

# Enviar la respuesta forjada
response = send_response(forged_query)
print(f"Respuesta del servidor: {response}")
