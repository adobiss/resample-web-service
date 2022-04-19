import requests

url = 'http://127.0.0.1:8000/files/'
file = {'inFile': open(r"C:\Users\AD\Desktop\You Tell Me.mp3", 'rb')}
response = requests.post(url=url, files=file)
json_data = response.json()
file = {'inFile': (open(r"C:\Users\AD\Desktop\You Tell Me.mp3", 'rb')).close()}
print(json_data)