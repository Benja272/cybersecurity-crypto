import requests
import base64

server = "https://ciberseguridad.diplomatura.unc.edu.ar/cripto/ecb-forge/"
email = "benjamin.picech@mi.unc.edu.ar"
tex1 = f"{'a'*11 + 'admin' + 'b' * 11 + 'a'*9}@gmail.admin"
tex2 = f"{'a'*11 + 'admin' + 'b' * 11 + 'a'*10}@gmail.com"
response = requests.get(f"{server}/{email}/register?email={tex2}&encrypted=false")
challenge2 = response.text
print(challenge2)
for i in range(5):
  print(challenge2[i*16:(i+1)*16])
decoded2 = base64.b64decode(challenge2)
print("len decoded2", len(decoded2))
zero_padding = decoded2[-16:]
response1 = requests.get(f"{server}/{email}/register?email={tex1}&encrypted=false")
print(response1.text)
decoded = base64.b64decode(response1.text)
print("len decoded", len(decoded))
for i in range(5):
  print(response1.text[i*16:(i+1)*16])
print(challenge2[16:32] + challenge2[:16]+ challenge2[-32:-16] + response1.text[-32:])
message = decoded2[16:32] + decoded2[:16]+ decoded2[-32:-16] + decoded[-32:]
print(decoded[0])
response = requests.post(f"{server}/{email}/answer", files={"message": base64.b64encode(message)})
print(response.text)