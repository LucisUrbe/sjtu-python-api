# classtable.py - get class table for specified user and semester in json string format

import getpass
import requests
import time
from bs4 import BeautifulSoup


def classtable(session: requests.Session) -> str:
    Cookie: str = ''
    for key, value in session.cookies.items():
        Cookie += key + '=' + value + ';'
    print(Cookie)
    print(
        '[NOTE/CLASSTABLE] Here you volunteer to agree that the program will automatically read your sensitive information for data exchange.')
    headers: dict = {
        'Cookie': Cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'i.sjtu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    url: str = 'https://i.sjtu.edu.cn/xtgl/index_initMenu.html?jsdm=xs&_t=' + str(int(time.time()))  # 系统管理-角色代码：学生
    response = session.post(url, headers=headers)
    print(response.url)
    html: str = response.text
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    student_ID: str = soup.select('input#sessionUserKey')[0]['value']

    url: str = 'https://i.sjtu.edu.cn/kbcx/xskbcx_cxXsgrkb.html'  # 课表查询-学生课表查询-查询学生个人课表
    script: str = ''
    for tag in soup.find_all('a'):
        if '学生课表查询' in tag:
            script = tag['onclick']
            break
    if script == '':
        print('[ERROR/CLASSTABLE] INTERNAL ERROR. TELL THE DEVELOPER TO UPDATE THE SOFTWARE!')
        return {}
    gnmkdm: str = script.split('\'')[1]  # 功能模块代码, N2151
    url += '?gnmkdm=' + gnmkdm + '&layout=default&su=' + student_ID
    headers.update({
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': '*/*',
        'Origin': 'https://i.sjtu.edu.cn',
        'Referer': 'https://i.sjtu.edu.cn' + script.split('\'')[
            3] + '?gnmkdm=' + gnmkdm + '&layout=default&su=' + student_ID,
        'X-Requested-With': 'XMLHttpRequest'
    })
    data: dict = {
        'xnm': '2021',  # 学年码
        'xqm': '12',  # 学期码, 1 -> 3, 2 -> 12, 3 -> 16
        'kzlx': 'ck'  # 控制类型：窗口；打印: dy
    }
    json: str = requests.post(url, data, headers=headers).text
    return json


def main() -> None:
    from api.login import login as entry

    print('SJTU JACCOUNT SSO API DEMO')
    jaccount_name = input('<JACCOUNT> ')
    jaccount_password = getpass.getpass('<PASSWORD> ')
    session = entry(jaccount_name, jaccount_password)
    if session.cookies.items() == []:
        print('Error occurred while trying to log in. Did you input an invalid user name or password?')
    else:
        print('SJTU CLASSTABLE JSON FETCH DEMO')
        json: str = classtable(session)
        print('SUCCESS! Your class table for the current semester is shown below.')
        print(json)


if __name__ == '__main__':
    main()
