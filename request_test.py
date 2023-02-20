import requests


url = "https://app.handsnetwork.com/rest_free/pos/getPosChk"
api_key = "eyJhbGciOiJzaGEyNTYiLCJ0eXAiOiJKV1QifS57ImV4cCI6MTY3Njg2ODk4MiwiaWF0IjoxNjc2ODU4MTgyLCJpZCI6MTAsInVpZCI6ImFHRnVaSE4wWlhOMCIsInNob3BfY2QiOiJUMTE2MzkifS4xYTdjNmQ1ODQ4YmMwODJkZGYyYTYxN2FmOTJjMmM4NjViM2RlYjhmNDY1ZGYyYzZmZDJjNTI3NjM4Y2UwZjIw"
headers = {"authorization": api_key}
res = requests.get(url, headers=headers, params={"shop_cd": "T11639"})

data = eval(res.text)

print(data['cnt'])