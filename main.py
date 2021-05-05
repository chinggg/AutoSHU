from cxer import *
from course import *
from time import sleep

usernames = []
passwords = []


# You can do predesigned tasks here
def unattended():
    for i in range(len(usernames)):
        username = usernames[i]
        password = passwords[i]
        try:
            cx = CXer(username, password)
            for i, c in enumerate(cx):
                    cx.choose_course(i)
                    cx.cur_course.getopics()
                    cx.cur_course.topic_files()
        except LoginError:
            sleep(3)
            continue


# You can do what you want by calling functions manually
def init(cur_id):
    for x in enumerate(usernames):
        print(x)
    if cur_id == -1:
        cur_id = int(input("Please choose one user:"))
    cx = CXer(usernames[cur_id], passwords[cur_id])
    cx.login()
    if cx.check():
        cx.get_courses()
    else:
        print()
        return False
    cx.choose_course()
    cx.cur_course.getopics()
    cx.cur_course.get_mates()
    cx.cur_course.topic_files()
    cx.cur_course.send_replies()


def main():
    cur_id = -1
    read2cols('key.txt', usernames, passwords)
    unattended()
    while True:
        init(cur_id)
        for x in enumerate(usernames):
            print(x)
        sta = int(input("Current work has finished, please enter new number to continue(-1 to exit):"))
        if sta == -1:
            return
        else:
            init(sta)


if __name__ == '__main__':
    main()
