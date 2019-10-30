import re
import time
import random
import json
import requests
#分牌
def number(puke): #获得数字
    list = [[] for i in range(15)]
    for i in puke:
        list[int(i[1:])].append(i)
    return list
#分颜色
def color(puke): #获得花色
    list = [[] for i in range(4)]
    for i in puke:
        if i[0] == '#':
            list[0].append(i)
        elif i[0] == '&':
            list[1].append(i)
        elif i[0] == '*':
            list[2].append(i)
        else:
            list[3].append(i)
    return list
#单张
def puke1(puke): #单张
    list = []
    num = number(puke)
    for i in range(15):
        if len(num[i]) == 1:
            list.append(num[i])
    return list
#对子
def puke2(puke): #对子
    list = []
    num = number(puke)
    for i in range(15):
        if len(num[i]) == 2:
            list.append(i)
    return list
#三条
def puke3(puke): #三条
    num = number(puke)
    for i in range(15):
        if len(num[i]) == 3:
            return i
    return 0
#炸弹
def puke4(puke): #炸弹
    num = number(puke)
    for i in range(15):
        if len(num[i]) == 4:
            return i
    return 0
#顺子
def puke5(puke):
    for i in range(1,5):
        if(int(puke[i][1:]) != int(puke[i-1][1:]) + 1):
            return 0
    return 1
#葫芦
def puke6(puke):
    if(len(puke2(puke)) == 1 and puke3(puke)!=0):
        return puke3(puke)
    else:
        return 0
#同花
def puke7(puke):
    for i in puke:
        x = i[0]
        break
    for i in puke:
        if (i[0] != x):
            return 0
    return 1
#同花顺
def puke8(puke):
    if(puke7(puke) == 1 and puke5(puke) ==1):
        return 1
    else:
        return 0
#算权值
def value(puke):
    if(puke8(puke) == 1): #同花顺
        return int(puke[4][1:]) + 161
    elif(puke4(puke) != 0): #炸弹
        return puke4(puke)+150
    elif(puke6(puke)!=0): #葫芦
        return 83+puke6(puke)
    elif(puke7(puke) == 1): #同花
        return int(puke[4][1:])+68
    elif(puke5(puke) == 1): #顺子
        return 63+int(puke[0][1:])
    elif(puke3(puke)!=0 and len(puke2(puke))==0): #三张
        return 50+puke3(puke)
    elif(len(puke2(puke)) == 2 ): #两对
        if(puke2(puke)[1] == puke2(puke)[0]+1):
            return 38+puke2(puke)[0]
        else:
            return puke2(puke)[1]+26
    elif(len(puke2(puke)) == 1): #一对
        return puke2(puke)[0]+13
    else:
        return int(puke[4][1:]) #单张
#算前墩权值
def value2(puke):
    if (puke[0][1:] == puke[1][1:] and puke[1][1:] == puke[2][1:]):
        return int(puke[0][1:]) + 51
    elif (len(puke2(puke)) != 0):
        return puke2(puke)[0] + 13
    else:
        return int(puke[2][1:])

def value3(puke):
    if(puke[0][1:] == puke[1][1:] and puke[1][1:] == puke[2][1:]):
        return int(puke[0][1:])+51
    elif(len(puke2(puke))!=0):
        return puke2(puke)[0]+26
    else:
        return int(puke[2][1:])
#排行榜
def rank():
    url=' http://api.revth.com/rank'
    headers={}
    soup=requests.get(url,headers).text
    print(soup)
#历史战绩
def history(token,id):
    url='http://api.revth.com/history'
    headers={'X-Auth-Token':token}
    data= {"page": 1, "limit": 1, "player_id": id}
    #x=json.dumps(data, ensure_ascii=False)
    soup=requests.request("GET",url,headers=headers,params=data).text
    print(soup)
#战局详细
def gameend(token,id):
    url='http://api.revth.com/history/'+str(id)
    headers = {"X-Auth-Token": token}
    soup = requests.request("GET",url,headers=headers).text
    print(soup)
#注册绑定
def regiseterAndBind(username,password,student_number,student_password):

    url = 'http://api.revth.com/auth/register2'
    form_data = {
    "username":username,
    "password": password,
    "student_number": student_number,
    "student_password": student_password
   }
    headers = {
    "Content-Type": 'application/json',
    }
    response = requests.post(url=url, headers=headers, data=json.dumps(form_data), verify=False);
    print(response.text)
#提交
def submit(token,gid, mycard):
    header={
        'X-Auth-Token': token,
        'Content-Type':'application/json'
    }
    url = 'http://api.revth.com/game/submit'
    data = {
        'id':gid,
        'card':mycard
    }
    x = json.dumps(data, ensure_ascii=False)
    print(x)
    response = requests.request('POST', url,headers=header , data=x).text
    print(response)
#登陆
def login(username,password):
    url = " http://api.revth.com/auth/login"
    data={
        'username':username,
        'password':password
    }
    json_data = json.dumps(data)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    print(response.text)
    p=re.compile('token":"(.+?)"')
    token=p.findall(response.text)[0]
    return token
#开局
def gameopen(token):
    url = "http://api.revth.com/game/open"
    headers = {'x-auth-token': token}
    response = requests.request("POST", url, headers=headers)
    dict_data = str(json.loads(response.text))
    p=re.compile("'id': (.+?),")
    id=p.findall(dict_data)
    p=re.compile("card': '(.+?)'")
    card=p.findall(dict_data)[0]
    #print(card)
    id.append(card)
    return id
def main(str):
    for i in range(100):
        #t1  = time.time()
        #card=['$2','$3','$4','$5','$6','$7','$8','$9','$10','$J','$Q','$K','$A','&2','&3','&4','&5','&6','&7','&8','&9','&10','&J','&Q','&K','&A','*2','*3','*4','*5','*6','*7','*8','*9','*10','*J','*Q','*K','*A','#2','#3','#4','#5','#6','#7','#8','#9','#10','#J','#Q','#K','#A']
        #str=random.sample(card,13)
        #str = ''.join(str)
        p = 0
        puke = []
        str = str.replace('A', '14')  # 做牌变化
        str = str.replace('J', '11')
        str = str.replace('Q', '12')
        str = str.replace('K', '13')
        str = str.replace(' ', '')
        for i in range(0, 13):  # 得到手牌
            res = re.match('((\$|\*|&|#)?(2|3|4|5|6|7|8|9|10|11|12|13|14)?)', str[p:])
            puke.append(res.group())
            p = p + res.end()
        print(puke)
        puke.sort(key=lambda x: int(x[1:])) #完成分牌
        list = []
        hd = {}
        k = 0
        ll = []
        #hd牌型
        for i1 in range(0,9):
            list.append(puke[i1])
            for i2 in range(i1+1, 10):
                list.append(puke[i2])
                for i3 in range(i2+1,11):
                    list.append(puke[i3])
                    for i4 in range(i3+1,12):
                        list.append(puke[i4])
                        for i5 in range(i4+1, 13):
                            list.append(puke[i5])
                            ll.append(list.copy())
                            hd[k] = value(list)
                            k+=1
                            list.pop()
                        list.pop()
                    list.pop()
                list.pop()
            list.pop()
        hdd = sorted(hd,key=hd.__getitem__,reverse=True) #所有后墩牌型且权值从大到小排序
        outp = []
        ll2 = []
        zd = {}
        qd = {}
        for i in hdd:
            maxv = hd[i]
            break
        for i in hdd: #找到权值最大的牌型
            pk = puke.copy()
            if(hd[i]*3 <= maxv):
                break
            for j in ll[i]:
              pk.remove(j)
            list = []
            for i1 in range(0, 8):
                list.append(pk[i1])
                for i2 in range(i1 + 1, 8):
                    list.append(pk[i2])
                    for i3 in range(i2 + 1, 8):
                        list.append(pk[i3])
                        for i4 in range(i3 + 1, 8):
                            list.append(pk[i4])
                            for i5 in range(i4 + 1, 8):
                                list.append(pk[i5])
                                v = value(list)
                                if(v >= hd[i]): #中墩比后墩大
                                    list.pop()
                                    continue
                                if(hd[i]+v<maxv-43):#权值不可能比最大
                                    list.pop()
                                    continue
                                pkk = pk.copy()
                                for j in list:
                                    pkk.remove(j)
                                v2 = value2(pkk)
                                if(v2>=v): #前墩比中墩大
                                    list.pop()
                                    continue
                                v2 = value3(pkk)
                                if(hd[i]+v+v2 > maxv):
                                    maxv = hd[i]+v+v2
                                    outp=[pkk.copy(), list.copy(), ll[i]]
                                list.pop()
                            list.pop()
                        list.pop()
                    list.pop()
                list.pop()
        mycard = [' '.join(i) for i in outp]
        for i in range(0,3):
            mycard[i] = mycard[i].replace('14', 'A')  # 做牌变化
            mycard[i] = mycard[i].replace('11', 'J')
            mycard[i] = mycard[i].replace('12', 'Q')
            mycard[i] = mycard[i].replace('13', 'K')
        return mycard
if __name__ == '__main__':
    username = '666'
    password = '100100'
    token = login(username, password)
    #while True:
    for i in range(50):
         hh = gameopen(token)
         gid = hh[0]
         puke = hh[1]
         print(puke)
         puke = main(puke)
         submit(token, gid, puke)
         history(token, 72)
         #time.sleep(5)

    #gameend(token, 55896)
