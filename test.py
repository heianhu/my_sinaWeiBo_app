import requests
import time
import urllib.request
from bs4 import BeautifulSoup
def leap_year(y):
    '''判断是否是闰年'''
    if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
        return True
    else:
        return False

def days_in_month(y, m):
    '''判断每个月都有几天'''
    if m in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif m in [4, 6, 9, 11]:
        return 30
    else:
        if leap_year(y):
            return 29
        else:
            return 28

def days_this_year(year):
    '''判断今年共几天'''
    if leap_year(year):
        return 366
    else:
        return 365

def days_passed(year, month, day):
    '''判断今年过了几天'''
    m = 1
    days = 0
    while m < month:
        days += days_in_month(year, m)
        m += 1
    return days + day

def daysBetweenDates(year1, month1, day1, year2, month2, day2):
    '''判断两个时间相差了多久'''
    if year1 == year2:
        return days_passed(year2, month2, day2) - days_passed(year1, month1, day1)
    else:
        sum1 = 0
        y1 = year1
        while y1 < year2:
            sum1 += days_this_year(y1)
            y1 += 1
        return sum1 - days_passed(year1, month1, day1) + days_passed(year2, month2, day2)

def dao_ji_shi(now):
    '''返回 倒计时 的字符串'''
    biaoqing = ['[坏笑]', '[舔屏]', '[微笑]', '[生病]']
    holiday = {(2017, 10, 1): '国庆节', (2017, 4, 2): '清明节', (2017, 5, 1): '劳动节', (2017, 5, 28): '端午节',
               (2017, 10, 4): '中秋节'}
    pri = []
    strr = ''
    for a in holiday.keys():
        result = daysBetweenDates(now[0], now[1], now[2], a[0], a[1], a[2])
        if result <= 10:
            pri.append((holiday[a], result, biaoqing[0]))
        elif result <= 20:
            pri.append((holiday[a], result, biaoqing[1]))
        elif result <= 30:
            pri.append((holiday[a], result, biaoqing[2]))
        else:
            pri.append((holiday[a], result, biaoqing[3]))
    pri.sort(key=lambda e: e[1])
    for i in range(len(pri)):
        if pri[i][1] < 0:
            continue
        else:
            strr += '距离 {} 还有 {} 天{}\n'.format(pri[i][0], pri[i][1], pri[i][2])
            break
    return strr

def history_today_techonolegy(month,day):
    '''返回 历史上科技的今天 的字符串'''
    m=''
    d=''
    if month<10:
        m+='0'
    if day<10:
        d+='0'
    m+=str(month)
    d+=str(day)
    # 网址
    url = "http://www.lssdjt.com/a/keji/"+m+d+".htm"
    # 请求
    request = urllib.request.Request(url)
    # 爬取结果
    response = urllib.request.urlopen(request)
    data = response.read()

    soup = BeautifulSoup(data,"lxml")
    s = soup.select('div[class="p5 view"] p')
    ss = ''
    flag=1
    for i in s:
        ss += i.string[3:]
        ss+='\n'
    return ss

def history_today2(month,day):
    '''返回 发送首页重要的历史上的今天 的字符串'''
    m=''
    d=''
    if month<10:
        m+='0'
    if day<10:
        d+='0'
    m+=str(month)
    d+=str(day)
    # 网址
    url = "http://www.lssdjt.com/"
    # 请求
    request = urllib.request.Request(url)
    # 爬取结果
    response = urllib.request.urlopen(request)
    data = response.read()

    soup = BeautifulSoup(data) #如果添加过'lxml'库的话改为BeautifulSoup(data,"lxml")
    s = soup.select('a[target="_blank"] ')
    ss = ''
    flag=1
    for i in s[4:16:2]:
        if len(ss)+len(i.string)>125:
            break
        ss += i.string
        ss+='\n'
    return ss

def update_weibo(strr):
    '''微博发送接口'''
    # 发表文字微博的接口
    url_post_a_text = "https://api.weibo.com/2/statuses/update.json"
    # 构建POST参数
    playload = {
        "access_token": "", #此处填入自己申请应用时显示的，隐私问题将此删除
        "status": strr
    }
    # POST请求，发表文字微博
    r = requests.post(url_post_a_text, data=playload)

now=(time.localtime(time.time())[0],time.localtime(time.time())[1],time.localtime(time.time())[2])
strr=''
strr+=history_today2(now[1],now[2])
strr+=dao_ji_shi(now)
#print (strr)
update_weibo(strr)