import requests

r = requests.post(url = 'https://async.scraperapi.com/jobs', json={ 'apiKey': '0b6f67d719ccaadd11ea8a52d82dbfad', 'url': 'https://example.com' })
print(r.text)