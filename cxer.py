import re
import requests
from mykit import *
from user import *
from course import Course


class CXer(User):

    login_url = "http://www.elearning.shu.edu.cn/login/to"
    check_url = "http://i.mooc.elearning.shu.edu.cn/space/index.shtml"
    courselist_url = "http://www.elearning.shu.edu.cn/courselist/study"
    api_url = "http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"

    def __init__(self, username, password):
        super().__init__(username, password)
        self.courses = []
        self.cur_course = ""

    def find_url(self, html):
        pat = 'action="(.*?)"'
        url = re.search(pat, html, re.S).group(1)
        return url

    def find_token(self, html):
        pat = 'name="(.*?)" value="(.*?)"'
        results = re.findall(pat, html, re.S)
        dic = {}
        for x in results:
            dic[x[0]] = x[1]
        return dic

    def login(self):
        print(f"{self.username} is trying to login...")
        r = self.sess.get(self.login_url)
        rlog(r)
        logind = self.sess.post(r.url, data={'username': self.username, 'password': self.enword})
        rlog(logind)
        finalurl = self.find_url(logind.text)
        if 'http' not in finalurl:
            print("Wrong username or password! Please try again.")
            return
        token = self.find_token(logind.text)
        finalr = self.sess.post(finalurl, data=token)

    def check(self):
        pat = 'personalName" title="(.*?)"'
        r = self.sess.get(self.check_url)
        if 'personalName' in r.text:
            name = re.search(pat, r.text, re.S).group(1)
            self.realname = name
            print(f"login success! {name}")
            return True
        else:
            print("Cannot login!")
            with open("FAILogin.html", "w", encoding="utf-8") as fs:
                fs.write(r.text)
            return False

    def get_courses(self):
        html = self.sess.get(self.courselist_url).text
        pat = r"href='(.*?studentcourse.*?)'.*?courseNameHtml\">\s*(.*?)\s*<"
        self.courses = re.findall(pat, html, re.S)
        if len(self.courses) == 0:
            print("Error! Cannot get courses")
        for x in enumerate(self.courses):
            print(x)
        return self.courses

    def choose_course(self, i=-1):
        if i != -1:
            print(f"You have chosen no.{i} course by default")
        else:
            i = int(input("Please choose one course:"))
        self.cur_course = Course(self.sess.get(self.courses[i][0]), self.courses[i][1], self.sess)
        print("Now you are visiting", self.cur_course)
        return self.cur_course
