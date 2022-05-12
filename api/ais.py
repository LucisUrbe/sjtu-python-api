import requests


def ais() -> dict:
    try:
        url = 'https://i.sjtu.edu.cn/xtgl/login_slogin.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
            'Content-Type': 'text/html;charset=utf-8', 'Cookie': ''
        }
        response = requests.get(url)
        for key, value in response.cookies.items():  
            headers['Cookie'] += key + '=' + value + ';'
        print(response.cookies.items())
        return headers
    except Exception as error:
        print('[ERROR/AIS]', error)
