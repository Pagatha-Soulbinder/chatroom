'''
TCP fork多进程
网络字典项目 服务端

实现步骤
    1 定义全局变量  ,导入相应模块
    2 以fork多进程模型搭建网络连接
    3 在子进程中处理客户端请求（封装操作函数）
        a 操作函数中与服务端做好约定 按收到的信息分别作出相应处理注册，登录，查询历史记录，查词，退出等请求（继续封装

*为了复习以往知识点，查寻单词采取文本模式，不用数据库
'''


from socket import *
import pymysql
import os,sys
import time
import signal
from pymongo import MongoClient

if len(sys.argv) < 3:#终端输入的参数小于3个
    print("""Start as:
    python3 dict_server.py 0.0.0.0 8000
    """)
    sys.exit(0)

#定义全局变量   
HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (HOST,PORT)
DICT_TEXT = './dict.txt'#单词本位置
CIPHER = 1
#搭建网络连接
def main():
    #连接数据库(在子进程创建游标，可以防止进程间互相影响写入)
    db = pymysql.connect('localhost','root','123456','dict')
    #创建套接字
    s = socket()
    # s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)#工作中不会频繁启动服务器
    s.bind(ADDR)
    s.listen(5)

    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    conn = MongoClient("localhost",27017,connect=False)
    mongoDb = conn.dir
    # myset = db.word


    






    #创建多线程之前先监听
    while True:
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        pid = os.fork()
        if pid == 0:
            s.close()
            if CIPHER == 1:
                do_child_byMongo(c,mongoDb)
                
            elif CIPHER == 0:
                do_child(c,db)#子进程中处理客户端请求


            sys.exit()
        else:
            c.close()

# 子进程中处理客户端请求
def do_child(c,db):
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if not data or data[0] == "E":
            c.close()
            sys.exit()
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_hist(c,db,data)

def do_child_byMongo(c,mongoDb):
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if not data or data[0] == "E":
            c.close()
            sys.exit()
        elif data[0] == 'R':
            do_register_mongo(c,mongoDb,data)
        elif data[0] == 'L':
            do_login_mongo(c,mongoDb,data)
        elif data[0] == 'Q':
            do_query_mongo(c,mongoDb,data)
        elif data[0] == 'H':
            do_hist_mongo(c,mongoDb,data)    














def do_hist(c,db,data):
    name = data.split(' ')[1]
    cursor = db.cursor()
    #只查找最近10条
    sql = 'select * from hist where name = "%s" order by id desc limit 10'%name
    cursor.execute(sql)
    r = cursor.fetchall()#获取全部10条记录
    if not r:
        c.send(b'FAIL')
        return
    else:
        c.send(b'OK')
        time.sleep(0.1)
    for i in r:
        msg = "%s      %s       %s"%(i[1],i[2],i[3])#取后三项name word time
        c.send(msg.encode())
        time.sleep(0.1)#避免沾包
    c.send(b"##")   #按照约定 发送完毕的信号

def do_hist_mongo(c,mongoDb,data):
    myset = mongoDb.hist
    # .aggregate({$project:{_id:0,Name:'$name',Age:'$age'}})
    # res = myset.aggregate({'$project':{'wordhist':'$word'}})
    name = data.split(' ')[1]
    cursor = myset.find({'name':name})

    # his_list = myset.distinct('wordhist')
    a = ''
    # for i in his_list:
    #     a+=i+','
    
    for i in cursor:
        a += i['word_histery'] + ' '


    c.send(b'OK')
    time.sleep(0.1)
    c.send(a.encode())



def do_query(c,db,data):
    l = data.split(" ")
    name = l[1]
    word = l[2]
    f = open(DICT_TEXT)
    #插入历史记录
    cursor = db.cursor()
    tm = time.ctime()
    sql = 'insert into hist(name,word,time) values\
            ("%s","%s","%s")'%(name,word,tm)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("insert Error")
        db.rollback()


    
    for line in f:#遍历单词本
        tmp = line.split(' ')[0]#提取单词
        if tmp > word:
            break
        elif tmp == word:
            c.send(line.encode())
            f.close()
            return
    #注意！有用意！        
    c.send("没有找到该单词".encode())#如果单词是zzzz 这样遍历完也发送未找到该单词
    f.close()

def do_query_mongo(c,mongoDb,data):
    l = data.split(" ")
    name = l[1]
    word = l[2]    
    myset_ins = mongoDb.hist
    myset_ins.insert_one({'name':name,'word_histery':word})
    myset_que = mongoDb.word
    
    res = myset_que.find_one({'word':word})
    if res is None:
        c.send(b'None')
    c.send(res['mean'].encode())

def do_login(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = "select * from user where name = '%s' and passwd = '%s'"%(name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r == None:
        c.send(b"FAIL")
    else:
        c.send(b"OK")

def do_login_mongo(c,mongoDb,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]   
    myset = mongoDb.user
    result = myset.find_one({'name':name,'passwd':passwd},{})
    if result == None:
        c.send(b"FAIL")
    else:
        c.send(b"OK")        

def do_register(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()#直接传游标怕进程之间相互影响
    sql = "select * from user where name = '%s'"%name
    cursor.execute(sql)
    r= cursor.fetchone()#只获取一条数据
    if r != None:
        c.send(b'EXISTS')
        return
    #插入用户
    sql = "insert into user (name,passwd) values\
            ('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback()
        c.send(b'FAIL')


def do_register_mongo(c,mongoDb,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    myset = mongoDb.user
    
    result = myset.find_one({'name':name},{})
    if result != None:

        c.send(b'EXISTS')
        return
    myset.insert_one({'name':name,'passwd':passwd})
    c.send(b'OK')






if __name__ =='__main__':
    main()