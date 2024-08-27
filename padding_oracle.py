import itertools
import requests
import base64
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Placeholder for server and email
server = "https://ciberseguridad.diplomatura.unc.edu.ar/cripto/padding-oracle"
email = "benjamin.picech@mi.unc.edu.ar"

# Function to get the ciphertext (AES in CBC mode)
def get_ciphertext():
    response = requests.get(f"{server}/{email}/challenge")
    if response.status_code == 200:
        return base64.b64decode(response.text)
    else:
        raise Exception("Failed to retrieve ciphertext")

# Function to send the manipulated ciphertext for validation (Padding Oracle check)
def padding_oracle(ciphertext):
    response = requests.post(f"{server}/{email}/decrypt", files={'message': base64.b64encode(ciphertext)})
    if response.status_code == 200:
        return True  # Valid padding
    elif "Bad padding bytes" in response.text:
        return False  # Invalid padding
    else:
        raise Exception("Unexpected server response")

# Parallelized padding oracle attempt for a single byte with logging
def attempt_padding_oracle(byte_guess, temp, previous_block, current_block, byte_index):
    padding_value = byte_index
    modified_bytes = [byte_guess] + list(temp)
    modified_block = previous_block[0: 16 - byte_index] + bytes(modified_bytes)

    # Log the attempt
    try: 
      if padding_oracle(bytes(modified_block + current_block)):
          print(temp, previous_block, current_block)
          logging.info(f"Valid padding found for byte_guess: {byte_guess} at byte_index: {byte_index}")
          return byte_guess
    except Exception as e:
        logging.error(f"Error occurred during padding oracle attempt: {str(e)}")
    return None

def padding_oracle_attack(ciphertext):
    block_size = 16  # AES block size in bytes
    num_blocks = len(ciphertext) // block_size
    plaintext = bytearray()

    # Split the ciphertext into blocks
    blocks = [ciphertext[i * block_size:(i + 1) * block_size] for i in range(num_blocks)]
    print(num_blocks)
    # Iterate over each block (except the first IV block, which we skip)
    for block_index in range(1, num_blocks):
        current_block = blocks[block_index]
        previous_block = blocks[block_index - 1]
        recovered_plaintext = bytearray(block_size)
        guesses = bytearray(block_size)

        # Recover each byte of the block (from last byte to first byte)
        for byte_index in range(1, block_size + 1):
            padding_value = byte_index
            temp = bytearray()
            if byte_index > 1:
                temp = guesses[-byte_index + 1:].copy()
            print(temp)
            for i in range(byte_index - 1):
                temp[i] ^= padding_value ^ byte_index - i - 1
            print(temp)
            
            # Use ThreadPoolExecutor for parallelizing byte guesses
            with ThreadPoolExecutor(max_workers=50) as executor:
                l=[]
                for byte_guess in range(256):
                  if byte_guess != 167:
                    l.append(byte_guess)
                if byte_index == 1 and block_index == 9:
                  futures = {executor.submit(attempt_padding_oracle, byte_guess, temp, previous_block, current_block, byte_index): byte_guess for byte_guess in l}
                else:
                  futures = {executor.submit(attempt_padding_oracle, byte_guess, temp, previous_block, current_block, byte_index): byte_guess for byte_guess in range(256)}
                
                for future in as_completed(futures):
                    result = future.result()
                    if result is not None:
                        recovered_byte = result ^ previous_block[-byte_index] ^ padding_value
                        recovered_plaintext[-byte_index] = recovered_byte
                        guesses[-byte_index] = result
                        break
        with open("recovered_plaintext1.txt", "ab") as f:
            f.write(recovered_plaintext)
        print(recovered_plaintext, block_index)
        plaintext.extend(recovered_plaintext)

    return plaintext

# Fetch ciphertext and execute the padding oracle attack
try:
    ciphertext = get_ciphertext()
    # decrypted_message = padding_oracle_attack(ciphertext)
    with open("recovered_plaintext1.txt", "rb") as f:
        message = f.read()
    # print(message.encode('ascii'))
    message = ciphertext[0:16] + message
    print(f"{server}/{email}/answer")
    response = requests.post(f"{server}/{email}/answer", files={"message": base64.b64encode(message)})
    print(response.text)
    # print(decrypted_message)  # Display the first 256 characters for preview
except Exception as e:
    logging.error(f"Error occurred: {str(e)}")
