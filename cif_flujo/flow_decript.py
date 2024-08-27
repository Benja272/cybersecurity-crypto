
import base64

def has_repeated_ascii_char(bytes_obj):
    if not bytes_obj:
        return False
    return all(byte == bytes_obj[0] for byte in bytes_obj)


def r_key(key, lines, length):
  if len(key) == length:
    print("Key found:")
    print(base64.b64encode(bytes(key)))
    for line in lines:
      c = bytes(x ^ y for (x, y) in zip(key, line))
      try:
        print(c.decode())
      except:
        continue
    return
  j = length - len(key) - 1
  for i in range(256):
    character = bytes([i])
    rep1, rep2, num = False, False, False
    new_key = character + key
    in_ascci = 5
    for line in lines:
      c = bytes(x ^ y for (x, y) in zip(new_key, line[j:]))
      if len(c)  != len(new_key):
        print("Length error")
        print(len(c))
        print(len(new_key))
        break
      if c[0] < 33 or c[0] > 126:
        in_ascci -= 1
      if in_ascci < 3:
        break
      if c.isdigit() and int(c.decode()) % 2 == 0:
        num = True
      if has_repeated_ascii_char(c) and not rep1:
        rep1 = True
      elif has_repeated_ascii_char(c):
        rep2 = True
    if rep1 and rep2 and num:
      r_key(new_key, lines, length)

# open local file called cif with the encrypted text
with open('cif', 'rb') as f:
    data = f.read()
    lines = data.splitlines()
    print(len(lines))

    lines = [base64.b64decode(l) for l in lines]
    #get lines
    length = len(lines[0])
    print("Length of the key:")
    print(length)
    print("Lines:")
    print(lines)
    r_key(b'', lines, length)