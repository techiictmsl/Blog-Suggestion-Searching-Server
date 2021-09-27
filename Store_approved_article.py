'''
This module will do multiple tasks after an unpublised article has been approved by the admin (IIC Content team)

1) On approval, the status of the unpublised article would change from 0 to 1

2) In the Approved_articles table create a record of the article with the same details and remove that article from unpublished_articles table.
   This table will help us with fetching details for articles visualised as tiles or slabs in the landing page or the suggestions section.

3) Our next task is to append the same article into individual tables on auth_name, write_date, domains, subdomain, title where each field is mapped with the article id
   These tables are being created to use the filter based searching.

4) We will not declare any PKs in these auxillary tables because there might be multiple entries and also to avoid storing list objects 

'''

from dotenv import load_dotenv   
load_dotenv()
import os
import pymysql

a=os.environ.get('host')
b=os.environ.get('user')
c=os.environ.get('password')	
d=os.environ.get('database')



def store_into_all(article_id):

	mydb=pymysql.connect(host=a,user=b,password=c,database=d,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

	mycursor=mydb.cursor()

	#STEP 1: CHANGING THE STATUS OF AN UNPUBLISHED ARTICLE ON APPROVAL

	#The request has to be accessed via FastApi by using the article_id

	#article_id='abc911 2021-09-01 18:21:30' #suppose this is the article_id received via a request from the 3rd server

	#Now we will change the status code of the article with this article_id from unpublished_articles table
	instruction='update unpublished_articles set article_status = %s where article_id = %s'
	data=(1,article_id)
	mycursor.execute(instruction,data)
	mydb.commit()


	#STEP 2: RETRIEVE AND RETURNING THE JSON OBJECT OF THE ARTICLE

	instruction="select * from unpublished_articles where article_id = %s"
	data=(article_id,)
	mycursor.execute(instruction,data)
	result=mycursor.fetchone()
	#print(result['article_id'])


	#STEP 3: INSERT THE ARTICLE DETAILS INTO THE DIFFERENT TABLES AND THEN DELETE THE RECORD FROM Unpublished_articles

	#If there is no image which is represenited by image_count=0, then we will provide a default image link
	if result["image_count"]==0:
		ilink='https://images.unsplash.com/photo-1432821596592-e2c18b78144f?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80'

	else:
		ilink=result["image_link"]

	#The data is being pushed into the Approved_articles table which will send data for the tiles in json format
	instruction="insert into approved_articles (article_id, title, body,  img_link,  views,  likes, user_id, write_date) values (%s,%s,%s,%s,%s,%s,%s,%s)"
	data_sets=(result["article_id"],result["title"],result["body"],ilink,result["views"],result["likes"],result["user_id"],result["write_date"])
	mycursor.execute(instruction,data_sets)
	mydb.commit()


	#Now we delete the approved article from the unpublished articles table
	instruction="delete from iicblogdatabase.unpublished_articles where article_id=%s"
	data=(article_id,)
	mycursor.execute(instruction,data)
	mydb.commit()

	mydb.close()

	'''

	#One thing will be added here! Here I need to append the art.json object in a google sheet of IIC Technical Wing drive. This will be a good source of Backup. Need to learn google suite api and to convert json to csv files.


	'''
	mydb=pymysql.connect(host=a,user=b,password=c,database=d,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

	mycursor=mydb.cursor()

	#Now we start inserting these relevant informations about the article into other tables

	#Inserting into Authour name table

	instruction="insert into auth_filter (article_id, auth_name) values (%s,%s)"
	data_sets=(result["article_id"],result["auth_name"])
	mycursor.execute(instruction,data_sets)
	mydb.commit()


	#Inserting into Domain table

	my_list = result["domain"].split(",")
	for i in my_list:
		instruction="insert into domain_filter (article_id, domain) values (%s,%s)"
		data_sets=(result["article_id"],i)
		mycursor.execute(instruction,data_sets)
		mydb.commit()


	#Inserting into Sub-Domain table

	my_list = result["subdomain"].split(",")
	for i in my_list:
		instruction="insert into subdom_filter (article_id, sub_domain) values (%s,%s)"
		data_sets=(result["article_id"],i)
		mycursor.execute(instruction,data_sets)
		mydb.commit()


	#Inserting into title table

	instruction="insert into title_filter (article_id, title) values (%s,%s)"
	data_sets=(result["article_id"],result["title"])
	mycursor.execute(instruction,data_sets)
	mydb.commit()


	#Inserting into Date table

	instruction="insert into date_filter (article_id, write_date) values (%s,%s)"
	data_sets=(result["article_id"],result["write_date"])
	mycursor.execute(instruction,data_sets)
	mydb.commit()

	mydb.close()