import requests

endpoint = "http://127.0.0.1:8000/login/"

data = {
    'name':'yogesh',
    'email':'yogesh@gmail.com',
    'password':'1234'
}



response = requests.post(endpoint,json=data)

if response.status_code == 200:
    print("success")
    print(list(response))
