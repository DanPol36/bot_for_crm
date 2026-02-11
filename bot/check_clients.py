import requests

try:
    r = requests.get('http://127.0.0.1:5000/clients?format=json', timeout=5)
    print('STATUS', r.status_code)
    print('FINAL_URL', r.url)
    print('HISTORY', [(h.status_code, h.headers.get('Location')) for h in r.history])
    print('CTYPE', r.headers.get('Content-Type'))
    print('BODY PREVIEW:\n')
    print(r.text[:2000])
except Exception as e:
    print('ERROR', repr(e))
