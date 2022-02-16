#!python
# demo.py - this is the main process (demo)
import getpass


def main() -> None:
    from api.login import login as entry

    print('SJTU JACCOUNT SSO API DEMO')
    jaccount_name = input('<JACCOUNT> ')
    jaccount_password = getpass.getpass('<PASSWORD> ')
    cookies = entry(jaccount_name, jaccount_password)
    if cookies == {}:
        print('Error occurred while trying to log in. Did you input an invalid user name or password?')
    else:
        print('Success! Your secret cookie key is:')
        print(cookies.get('JAAuthCookie'))
        print('Do not tell anyone!')

if __name__ == '__main__':
    main()
