from cxer import CXer
from error import TooManyReqError, LoginError
from mykit import read2cols
import time
import argparse

usernames = []
passwords = []


def unattended(username, password, args):
    print("Will do predesigned work for ", username)
    try:
        cx = CXer(username, password)
        cx(args)
        # for i, c in enumerate(cx):
        #     if args.course and args.course not in c[1]:
        #         continue
        #     cs = cx[i]
        #     print(cs)
        #     cs(args)
    except TooManyReqError:
        time.sleep(60)
    except LoginError:
        time.sleep(3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AutoSHU')
    parser.add_argument("-u", "--username", help="username")
    parser.add_argument("-p", "--password", help="password")
    parser.add_argument("-f", "--filename", help="specify filename that stores username and password")
    parser.add_argument("--topic", action='store_true', help="password")
    parser.add_argument("--hw", action='store_true', help="show homeworks ddl")
    parser.add_argument("--course", help='specify course name keyword')
    args = parser.parse_args()
    args.filename = args.filename or 'key.txt'
    if args.username and args.password:
        unattended(args.username, args.password, args)
    else:
        read2cols(args.filename, usernames, passwords)
        for username, password in zip(usernames, passwords):
            unattended(username, password, args)
