'''
  	1. 功能说明
	  	【1】用户可以登录和注册
		    	* 登录凭借用户名和密码登录
				* 注册要求用户必须填写用户名，密码，其他内容自定
				* 用户名要求不能重复
				* 要求用户信息能够长期保存
		
		【2】可以通过基本的图形界面print以提示客户端输入。
		    	* 程序分为服务端和客户端两部分
				* 客户端通过print打印简单界面输入命令发起请求
				* 服务端主要负责逻辑数据处理
				* 启动服务端后应该能满足多个客户端同时操作
		
		【3】客户端启动后即进入一级界面，包含如下功能：
		     
				 登录    注册    退出

				 * 退出后即退出该软件
				 * 登录成功即进入二级界面，失败回到一级界面
				 * 注册成功可以回到一级界面继续登录，也可以直接用注册用户进入二级界面
		
		【4】用户登录后进入二级界面，功能如下：
		     
				 查单词    历史记录    注销

				 * 选择注销则回到一级界面
				 * 查单词：循环输入单词，得到单词解释，输入特殊符号退出单词查询状态
				 * 历史记录：查询当前用户的查词记录，要求记录包含name   word   time。可以查看所有记录或者前10条均可。
	
	2. 单词本说明

	  	【1】 特点 : 1. 每个单词一定占一行
		            2. 单词按照从小到大顺序排列
					3. 单词和解释之间一定有空格
		
		【2】 查词说明 ： 1. 直接使用单词本查询（文本操作）
						2. 先将单词存入数据库，然后通过数据库查询。（数据库操作）
		
  	3. 操作步骤
	   
		【1】 确定并发方案？ 确定套接字使用？ 确定具体细节？
          		使用文件查询还是数据库？
					
					* fork 多进程 ，tcp套接字
					* 注册后回到一级界面，历史记录显示最近10条
					* 文本直接查询

	
		【2】 建立数据库 ： 建立几个表，表关系，表字段及类型
		      * 想办法将单词导入数据库
					
					用户表 ： id   name   passwd 
					历史记录：id   name   word    time 
					单词存储：id   word   mean

					1. 创建数据库：
					  create database dict default charset=utf8;

					2. 创建用户表：
						create table user (id int primary key auto_increment,name varchar(32) not null,passwd varchar(16) default '000000');
          
					3. 创建历史记录表：
						create table hist (id int primary key auto_increment,name varchar(32) not null,word varchar(32) not null,time varchar(64));
					
					4. 创建单词表：
						create table words (id int primary key auto_increment,word varchar(32),mean text);


		【3】 结构设计：即如何封装，客户端和服务端工作流程。具体项目有几个功能模块。

					* 函数封装
					* 客户端启动--》进入一级界面--》登录--》二级界面--》具体请求--》展示内容
					* 服务端循环接收请求--》处理请求--》将数据发送给客户端
					* 功能模块：登录，注册，查询单词，历史记录


		【4】 完成通信的搭建

		【5】 分析具体通能，逐个模块实现
			
		  
			1、注册
         　　客户端：*输入注册信息
					*将信息发送给服务端
                    *得到服务器反馈

         　　服务端：*接收请求
					*判断是否允许注册
					*反馈结果给客户端
					*如果可以注册则插入数据库
       
				2. 登录
						客户端： * 输入用户名密码
								* 将信息发送给服务器
								* 得到服务端反馈
								* 如果登录成功进入二级界面
						
						服务端： * 接收请求
								* 判断是否允许登录
								* 反馈结果

				3. 查词
				    客户端 ： * 输入查询单词
							* 发送请求给服务端
							* 获取结果
						
						服务端 ： * 接收请求
								* 查找单词
								* 将查询结果发送给客户端
								* 插入历史记录

				4. 历史记录




将查询字典 插入数据库

'''
import pymysql

f = open('dict.txt')
db = pymysql.connect('localhost','root','123456','dict')

cursor = db.cursor()

for line in f:#一行行的写
    tmp = line.split(' ')
    word = tmp[0]
    mean = ' '.join(tmp[1:]).strip()#不考虑解释中间有空格的情况
    sql = 'insert into words(word,mean) values ("%s","%s")'%(word,mean)


    try:
        cursor.execute(sql)
        db.commit()
    except Exception:
        db.rollback()
f.close()

