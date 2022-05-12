from bs4 import BeautifulSoup


def form(html: str) -> dict:
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # If you directly need 're' to find the captcha uuid
        # script = soup.select('div.login-layout')[0].script
        # uuid = re.compile('captcha\?uuid=(.*?)&', re.S).findall(script.text)[0]
        form_hidden = soup.select('form#form-input')[0].find_all('input')
        sid = form_hidden[0]['value']
        returl = form_hidden[1]['value']
        se = form_hidden[2]['value']
        v = form_hidden[3]['value']
        uuid = form_hidden[4]['value']
        client = form_hidden[5]['value']
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
