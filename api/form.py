from bs4 import BeautifulSoup


def form(html: str) -> dict:
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # If you directly need 're' to find the captcha uuid
        #script = soup.select('div.login-layout')[0].script
        #uuid = re.compile('captcha\?uuid=(.*?)&', re.S).findall(script.text)[0]
        form = soup.select('form#form-input')[0].find_all('input')
        sid = form[0]['value']
        returl = form[1]['value']
        se = form[2]['value']
        v = form[3]['value']
        uuid = form[4]['value']
        client = form[5]['value']
        return {
            'sid': sid,
            'returl': returl,
            'se': se,
            'v': v,
            'uuid': uuid,
            'client': client
        }
    except Exception as error:
        print('[ERROR/FORM]', error)
