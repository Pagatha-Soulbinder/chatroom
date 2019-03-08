# from pymongo import MongoClient
# import bson.binary
# f = open('dict.txt')
# conn = MongoClient("localhost",27017)
# db = conn.dic
# myset = db.word

#一行行的写
# for line in f:
# 	tmp = line.split(' ')
# 	word = str(tmp[0])
# 	#不考虑解释中间有空格的情况
# 	mean = ' '.join(tmp[1:]).strip()
# 	print(word,mean)
# 	a = {'word':word,'mean':mean}
# 	myset.insert_one(a)
	

# f.close()

from pymongo import MongoClient
f = open('dict.txt')
conn = MongoClient("localhost",27017)
db = conn.dir
myset = db.word
a = {}
myset.delete_many({})
#一行行的写
for line in f:

	tmp = line.split(' ')
	word = tmp[0].replace('.',' ')
	mean = ' '.join(tmp[1:]).strip()#不考虑解释中间有空格的情况
	# print(word,mean)

	myset.insert_one({'word':word,'mean':mean})
	# a[word]=mean
	
	
# print(a)





# 	a[word]=mean
# myset.insert_many(a)
	

f.close()

