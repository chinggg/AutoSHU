import re
import requests
from mykit import *
from user import User
from course import Course
from error import LoginError


class CXer(User):

    login_url = "https://oauth.shu.edu.cn/login/eyJ0aW1lc3RhbXAiOjE2MjAyMTI3MzkzMDQ5Mjc5MjQsInJlc3BvbnNlVHlwZSI6ImNvZGUiLCJjbGllbnRJZCI6IlAzV25LVW5lQk1EUndza05lTzh3Z283YiIsInNjb3BlIjoiMSIsInJlZGlyZWN0VXJpIjoiaHR0cDovL3NodS5meXNzby5jaGFveGluZy5jb20vc3NvL3NodSIsInN0YXRlIjoiIn0="
    check_url = "http://i.mooc.elearning.shu.edu.cn/space/index.shtml"
    courselist_url = "http://www.elearning.shu.edu.cn/courselist/study"
    api_url = "http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"

    def __init__(self, username, password):
        super().__init__(username, password)
        self.login()
        self.courses = self.get_courses()
        self.index = len(self.courses)
        self.cur_course = ""

    def __iter__(self):
        yield from self.courses

    def __getitem__(self, index):
        return self.courses[index]

    def __len__(self):
        return len(self.courses)

    def find_url(self, html):
        pat = 'action="(.*?)"'
        url = re.search(pat, html, re.S).group(1)
        return url

    def find_token(self, html):
        pat = 'name="(.*?)" value="(.*?)"'
        results = re.findall(pat, html, re.S)
        dic = {x[0]:x[1] for x in results}
        return dic

    def login(self):
        print(f"{self.username} is trying to login...")
        r = self.sess.post(self.login_url, data={'username': self.username, 'password': self.enword})
        fanya_url = self.find_url(r.text)
        if 'http' not in fanya_url:
            raise LoginError(self.username, self.password)
        token = self.find_token(r.text)
        finalr = self.sess.post(fanya_url, data=token)
        return self.check()

    def check(self):
        pat = 'personalName" title="(.*?)"'
        r = self.sess.get(self.check_url)
        if 'personalName' in r.text:
            name = re.search(pat, r.text, re.S).group(1)
            self.realname = name
            print(f"login success! {self.username} {name}")
            return True
        else:
            print("Cannot login!")
            with open("FAILogin.html", "w", encoding="utf-8") as f:
                f.write(r.text)
            raise LoginError(self.username, self.password)
            return False

    def get_courses(self):
        html = self.sess.get(self.courselist_url).text
        pat = r"href='(.*?studentcourse.*?)'.*?courseNameHtml\">\s*(.*?)\s*<"
        courses = re.findall(pat, html, re.S)
        if not courses:
            print("Error! Cannot get courses")
        for x in enumerate(courses):
            print(x)
        return courses

    def choose_course(self, i=-1):
        if i != -1:
            print(f"You have chosen no.{i} course by default")
        else:
            i = int(input("Please choose one course:"))
        self.cur_course = Course(self.sess.get(self.courses[i][0]), self.courses[i][1], self.sess)
        print("Now you are visiting", self.cur_course)
        return self.cur_course

if __name__ == '__main__':
    cxer = CXer(19129999, 'WillThrowError')
    for x in enumerate(cxer):
        print(x)
