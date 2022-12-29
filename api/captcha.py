import requests

import api.ocr as ocr


def refresh_captcha(uuid: str, cookies: str, referer: str) -> bytes:
    url = 'https://jaccount.sjtu.edu.cn/jaccount/captcha?uuid=' + uuid
    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': cookies,
        'Referer': referer,
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }
    image = requests.get(url, headers=headers).content
    # If you need to save the .jpeg image
    # with open(os.path.dirname(os.path.abspath(__file__)) + '/captcha.jpeg', 'wb') as file:
    #    file.write(image)
    return image


def captcha(uuid: str, cookies: str, referer: str) -> str:
    image = refresh_captcha(uuid, cookies, referer)
    return ocr.ocr(image)
