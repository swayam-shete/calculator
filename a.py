import requests
import json

url = "https://p3gp1w5s-5000.inc1.devtunnels.ms/employee?testingparam=989"

payload = json.dumps({
  "name": "swayam",
  "age": 2,
  "course": "if",
  "email": "swayam.12@gamil.com"
})
headers = {
  'Content-Type': 'application/json',
  'test':'abcd'}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
