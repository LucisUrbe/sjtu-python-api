import requests

import api.form as form
import api.captcha as captcha


def login(jaccount_name: str, jaccount_password: str) -> requests.Session:
    # LOCAL CONSTANT STRINGS
    # A. URLs
    URL_JAC_LOGOUT: str = 'https://jaccount.sjtu.edu.cn/oauth2/logout'
    URL_JAC_LOG_IN_SIM: str = 'https://i.sjtu.edu.cn/jaccountlogin'
    URL_JAC_POST_PREFIX: str = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin?'

    # B. Error messages
    ERROR_EMPTY_INPUT: str = 'INVALID USER NAME OR PASSWORD.'

    ERROR_LOGIN_0: str = '[ERROR/LOGIN] WRONG USER NAME OR PASSWORD!'
    ERROR_LOGIN_1: str = '[WARN/LOGIN] WRONG CAPTCHA SOLUTION, RETRYING...'
    ERROR_LOGIN_2: str = '[ERROR/LOGIN] SJTU JACCOUNT SYSTEM IS DOWN, PLEASE TRY AGAIN LATER.'
    ERROR_LOGIN_3: str = '[ERROR/LOGIN] ACCOUNT FROM DELEGATED AGENCY DOES NOT EXIST, PLEASE RETRY SELECTION.'
    ERROR_LOGIN_4: str = '[ERROR/LOGIN] ACCOUNT FROM DELEGATED AGENCY HAS EXPIRED, PLEASE RETRY SELECTION.'
    ERROR_LOGIN_5: str = '[ERROR/LOGIN] CURRENT DELEGATED AGENCY IS INVALID, PLEASE RETRY SELECTION.'
    ERROR_LOGIN_6: str = '[ERROR/LOGIN] YOU HAS CHANGED YOUR PASSWORD. CURRENT SESSION REQUIRE YOU TO RETRY LOGIN.'
    ERROR_LOGIN_7: str = '[ERROR/LOGIN] YOUR ACCOUNT IS CURRENTLY NOT LOG-ABLE.'
    ERROR_LOGIN_8: str = '[ERROR/LOGIN] LOGIN SESSION IS STALE. PLEASE RETRY.'
    ERROR_LOGIN_9: str = '[ERROR/LOGIN] QR CODE IS STALE. PLEASE REFRESH.'
    ERROR_LOGIN_10: str = '[ERROR/LOGIN] SJTU INFOPLUS TASKCENTER LOGIN IS STALE. RETRY LOGGIN IN TO THE APP.'
    ERROR_LOGIN_11: str = '[ERROR/LOGIN] PLEASE SCAN QR CODE BY WECHAT OR SJTU INFOPLUS TASKCENTER.'
    ERROR_LOGIN_12: str = '[ERROR/LOGIN] EXCEPTION WHILE FETCHING WECHAT LOGIN. PLEASE RETRY.'
    ERROR_LOGIN_13: str = '[ERROR/LOGIN] NO JACCOUNT BINDED TO WECHAT. PLEASE LOG IN BY USER NAME AND PASSWORD.'
    ERROR_LOGIN_DEFAULT: str = '[ERROR/LOGIN] UNDEFINED ERROR.'

    # C. Warning messages
    WARN_UNSOLVED: str = '[WARN/LOGIN] WEAK NETWORK CONNECTION, RETRYING...'
    WARN_WRONG_CAPTCHA: str = '[WARN/LOGIN] 10 TIMES ERROR ON CAPTCHA'

    # LOGIN SIMULATION PROCESS
    # 1. Directly raise an error if account name or password is empty.
    if jaccount_name == '' or jaccount_password == '':
        raise ValueError(ERROR_EMPTY_INPUT)

    # 2. Initialize a new requests session and perform a logout operation.
    session = requests.Session()
    session.get(URL_JAC_LOGOUT)

    # 3. Find a normal user page to be logged in with real headers from a client browser.
    #    Get the initial response with the headers above and get the fixed URL.
    headers: dict[str, str] = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    } # initial headers
    response = session.get(URL_JAC_LOG_IN_SIM, headers=headers)
    url_fix = response.url

    # 4. Concatenate the cookies (strings) from the response above in order to update headers for POST.
    JSESSIONID = session.cookies.get('JSESSIONID', domain='jaccount.sjtu.edu.cn', path='/jaccount')
    jaoauth2021 = session.cookies.get('jaoauth2021', domain='jaccount.sjtu.edu.cn', path='/')
    jajaccount2021 = session.cookies.get('jajaccount2021', domain='jaccount.sjtu.edu.cn', path='/')
    cookies_string: str = f'JSESSIONID={JSESSIONID}; jaoauth2021={jaoauth2021}; jajaccount2021={jajaccount2021}'
    # for key, value in session.cookies.items():
    #     cookies_string += key + '=' + value + '; '
    # cookies_string = cookies_string[0:-2]
    headers.update({
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookies_string,
        'Origin': 'https://jaccount.sjtu.edu.cn',
        'Referer': url_fix,
        'Sec-Fetch-Site': 'same-origin',
    }) # headers with jaccount session id
    
    # 5. More parameters are included in the response text. Use an HTML parser to get them. Then, insert the user name and the password.
    submit = form.form(response.text) # critical form submission values
    submit.update({
        'user': jaccount_name,
        'pass': jaccount_password,
    })

    # 6. Get the captcha and solve it with OCR techniques. 
    #    Try with limited times to avoid occasional process mistakes (which is unknown and still unsolved).
    for _ in range(10): # try maximum 10 times
        jaccount_captcha = captcha.captcha(submit['uuid'], cookies_string, url_fix).strip().replace(' ','') # get rid of spaces

        submit.update({
            'captcha': jaccount_captcha,
        })

        url = URL_JAC_POST_PREFIX
        for key, value in submit.items():
            url += key + '=' + value + '&'
        url = url[0:-1]
        response = session.post(url, headers=headers) # URL returned from ulogin (post prefix) is wrong.

        cookies: dict = session.cookies.get_dict()
        if (cookies.get('JAAuthCookie') is not None):
            cookies_fix: str = ''
            for key, value in cookies.items():
                cookies_fix += key + '=' + value + ';'
            headers.update({
                'Cookie': cookies_fix
            })
            # Get the right address.
            response = session.get(url_fix, headers=headers)
            return session # successful session
        else: 
            # Failed to get the specified cookie.
            # Show possible error messages.
            if '&err=' in response.url:
                if '&err=1' in response.url:
                    print(ERROR_LOGIN_1)
                elif '&err=0' in response.url:
                    print(ERROR_LOGIN_0)
                    return requests.Session() #
                elif '&err=2' in response.url:
                    print(ERROR_LOGIN_2)
                    quit(-2)
                elif '&err=3' in response.url:
                    print(ERROR_LOGIN_3)
                    quit(-3)
                elif '&err=4' in response.url:
                    print(ERROR_LOGIN_4)
                    quit(-4)
                elif '&err=5' in response.url:
                    print(ERROR_LOGIN_5)
                    quit(-5)
                elif '&err=6' in response.url:
                    print(ERROR_LOGIN_6)
                    return requests.Session() #
                elif '&err=7' in response.url:
                    print(ERROR_LOGIN_7)
                    quit(-7)
                elif '&err=8' in response.url:
                    print(ERROR_LOGIN_8)
                    return requests.Session() #
                elif '&err=9' in response.url:
                    print(ERROR_LOGIN_9)
                    return requests.Session() #
                elif '&err=10' in response.url: ####### TODO: FIX THE POSSIBLE CASES BELOW #######
                    print(ERROR_LOGIN_10)
                    return requests.Session() #
                elif '&err=11' in response.url:
                    print(ERROR_LOGIN_11)
                    return requests.Session() #
                elif '&err=12' in response.url:
                    print(ERROR_LOGIN_12)
                    return requests.Session() #
                elif '&err=13' in response.url:
                    print(ERROR_LOGIN_13)
                    quit(-13)
                else:
                    print(ERROR_LOGIN_DEFAULT)
            else:
                # An unsolved error about networking. Just try with more times.
                print(WARN_UNSOLVED)
                raise RuntimeError('NETWORKING ERROR')

            # Reassemble the cookies and retry.
            JSESSIONID = session.cookies.get('JSESSIONID', domain='jaccount.sjtu.edu.cn', path='/jaccount')
            jaoauth2021 = session.cookies.get('jaoauth2021', domain='jaccount.sjtu.edu.cn', path='/')
            jajaccount2021 = session.cookies.get('jajaccount2021', domain='jaccount.sjtu.edu.cn', path='/')
            cookies_string: str = f'JSESSIONID={JSESSIONID}; jaoauth2021={jaoauth2021}; jajaccount2021={jajaccount2021}'
    
    print(WARN_WRONG_CAPTCHA)
    return requests.Session()
