#This module will accept the json file and store it into the unpublished table of MySql database

from dotenv import load_dotenv   
load_dotenv()
import os
import pymysql

a=os.environ.get('host')
b=os.environ.get('user')
c=os.environ.get('password')	
d=os.environ.get('database')



#Here we need to accept the json body from server 2 and save the json file as sample.json
#This cannot handle mutiple json bodies sent all at once....only one at a time
#For every json object sent, it will keep overwriting the json file and from there we will store it

def store_unpub(json_obj):

     mydb=pymysql.connect(host=a,user=b,password=c,database=d,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

     mycursor=mydb.cursor()
     
     instruction="insert into unpublished_articles (article_id, title, body,auth_name, Auth_designation, write_date, domain, subdomain, article_status,  views,likes,  user_id, facebook_link, twitter_link, linkedin_link, image_count, image_link) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
     data_sets=(json_obj["article_id"],json_obj["title"],json_obj["body"],json_obj["auth_name"],json_obj["Auth_designation"],json_obj["write_date"],json_obj["domain"],json_obj["sub_domain"],json_obj["status"],json_obj["views"],json_obj["likes"],json_obj["user_id"],json_obj["facebook_link"],json_obj["twitter_link"],json_obj["linkedin_link"],json_obj["image_count"],json_obj["image_link"])
     mycursor.execute(instruction,data_sets)
     mydb.commit()

     mydb.close()
     