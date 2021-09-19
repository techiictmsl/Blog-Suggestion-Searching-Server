'''
There are two objectives in this section: 
1) Firstly, the landing page has two sections or divisions: most viewed/trending articles and recently published
2) Server 4 will send the preliminary infos about the articles in each section
'''


import mysql.connector
from dotenv import load_dotenv   
load_dotenv()
import os
import mysql.connector

a=os.environ.get('host')
b=user=os.environ.get('user')
c=password=os.environ.get('password')	
d=database=os.environ.get('database')

mydb=mysql.connector.Connect(
	host=a,
	user=b,
	password=c,
	database=d
)

mycursor=mydb.cursor()

def trending():

	#Send article ids of all the existing articles to the landing page so that sayan can ask for 4 at a time
	instruction="select article_id from approved_articles order by views desc;"
	mycursor.execute(instruction)
	result=mycursor.fetchall() 
	#print(result)
	return result

def send_trending(recieved_art_ids):

	#After recieving article id's from the froont-end indicating which one's to show, we will send the info about those articles to sayan
	#recieved_art_ids=['abc911 2021-09-01 18:21:30','abc789 2021-08-30 18:21:30']
	tot_res=[]
	for i in recieved_art_ids:
		instruction="select * from approved_articles where article_id = (%s)"
		data=(i,)
		mycursor.execute(instruction,data)
		result=mycursor.fetchone()
		tot_res.append(result)

	return tot_res
	#return tot_result which contains the info about 4 articles at a time in a list

def recent_pub():
	instruction="select article_id from date_filter order by write_date desc;"
	mycursor.execute(instruction)
	result=mycursor.fetchall()
	print(result)
	#return result


def send_recent():
	#After recieving article id's from the froont-end indicating which one's to show, we will send the info about those articles to sayan
	recieved_art_ids=['abc789 2021-08-30 18:21:30','abc456 2021-08-23 01:49:30']
	tot_res=[]
	for i in recieved_art_ids:
		instruction="select * from approved_articles where article_id = (%s)"
		data=(i,)
		mycursor.execute(instruction,data)
		result=mycursor.fetchone()
		tot_res.append(result)
	print(tot_res)		

'''
#Need to convert these into json and then send
trending()
send_trending()
recent_pub()
send_recent()
'''



