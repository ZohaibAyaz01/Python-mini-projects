import requests
import sys

def api():
    for word in sys.stdin:
        url = f"http://testphp.vulnweb.com/{word}"
        res = requests.get(url)
        if res.status_code == 404:
            api()
        else:
            print(res.status_code)
            print(word)
            data=res.json()
            print(data)
api()