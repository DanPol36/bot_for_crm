from dotenv import load_dotenv
import os, requests, json
load_dotenv(r'c:/тг_бот/bot/.env')
token = os.getenv('BOT_TOKEN')
if not token:
    print('No BOT_TOKEN')
    raise SystemExit(1)
url = f'https://api.telegram.org/bot{token}/getUpdates'
r = requests.get(url, timeout=10)
print('HTTP', r.status_code)
js = r.json()
print(json.dumps(js, ensure_ascii=False, indent=2))
if js.get('ok') and js.get('result'):
    ids = [u['update_id'] for u in js['result']]
    if ids:
        last = max(ids)
        print('Clearing offset to', last+1)
        r2 = requests.get(url, params={'offset': last+1}, timeout=10)
        print('ACK HTTP', r2.status_code)
        try:
            print(r2.json())
        except Exception:
            print(r2.text)
else:
    print('No updates to clear')
