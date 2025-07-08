import requests

url = 'http://94.237.57.211:37932/login'
data = {
    "username": "admin",
    "password": "admin"
}

r = requests.post(url, data=data)
print(r.text)
