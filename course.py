import re
import requests
from mykit import *
from urllib.parse import *


class Course:
    def __init__(self, r, name, sess):
        pat_bbs = 'href="(/bbscircle/grouptopic.*?)"'
        self.sess = sess
        self.base = 'http://mooc1.elearning.shu.edu.cn'
        self.name = name
        self.home = r
        self.bbs_url = self.base + re.search(pat_bbs, r.text, re.S).group(1)
        self.topics = []

    def learn(self):
        return

    def getopics(self):
        print("topic url:", self.bbs_url)
        html = self.sess.get(self.bbs_url).text
        pat = '置顶.*?"(/bbscircle/gettopicdetail.*?)".*?<span.*?>(.*?)</span>'
        topics = re.findall(pat, html, re.S)
        for i in range(len(topics)):
            topics[i] = list(topics[i])
            topics[i][0] = self.base + topics[i][0]
            topics[i][1] = topics[i][1].strip()
        self.topics = topics
        for x in enumerate(self.topics):
            print(x)
        return self.topics

    def topic_files(self):
        pat = 'href="(/ueditor.*?)".*?title="(.*?)">'
        s = input("Trying to collect files. Enter the number(s) of your topic(s):")
        orders = parsein(s)
        print("You choose:", orders)
        for i in orders:
            url = self.topics[i][0]
            print(f"No.{i}:{url}")
            html = self.sess.get(url).text
            files = re.findall(pat, html, re.S)
            print(files)

    def check_reply(self, html):
        pat = 'ispraise.*?value="([01])"'
        ispraise = re.search(pat, html, re.S).group(1)
        if ispraise == '0':
            return True
        return False

    def add_praise(self, dic):
        url = self.base + "/bbscircle/addpraise"
        form = {
            "topicid": dic["topicid"],
            "cpi": dic["cpi"],
            "openc": dic["openc"]
        }
        self.sess.post(url, data=form)

    def send_replies(self):
        reply_url = self.base + '/bbscircle/addreply'
        s = input("Trying to send replies. ENTER the number(s) of your topic(s):")
        orders = parsein(s)
        for i in orders:
            print(f"Visiting NO.{i} topic...")
            url = self.topics[i][0]
            parsed = urlparse(url)
            print(f"parsed:{parsed}")
            qs = parsed.query
            print(f"qs:{qs}")
            dic = parse_qs(qs, keep_blank_values=True)
            print(dic)
            html = self.sess.get(url).text
            if not self.check_reply(html):
                print(f"You have visited NO.{i} topic{self.topics[i][1]}. PASS!")
                continue
            print(f"no.{i} topic{self.topics[i][1]} replies in below:")
            pat = 'replyfirstname">(.*?)</h3>'
            replies = re.findall(pat, html, re.S)
            if len(replies) == 0:
                print("No existing replies. Cannot copy:(")
                continue
            for reply in enumerate(replies):
                print(reply)
            myreply = replies[len(replies) - 1]  # .replace("<br>","")
            form = {
                "clazzid": dic["clazzid"],
                "topicid": dic["topicid"],
                "content": myreply,
                "files": "",
                "cpi": dic["cpi"][0],
                "ut": "s",
                "attachmentfile": "",
                "openc": dic["openc"],
                "showchooseclazzid": dic["showchooseclazzid"]
            }
            for k, v in form.items():
                form[k] = v[0] if isinstance(v, dict) else v
            print("form:", form)
            print("urlencode:", urlencode(form))
            sta = input("Are you sure to send reply?(y/n)")
            if 'y' in sta or 'Y' in sta:
                r = self.sess.post(reply_url, data=form)
                self.add_praise(form)
                print(f"NO.{i} topic replied!")

        print("All replies you chose have been sent! FINISHED!")
