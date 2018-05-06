#coding:utf-8
import requests
import re
import os
from bs4 import BeautifulSoup
import time
import sys

class BnuzEol():
    """Summary of BnuzEol here.

    This class is to get the BnuzEol unfinished homework.
    It will display the unfinished homework.

    Attributes:
        timeout: all requests timeout
        url: to get the logintoken,the home of bnuzeol
        chinesename: students' real name
        username: BnuzEol username
        password: BnuzEol password
        logintoken: login BnuzEol essential params
        homeworknum: unfinished homework num
        homeworkname: all of the unfinished homework names
        id: all of the unfinished homework course id
        headers: the header of the request
        htmlcontent: in order to show the chinese correctly
        idnamedict: include unfinished homework id and name
        web: to keep the requests session
    """

    def __init__(self,timeout,url):
        self.timeout = timeout
        self.url = url
        self.chinesename = ''
        self.username = ''
        self.password = ''
        self.logintoken = ''
        self.homeworknum = 0
        self.homeworkname = ''
        self.id = ''
        self.headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        self.showcontent = []
        self.idnamedict = []
        self.web = requests.session()

    def __main__(self):
        #self.username = input("txt_loginName:")
        #self.password = input("txt_password:")
        self.username = '1501040222'
        self.password = '5555555'
        #self.GetUserPwd()
        self.LoginEol()

    def GetUserPwd(self):
        try:
            name = ''
            pwd = ''
            count = 1
            ABSPATH = None
            ABSPATH = os.path.abspath(sys.argv[0])
            ABSPATH = os.path.dirname(ABSPATH) + "/login.txt"
            if not os.path.exists(ABSPATH):
                print("Error!Yon don't have the login.txt.")
                input()
                os._exit(0)
            else:
                with open(ABSPATH) as f:
                    for line in f.readlines():
                        if count == 1:
                            name = line.strip()
                        else:
                            pwd = line.strip()
                        count += 1
                    self.username = name
                    self.password = pwd
        except ZeroDivisionError as e:
            print('except:', e)

    def GetLoginToken(self):
        try:
            logintokentext = self.web.get(self.url, headers=self.headers, timeout=self.timeout)
            if logintokentext.status_code == 200:
                soup = BeautifulSoup(logintokentext.text, "lxml")
                self.logintoken = soup.find('input', {'name':'logintoken'}).get('value')
                #print(self.logintoken)
            else:
                print('Get the params in error.')
        except ZeroDivisionError as e:
            print('except:', e)

    def LoginEol(self):
        try:
            self.GetLoginToken()
            loginurl = 'http://eol.bnuz.edu.cn/meol/loginCheck.do'
            payload = {
                'logintoken': self.logintoken,
                'IPT_LOGINUSERNAME': self.username,
                'IPT_LOGINPASSWORD': self.password
            }
            logintext = self.web.post(loginurl, data=payload, headers=self.headers, timeout=self.timeout)
            if logintext.status_code == 200:
                if logintext.url == 'http://eol.bnuz.edu.cn/meol/personal.do':
                    #print(logintext.text)
                    #print(logintext.url)
                    self.chinesename = (re.findall(r'class="login-text">\s*<span>(.*)</span>', logintext.text))[0]
                    print('爱学习的'+self.chinesename+'同学：')
                    self.GetHomeworkList()
                else:
                    print('Error username or password.')
                    input()
            else:
                print('Login in error.')

        except ZeroDivisionError as e:
            print('except:', e)

    def GetHomeworkList(self):
        try:
            homeworkurl = 'http://eol.bnuz.edu.cn/meol/welcomepage/student/interaction_reminder_v8.jsp'
            payload = {
                'r':'0.5123454851964999'
            }
            homeworktext = self.web.get(homeworkurl, headers=self.headers, data=payload, timeout=self.timeout)
            if homeworktext.status_code == 200:
                #print(homeworktext.text)
                num = re.findall(r'title="点击查看"><span>(\d)</span>门课程有待提交作业', homeworktext.text)
                if num:
                    #print(num[0])
                    self.homeworknum = num[0]
                    self.homeworkname = re.findall(r'hw"\s*target="_blank">\s*(.*)</a></li>', homeworktext.text)
                    print("你有" + " %s "%num[0] + "门课需要提交作业")
                    print(self.homeworkname)
                    print('\n')
                    self.id = re.findall(r'id=(\d{5})&t=hw', homeworktext.text)
                    #print(self.id)
                    self.idnamedict = dict(zip(self.id, self.homeworkname))
                    #print(self.idnamedict)
                    self.GetHomeworkDetail()
                else:
                    print("You don't have unfinished homework.")
            else:
                print('Get the unfinished homework in Error.')
            self.Loginout()
        except ZeroDivisionError as e:
            print('except:', e)

    def GetHomeworkDetail(self):
        try:
            lessonurl = 'http://eol.bnuz.edu.cn/meol/lesson/enter_course.jsp'
            #testid = ['18901']
            for i in self.id:
                payload = {
                    'lid': i,
                    't': 'hw'
                }
                lesson = self.web.get(lessonurl, headers=self.headers, params=payload, timeout=self.timeout)
                if lesson.status_code == 200:
                    homeworkdetailurl = 'http://eol.bnuz.edu.cn/meol/common/hw/student/hwtask.jsp'
                    homeworkdetailpayload = {
                        'tagbug': 'client',
                        'strStyle': 'new06'
                    }
                    homworkdetail = self.web.get(homeworkdetailurl, headers=self.headers, params=homeworkdetailpayload, timeout=self.timeout)

                    if homworkdetail.status_code == 200:
                        #print(homworkdetail.text)
                        hwid = re.findall(r'hwtask.view.jsp\?hwtid=(\d{4,5})', homworkdetail.text)
                        #print('hwid')
                        #print(hwid)
                        for newid in hwid:
                            hwenter = re.findall(r'%s"\s*class="enter"' % newid, homworkdetail.text)
                            if hwenter:
                                #print(hwenter)
                                #self.Loginout()
                                #print(newid)
                                homeworkdetailname = re.findall(r'%s"\s*class="infolist">(.*)\s*</a></td>' % newid, homworkdetail.text)
                                #print(homeworkdetailname[0])
                                #homeworkdetaildate = re.findall(r'%s\s*</a></td>\s*<td class="align_c">(.*)\s*</td>' % homeworkdetailname[0], homworkdetail.text)
                                homeworkdetaildate = re.findall(r'hwtid=%s"\s*class="infolist">.*\s*</a></td>\s*<td class="align_c">(.*)\s*</td>' % newid,homworkdetail.text)
                                #print(homeworkdetaildate)
                                detailcontent = "{0:\u3000<20s}{1:\u3000<20s}{2:\u3000<20s}".format(self.idnamedict[i], '\n作业名称:'+ homeworkdetailname[0], '\n截止时间:' + homeworkdetaildate[0])
                                #print(detailcontent)
                                self.showcontent.append(detailcontent)
                        time.sleep(1)
                    else:
                        print('Enter the homework detail text in error.')
                else:
                    print('Enter the course text in error.')
            self.status = 1
            #print(self.showcontent)
            for text in self.showcontent:
                print(text+'\n')
        except ZeroDivisionError as e:
            print('except:', e)

    def Loginout(self):
        try:
            loginouturl = 'http://eol.bnuz.edu.cn/meol/homepage/V8/include/logout.jsp'
            loginout = self.web.get(loginouturl, headers=self.headers)
            if loginout.status_code == 200:
                print('Log out successfully')
            else:
                print('Log out in error.')
        except ZeroDivisionError as e:
            print('except:', e)


if __name__ == '__main__':
    url = 'http://eol.bnuz.edu.cn/meol/index.do'
    timeout = 10
    bnuz = BnuzEol(timeout,url)
    bnuz.__main__()
    input()


