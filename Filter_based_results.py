'''

This module focuses on accepting values to certain fields and apply queries on them.
The objective is to:
1) fetch each field separately
2) check which fields have been selected and contains a value
3) for those fields only we run a query and store our results in a list
4) we append the list with distinct article_ids only
5) we return those article_ids by returning a json


'''

from dotenv import load_dotenv   
load_dotenv()
import os
import pymysql

a=os.environ.get('host')
b=os.environ.get('user')
c=os.environ.get('password')	
d=os.environ.get('database')


#This function stores all the info a dictionary and clears out the previous fields and values

def store(data):
	find={}
	if len(data["title"])!=0:
		find["title"]=data["title"]
	if len(data["auth"])!=0:
		find["auth"]=data["auth"]
	if len(data["domain"])!=0:
		find["domain"]=data["domain"].split(",")
	if len(data["subdomain"])!=0:
		find["subdomain"]=data["subdomain"].split(",")
	return find


def take_common(a,b):
	res=[]
	for i in a:
		if i in b:
			res.append(i)
	return res




#In this function we iterate over the selected fileds and fetch article_ids based on the values of those fields
def fetch(find):

	mydb=pymysql.connect(host=a,user=b,password=c,database=d,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

	mycursor=mydb.cursor()

	res1=[]
	res2=[]
	res3=[]
	res4=[]

	for i in find.keys():
		if i =='title':
			instruction='select article_id from iicblogdatabase.title_filter where title=%s'
			data=(find[i],)
			mycursor.execute(instruction,data)
			result=mycursor.fetchone()["article_id"]
			res1.append(result)


		if i =='auth':
			instruction='select article_id from iicblogdatabase.auth_filter where auth_name=%s'
			data=(find[i],)
			mycursor.execute(instruction,data)
			result=mycursor.fetchall()
			for j in result:
				res2.append(j["article_id"])
			

		if i =='domain':
			for j in find[i]:
				instruction="select article_id from iicblogdatabase.domain_filter where domain=%s"
				data=(j,)
				mycursor.execute(instruction,data)
				result=mycursor.fetchall()
				for k in result:
					if k["article_id"] not in res3:
						res3.append(k["article_id"])
			

		if i =='subdomain':
			for j in find[i]:
				instruction="select article_id from iicblogdatabase.subdom_filter where sub_domain=%s"
				data=(j,)
				mycursor.execute(instruction,data)
				result=mycursor.fetchall()
				for k in result:
					if k["article_id"] not in res4:
						res4.append(k["article_id"])

	mydb.close()
	
	if len(res1)==0 and len(res2)!=0:
		res5=res2.copy()
	elif len(res1)!=0 and len(res2)==0:
		res5=res1.copy()
	else:
		res5=take_common(res1,res2)
	

	if len(res3)==0 and len(res4)!=0:
		res6=res4.copy()
	elif len(res3)!=0 and len(res4)==0:
		res6=res3.copy()
	else:
		res6=take_common(res3,res4)


	res=[]
	if len(res5)==0 and len(res6)!=0:
		res=res6.copy()
	elif len(res5)!=0 and len(res6)==0:
		res=res5.copy()
	else:
		res=take_common(res5,res6)
	
	return res


def existing_data():
	
	mydb=pymysql.connect(host=a,user=b,password=c,database=d,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

	mycursor=mydb.cursor()


	data={}
	res1=[]
	res2=[]
	res3=[]
	res4=[]

	mycursor.execute("select distinct auth_name from iicblogdatabase.auth_filter;")
	result = mycursor.fetchall()
	print(result)
	
	for i in result:
		res1.append(i["auth_name"])
	data["authour_name"]=res1

	
	mycursor.execute("select distinct domain from iicblogdatabase.domain_filter;")
	result = mycursor.fetchall()
	for i in result:
		res2.append(i["domain"])
	data["domains"]=res2

	
	mycursor.execute("select distinct sub_domain from iicblogdatabase.subdom_filter;")
	result = mycursor.fetchall()
	for i in result:
		res3.append(i["sub_domain"])
	data["subdomains"]=res3

	
	mycursor.execute("select distinct title from iicblogdatabase.title_filter;")
	result = mycursor.fetchall()
	for i in result:
		res4.append(i["title"])
	data["titles"]=res4
	
	mydb.close()
	return data
	
#existing_data()