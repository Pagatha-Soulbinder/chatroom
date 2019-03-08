'''
网络字典项目 客户端

        1、注册
    　　         *输入注册信息
                *将信息发送给服务端
                *得到服务器反馈
        2. 登录
                * 输入用户名密码
                * 将信息发送给服务器
                * 得到服务端反馈
                * 如果登录成功进入二级界面
        3. 查词
                * 输入查询单词
                * 发送请求给服务端
                * 获取结果
        4. 历史记录

'''


from socket import *
import sys
import getpass
def main():
    if len(sys.argv)<3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return

    while True:
        print('''
        ============welcome===========
        --1.注册   2.登录       3.退出--
        ==============================
        ''')
        try:
            cmd = int(input('输入选项:'))
        except Exception as e:
            print("命令错误")
            continue

        if cmd not in [1,2,3]:
            print("请输入正确选项")
            continue
        elif cmd == 1 :
            do_register(s)
        elif cmd == 2 :
            do_login(s)
        elif cmd ==3 :
            s.send(b'E')
            sys.exit("谢谢使用")




def do_login(s):
    name = input("User:")
    passwd = getpass.getpass()
    msg = "L %s %s"%(name,passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data =='OK':
        print("登录成功")
        login(s,name)#注意思考为什么传name

    else:
        print("登陆失败")

def login(s,name):
    while True:
        print('''
        ============查询界面===========
        --1.查词   2.历史记录    3.注销--
        ==============================
        ''')
        try:
            cmd = int(input('输入选项:'))
        except Exception as e:
            print("命令错误")
            continue

        if cmd not in [1,2,3]:
            print("请输入正确选项")
            continue
        elif cmd == 1 :
            do_query(s,name)
        elif cmd == 2 :
            do_hist(s,name)
        elif cmd ==3 :  
            return#回到一级界面

def do_hist(s,name):
    msg = "H %s"%name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data =="OK":
        while True:#按照约定循环接收直到##
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    
    else:
        print("没有历史记录")


def do_query(s,name):
    while True:
        word = input("单词：")
        if word == '##':
            break
        msg = 'Q %s %s'%(name,word)
        s.send(msg.encode())
        #返回值可能是单词解释，也可能找不到
        data = s.recv(2048).decode()
        print(data)












def do_register(s):
    while True:
        name = input("User:")
        passwd = getpass.getpass()
        passwd1 = getpass.getpass("Again:")
        if (' ' in name) or (' 'in passwd):
            print("用户名密码许有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        
        msg = 'R %s %s'%(name,passwd)
        #发送请求，如发送信息较多可以用struct模块打包
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            # login(s,name)#注册成功进入二级界面
        elif data == 'EXISTS':
            print("用户已存在")
        else:
            print("注册失败,",data)   
        return



if __name__ =='__main__':
    main()