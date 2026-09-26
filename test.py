import requests
import json

session = requests.Session()

url = "https://auth.refsix.com/auth/login"

payload = json.dumps({
  "username": "matthewemerson",
  "password": "29me11o6"
})
headers = {
  'Authorization': 'Bearer Q0x1b2FaQVJSVkNaU2oyQ3p6N043dzpDTHVvYVpBUlJWQ1pTajJDeno3Tjd3',
  'Content-Type': 'application/json'
}

response = session.post(url, headers=headers, data=payload)

url = response.json()["userDBs"]["supertest"] + "/_all_docs?include_docs=true"

payload = {}
headers = {}

response = session.get(url, headers=headers, data=payload)

print(len(response.json()["rows"]))