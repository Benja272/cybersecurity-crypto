import requests
import urllib.parse

server = "https://ciberseguridad.diplomatura.unc.edu.ar/cripto/cbc-mac/"
email = "benjamin.picech@mi.unc.edu.ar"
from cryptography.hazmat.primitives import padding as symmetric_padding

def get_challenge():
    response = requests.get(f"{server}{email}/challenge")
    print(response.content)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Error al obtener el desafío")

def send_response(query):
    encoded_query = urllib.parse.quote(query, safe='=&@<>')
    print(f"Query codificada: {encoded_query}")
    response = requests.get(f"{server}{email}/answer?{encoded_query}")
    return response.text

# Función para generar la falsificación
def generate_forged_query(challenge):
    # Extraemos los valores clave
    components = challenge.split("&")
    original_mac = components[-1].split("=")[1]  # El valor de 'mac'
    original_query = "&".join(components[:-1])  # La parte del mensaje sin el MAC

    # Repetimos la query 10 veces, aplicando XOR en cada primer bloque
    repetitions = 10
    forged_query = original_query
    mac_bytes = bytes.fromhex(original_mac)

    # Asumimos que el primer bloque corresponde al tamaño del MAC (tamaño del bloque)
    query_blocks = forged_query.encode()
    print(len(query_blocks))
    print(len(mac_bytes))
    print(len(query_blocks) % len(mac_bytes))
    block_size = len(mac_bytes)  # El tamaño de bloque es el mismo que el MAC
    padder = symmetric_padding.PKCS7(block_size).padder()
    query_blocks = padder.update(forged_query.encode()) + padder.finalize()
    forged_blocks = query_blocks

    # Generamos la falsificación
    first_block_xor_mac = bytearray(query_blocks[:block_size])  # Tomamos el primer bloque
    print(len(query_blocks) % block_size)
    for j in range(block_size):
        first_block_xor_mac[j] ^= mac_bytes[j]  # XOR con el MAC
    for i in range(repetitions):
      forged_blocks += first_block_xor_mac + query_blocks[block_size:]
    # Convertimos los bloques forjados en la query string
    forged_query = forged_blocks + f"&mac={original_mac}".encode()
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
