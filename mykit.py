import json

# Please ensure each line has exactly one header
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Proxy-Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}


def headers2json(headers):
    dic = {}
    lines = headers.split('\n')
    for line in lines:
        if line.strip() == '':
            continue
        strs = line.split(':', 1)
        dic[strs[0].strip()] = strs[1].strip()
    print(json.dumps(dic))
    with open("headers.json", "w") as file:
        json.dump(dic, file)


# eg. 1-3,6-7,8
# 1.split ',' get list1 of str(s) 'a-b' or 'x'
# 2.foreach str in list1, split '-' get list2 containing two chars or just one
# 3.check len(list2)
def parsein(s):
    result = []
    list1 = s.split(',')
    for seq in list1:
        list2 = seq.split('-')
        if len(list2) == 2:
            a = int(list2[0])
            b = int(list2[1])
            for i in range(a, b + 1):
                result.append(i)
        elif len(list2) == 1:
            result.append(int(list2[0]))
        else:
            print("Error! Please check your input")
    return result


# read pairs of values from a file, split by space, '#' to ignore
def read2cols(filename, c1, c2):
    with open(filename, 'r', encoding='utf-8') as fs:
        lines = fs.readlines()
        for s in lines:
            s = s.strip()
            lst = s.split(' ')
            if '#' in lst[0]:
                continue
            c1.append(lst[0].strip())
            c2.append(lst[1].strip())


def rlog(r):
    print(r, r.url)
    print("Response Headers:", r.headers)
    print("History list:", r.history)
    for h in r.history:
        print("Target Url:", h.url)
        print("Response Headers:", h.headers)
    print("")
    # print("Response Text",r.text)


if __name__ == '__main__':
    print("This is just a collection of my pieces of code.")
