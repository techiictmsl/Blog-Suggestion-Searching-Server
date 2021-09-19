'''
In this main module we will implement all the functionalities of Server 4
This module will also act as the backbone for building the endpoit with FastAPI 
and handling the database connections.

'''



from fastapi import FastAPI
from typing import  Optional
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


import Landing_page_info
import Article_Analytics_info
import Filter_based_results
import Store_unpub_article
import Store_approved_article
import Suggestions_and_sorting


app=FastAPI()


@app.get('/landing_page')
async def send_all_article_ids():
	result= Landing_page_info.trending()
	res=[]
	for i in result:
		res.append(i[0])
	return res

@app.post('/send_details')
async def send_info_of_article_ids(recieved_art_ids: list):
	result=Landing_page_info.send_trending(recieved_art_ids)
	res={}
	for i in range(len(result)):
		res[result[i][0]]=[result[i][x] for x in range(len(result[i])) if x!=0 ]
	json_compatible_item_data = jsonable_encoder(res)
	return JSONResponse(content=json_compatible_item_data)

@app.post('/reading')
async def article_reading(article_id:str, user_id: str):
	Article_Analytics_info.onread(article_id,user_id)
	return "success"

@app.post('/liking')
async def article_liking(article_id:str, user_id: str):
	Article_Analytics_info.onlike(article_id, user_id)
	return "success"

@app.post('/unlike')
async def article_unliked(article_id:str, user_id: str):
	Article_Analytics_info.onunlike(article_id, user_id)
	return "success"

class Article(BaseModel):
	title:str
	body: str
	auth_name: str
	Auth_designation: str
	write_date: str
	domain: str
	sub_domain: str
	status: int
	views:int
	likes:int
	image_count:int
	image_link: Optional[str]
	user_id:str
	article_id:str
	facebook_link:str
	twitter_link:str
	linkdin_link:str


@app.post('/submit_unpublished_article')
async def saving_unpub_article(article: Article):
	Store_unpub_article.store_unpub(article)
	return "success"

@app.post('/store approve articles')
async def saving_approved_articles(article_id: str):
	Store_approved_article.store_into_all(article_id)
	return "success"

@app.get('/searching')
async def search_everything():
	return Filter_based_results.existing_data()

class datafilter(BaseModel):
	title: str 
	auth: str 
	domain: str
	subdomain: str

@app.post('/filtering')
async def filter_results(data: datafilter):
	json_compatible_item_data = jsonable_encoder(data)
	find=Filter_based_results.store(json_compatible_item_data)
	return Filter_based_results.fetch(find)

@app.post('/Suggestions')
async def suggestions_results(article_id:str):
	Sim_arts=Suggestions_and_sorting.similar_articles(article_id)
	Sim_arts=Suggestions_and_sorting.sortarts(Sim_arts)
	Same_auth=Suggestions_and_sorting.same_authour(article_id)
	Same_auth=Suggestions_and_sorting.sortarts(Same_auth)
	return Suggestions_and_sorting.send_details(Sim_arts,Same_auth)