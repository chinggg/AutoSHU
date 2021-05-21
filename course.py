import re
import requests
from mykit import *
from urllib.parse import *


class Course:

    pat_stat = re.compile('href="(/moocAnalysis.*?)"', re.S)
    pat_bbs = re.compile('href="(/bbscircle/grouptopic.*?)"', re.S)
    pat_hw = re.compile('data="(/work/getAllWork.*?)"', re.S)
    base_url = 'http://mooc1.elearning.shu.edu.cn'
    mate_url = 'http://mooc1.elearning.shu.edu.cn/moocAnalysis/classmateList'

    def __init__(self, url='', name='', sess=None):
        self.sess = sess
        self.name = name
        self.r = self.sess.get(url)
        self.params = my_urlparser(url)
        self.stat_url = self.base_url + self.pat_stat.search(self.r.text).group(1)
        self.bbs_url = self.base_url + self.pat_bbs.search(self.r.text).group(1)
        self.hw_url = self.base_url + self.pat_hw.search(self.r.text).group(1)
        self.topics = []
        self.hws = []
        self.mates = set()

    def __str__(self):
        return (
            f'\n课程名称: {self.name}\n'
            f'课程主页: {self.r.url}\n'
            f'课程参数: {self.params}\n'
            f'统计页面: {self.stat_url}\n'
            f'讨论页面: {self.bbs_url}\n'
        )

    def get_mates(self):
        pat_sname = re.compile(r'default">\s+(.*?)\s+</a>', re.S)
        pat_lst = re.compile(r'href="(/moocAnalysis/classmateList.*?)"', re.S)
        pat_tot = re.compile('总人数\((.*?)\)', re.S)
        stat_html = self.sess.get(self.stat_url).text
        tot = int(pat_tot.search(stat_html).group(1))
        if len(self.mates) >= tot-1:
            print("同学人数仍为",len(self.mates))
            return self.mates
        url = self.base_url + pat_lst.search(stat_html).group(1)
        form = my_urlparser(url)
        for i in range(1,5):
            form["classmateNUM"] = i
            html = self.sess.post(self.mate_url, data=form).text
            self.mates.update(pat_sname.findall(html))
        print(self.mates)
        print("同学人数",len(self.mates))
        return self.mates

    def getopics(self):
        print("topic url:", self.bbs_url)
        html = self.sess.get(self.bbs_url).text
        pat = re.compile("openDetail\('(.*?)'\).*?<span.*?>(\S+)<", re.S)
        # pat = '置顶.*?"(/bbscircle/gettopicdetail.*?)".*?<span.*?>(.*?)</span>'
        topics = pat.findall(html)
        for i in range(len(topics)):
            topics[i] = list(topics[i])
            topics[i][0] = self.base_url + topics[i][0]
            topics[i][1] = topics[i][1].strip()
        self.topics = topics
        for x in enumerate(self.topics):
            print(x)
        return self.topics

    def topic_files(self):
        pat = 'href="(/ueditor.*?)".*?title="(.*?)">'
        s = input("Trying to collect files. Enter the number(s) of your topic(s):")
        if not s:
            return None
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
        url = self.base_url + "/bbscircle/addpraise"
        form = {
            "topicId": dic["topicId"],
            "cpi": dic["cpi"],
            "openc": dic["openc"]
        }
        self.sess.post(url, data=form)

    def send_replies(self):
        reply_url = self.base_url + '/bbscircle/addreply'
        s = input("Trying to send replies. ENTER the number(s) of your topic(s):")
        orders = parsein(s)
        for i in orders:
            print(f"Visiting NO.{i} topic...")
            url = self.topics[i][0]
            # parsed = urlparse(url)
            # print(f"parsed:{parsed}")
            # qs = parsed.query
            # print(f"qs:{qs}")
            dic = my_urlparser(url)
            print(dic)
            html = self.sess.get(url).text
            if not self.check_reply(html):
                print(f"You have visited NO.{i} topic{self.topics[i][1]}. PASS!")
                continue
            print(f"no.{i} topic{self.topics[i][1]} replies in below:")
            pat = 'replyfirstname">(.*?)</h3>'
            replies = re.findall(pat, html, re.S)
            if not replies:
                print("No existing replies. Cannot copy:(")
                continue
            for reply in enumerate(replies):
                print(reply)
            myreply = replies[len(replies) - 1]  # .replace("<br>","")
            form = {
                "clazzid": dic["clazzid"],
                "topicId": dic["topicid"],
                "content": myreply,
                "files": "",
                "cpi": dic["cpi"],
                "ut": "s",
                "attachmentfile": "",
                "openc": dic["openc"],
                "showChooseClazzId": dic["showChooseClazzId"]
            }
            # for k, v in form.items():
                # form[k] = v[0] if isinstance(v, dict) else v
            print("form:", form)
            print("urlencode:", urlencode(form))
            sta = input("Are you sure to send reply?(y/n)")
            if 'y' in sta or 'Y' in sta:
                r = self.sess.post(reply_url, data=form)
                if 'error' in r.text:
                    print("Fail to reply, please do it yourself :(")
                else:
                    self.add_praise(form)
                    print(f"NO.{i} topic replied and praised!")

        print("All replies you chose have been sent! FINISHED!")

    def get_hw(self):
        pat = re.compile('<a.*?href="/work.*?title="\s*(.*?)\s*".*?截止时间：</span>\s*(.*?)\s*</span>.*?作业状态.*?<strong>\s*(.*?)\s*</strong>', re.S)
        html = self.sess.get(self.hw_url).text
        hws = pat.findall(html)
        print(hws)
