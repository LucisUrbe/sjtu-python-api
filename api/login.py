import requests
import matplotlib.pyplot as plt
from io import BytesIO

import api.form as form
import api.captcha as captcha


def login(jaccount_name: str, jaccount_password: str) -> dict:
    try:
        if jaccount_name == '' or jaccount_password == '':
            raise ValueError('INVALID USER NAME OR PASSWORD.')
        session = requests.Session()
        url = 'https://i.sjtu.edu.cn/jaccountlogin'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        } # initial headers
        response = session.get(url, headers=headers)

        cookies = ''
        for key, value in response.cookies.items():
            cookies += key + '=' + value + ';'
        
        headers.update({
            'Cookie': cookies,
            'Origin': 'https://jaccount.sjtu.edu.cn',
        }) # headers with jaccount session id
        
        submit = form.form(response.text) # critical form submission values
        submit.update({
            'user': jaccount_name,
            'pass': jaccount_password,
        })

        for _ in range(1, 10): # try maximum 10 times
            jaccount_captcha = captcha.captcha(submit['uuid'], cookies).strip().replace(' ','')

            submit.update({
                'captcha': jaccount_captcha
            })

            url = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin?'
            for key, value in submit.items():
                url += key + '=' + value + '&'
            response = session.post(url, headers=headers)

            cookies = session.cookies.get_dict() # dict
            if (cookies.get('JAAuthCookie') is not None):
                return cookies
            else:
                cookies = ''
                for key, value in response.cookies.items():
                    cookies += key + '=' + value + ';'
                print('[WARN/LOGIN] WRONG CAPTCHA SOLUTION, RETRYING...')
        
        print('[WARN/LOGIN] 10 TIMES ERROR ON CAPTCHA')
        cookies = session.cookies.get_dict()
        while (cookies.get('JAAuthCookie') is None):
            print('[WARN/LOGIN] YOU MUST RETRY CAPTCHA MANUALLY')

            from api.captcha import refresh_captcha
            image = refresh_captcha(submit['uuid'], cookies)
            plt.imshow(plt.imread(BytesIO(image)))
            plt.imshow()

            jaccount_captcha = input('<CAPTCHA>:')
            submit.update({
                'captcha': jaccount_captcha
            })

            url = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin?'
            for key, value in submit.items():
                url += key + '=' + value + '&'
            response = session.post(url, headers=headers)

            cookies = session.cookies.get_dict() # dict
        return cookies
    except Exception as error:
        print('[ERROR/LOGIN]', error)
