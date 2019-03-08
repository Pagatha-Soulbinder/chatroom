'''
 2】 建立数据库 ： 建立几个表，表关系，表字段及类型
		      * 想办法将单词导入数据库
			
					用户表 ： id   name   passwd 
					历史记录：id   name（此处不单写name会导致频繁联结查询）   word    time 
					单词存储：id   word   mean


'''



create database dict default charset = utf8;

-- 创建用户表
create table user (
    id int primary key auto_increment,
    name varchar(32) not null,
    passwd varchar(16) default '000000'
)default charset = utf8;

-- 创建历史记录表
create table hist(
    id int primary key auto_increment,
    name varchar(32) not null,
    word varchar(32) not null,
    time varchar(64)
)default charset = utf8;

-- 创建单词存储表
create table words(
    id int primary key auto_increment,
    word varchar(32),-- 单词
    mean text -- 解释
)default charset = utf8;


