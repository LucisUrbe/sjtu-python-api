import requests

import api.ocr as ocr


def refresh_captcha(uuid: str, cookies: str) -> bytes:
    try:
        url = 'https://jaccount.sjtu.edu.cn/jaccount/captcha?uuid=' + uuid
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
            'Content-Type': 'text/html;charset=utf-8',
            'Cookie': cookies
        }
        image = requests.get(url, headers=headers).content
        # If you need to save the .jpeg image
        # with open(os.path.dirname(os.path.abspath(__file__)) + '/captcha.jpeg', 'wb') as file:
        #    file.write(image)
        return image
    except Exception as error:
        print('[ERROR/REFRESH_CAPTCHA]', error)


def captcha(uuid: str, cookies: str) -> str:
    try:
        image = refresh_captcha(uuid, cookies)
        return ocr.ocr(image)
    except Exception as error:
        print('[ERROR/CAPTCHA]', error)
