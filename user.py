import requests
import rsa
import base64
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-us,en;q=0.9",
        "proxy-connection": "keep-alive",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
}

# Thanks to panghaibin
def enc(password):
    key_str = '''-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDl/aCgRl9f/4ON9MewoVnV58OL
    OU2ALBi2FKc5yIsfSpivKxe7A6FitJjHva3WpM7gvVOinMehp6if2UNIkbaN+plW
    f5IwqEVxsNZpeixc4GsbY9dXEk3WtRjwGSyDLySzEESH/kpJVoxO7ijRYqU+2oSR
    wTBNePOk1H+LRQokgQIDAQAB
    -----END PUBLIC KEY-----'''
    pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(key_str.encode('utf-8'))
    crypto = base64.b64encode(rsa.encrypt(password.encode('utf-8'), pub_key)).decode()
    return crypto

retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)

class User:
    def __init__(self, username, password):
        self.sess = requests.Session()
        self.sess.headers.update(HEADERS)
        self.sess.mount('http://', adapter)
        self.sess.mount('https://', adapter)
        self.username = str(username)
        self.password = str(password)
        self.enword = enc(password)
        self.realname = 'NULL'

    def __str__(self):
        return self.username

