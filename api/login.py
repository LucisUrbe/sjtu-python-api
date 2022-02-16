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
                if '&err=' in response.url:
                    if '&err=1' in response.url:
                        print('[WARN/LOGIN] WRONG CAPTCHA SOLUTION, RETRYING...')
                    elif '&err=0' in response.url:
                        print('[ERROR/LOGIN] WRONG USER NAME OR PASSWORD!')
                        return {} #
                    elif '&err=2' in response.url:
                        print('[ERROR/LOGIN] SJTU JACCOUNT SYSTEM IS DOWN, PLEASE TRY AGAIN LATER.')
                        quit(-2)
                    elif '&err=3' in response.url:
                        print('[ERROR/LOGIN] ACCOUNT FROM DELEGATED AGENCY DOES NOT EXIST, PLEASE RETRY SELECTION.')
                        quit(-3)
                    elif '&err=4' in response.url:
                        print('[ERROR/LOGIN] ACCOUNT FROM DELEGATED AGENCY HAS EXPIRED, PLEASE RETRY SELECTION.')
                        quit(-4)
                    elif '&err=5' in response.url:
                        print('[ERROR/LOGIN] CURRENT DELEGATED AGENCY IS INVALID, PLEASE RETRY SELECTION.')
                        quit(-5)
                    elif '&err=6' in response.url:
                        print('[ERROR/LOGIN] YOU HAS CHANGED YOUR PASSWORD. CURRENT SESSION REQUIRE YOU TO RETRY LOGIN.')
                        return {}
                    elif '&err=7' in response.url:
                        print('[ERROR/LOGIN] YOUR ACCOUNT IS CURRENTLY NOT LOG-ABLE.')
                        quit(-7)
                    elif '&err=8' in response.url:
                        print('[ERROR/LOGIN] LOGIN SESSION IS STALE. PLEASE RETRY.')
                        return {} #
                    elif '&err=9' in response.url:
                        print('[ERROR/LOGIN] QR CODE IS STALE. PLEASE REFRESH.')
                        return {} #
                    elif '&err=10' in response.url:
                        print('[ERROR/LOGIN] SJTU INFOPLUS TASKCENTER LOGIN IS STALE. RETRY LOGGIN IN TO THE APP.')
                        return {} #
                    elif '&err=11' in response.url:
                        print('[ERROR/LOGIN] PLEASE SCAN QR CODE BY WECHAT OR SJTU INFOPLUS TASKCENTER.')
                        return {} #
                    elif '&err=12' in response.url:
                        print('[ERROR/LOGIN] EXCEPTION WHILE FETCHING WECHAT LOGIN. PLEASE RETRY.')
                        return {} #
                    elif '&err=13' in response.url:
                        print('[ERROR/LOGIN] NO JACCOUNT BINDED TO WECHAT. PLEASE LOG IN BY USER NAME AND PASSWORD.')
                        quit(-13)
                    else:
                        print('[ERROR/LOGIN] UNDEFINED ERROR.')
                else:
                    print('[WARN/LOGIN] WEAK NETWORK CONNECTION, RETRYING...', response.url)
                    
        
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
            if '&err=' in response.url:
                print('[ERROR/LOGIN] AN ERROR OCCURRED WHILE LOGGIN IN. CONSIDER A WRONG USER NAME OR PASSWORD, OR A WEAK NETWORK QUALITY.')
                return {} #
            cookies = session.cookies.get_dict() # dict
        return cookies
    except Exception as error:
        print('[ERROR/LOGIN]', error)
