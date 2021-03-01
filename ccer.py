from user import *
import re
import requests

class CCer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.login_url = "http://cloudlab.hoc.ccshu.net/virtual/loginsubmit"
        self.up_url = "http://cloudlab.hoc.ccshu.net/virtual/lab/up"
        self.lab7_url = "http://cloudlab.hoc.ccshu.net/virtual/lab/d08ee5b3-148b-4794-8ced-743b616157dc"
        self.vps = ()
        
    def login(self):
        print(f"{self.username} is trying to login...")
        self.sess.post(self.login_url, data={'number':self.username, 'password':self.password})
        r = self.sess.get(self.lab7_url)
        pat = "li>欢迎您，(.*?)</li>"
        name = re.search(pat, r.text, re.S).group(1)
        if name != '':
            print(f'{name}登录成功')
        else:
            print('登录失败!')
            print(r.text)
        
    def up(self):
        print(f"{self.username} is tring to up...")
        self.sess.post(self.up_url, data={'id':'9e0f9277-619a-4440-99ab-2a9ca5a79e1e'})
        pat = "IP：(.*?)，登录帐号：root，登录密码：(.*?)<"
        r = self.sess.get(self.lab7_url)
        self.vps = re.search(pat, r.text, re.S).group(0)
        print(self.vps)
        
if __name__ == '__main__':
    ccer = CCer()
    ccer.login();
    ccer.up();
