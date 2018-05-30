# -*- coding:utf-8 -*- 
import re
import requests
from urllib import request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
from bs4 import BeautifulSoup
send_headers={"Accept-Encoding":"gzip, deflate",
              "Connection":"keep-alive",
              "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
              "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
              "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"}
options = Options()
#无头参数
#options.add_argument('-headless')  
driver = webdriver.Firefox(firefox_options=options)
def reqs():
	response=requests.get("https://mm.taobao.com/search_tstar_model.htm",headers=send_headers)
	response.encoding="utf-8"
	print(response.status_code)
	fw.write(str(response.text))
#传入主链接和跳转的页码,通过过滤条件 返回page 和 个人信息
def filpage(url,page_num):
	try:
		driver.get(url)
		driver.find_elements_by_xpath("/html/body/div/div[@class='mm_paginator']/div[@class='page']/span[4]/input[1]")[0].send_keys(page_num)
		driver.find_elements_by_xpath("/html/body/div/div[@class='mm_paginator']/div[@class='page']/span[4]/input[2]")[0].click()
	except Exception as e:
		driver.close
		return
	time.sleep(0.2)
	htmlfile=driver.page_source
	soup=BeautifulSoup(htmlfile,'lxml')
	itemSrc=soup.find_all('a',attrs={'class':'item-link'})
	all_src=[]
	for item in itemSrc:
		name=item.select("span[class='name']")[0].get_text()
		city=item.select("span[class='city']")[0].get_text()
		infos=item.select('div[class="info row2"] span')[0].get_text()
		infos="".join(infos.split())
		print(str(infos).split('/'))
		if len(str(infos).split('/'))==2:
			height=str(infos).split('/')[0]
			weight=str(infos).split('/')[1]
			src=item.get('href')
			if height>='170CM' and weight<='50KG':
				dic={'name':name,'page':'https:'+str(src),'city':city,'infos':infos}
				all_src.append(dic)
	return all_src
		#点击下一页
def getLinks(page_url):
	all_links=[]
	try:
		driver.get(page_url)
	except Exception as e:
		return
	htmlfile=driver.page_source
	name=driver.title
	soup=BeautifulSoup(htmlfile,'lxml')
	itemLink=soup.find_all('img')
	for item in itemLink:
		link={'name':name,'url':"https:"+str(item.get('src'))}
		all_links.append(link)
	return all_links	
def save_pics(pic,count,city,infos):
	#pic为字典,name:,url:
	req = request.Request(url=pic, headers=send_headers)  
	isCityexists=os.path.exists("E:\\pythonTest\\taobao\\"+city)
	isPersonexists=os.path.exists("E:\\pythonTest\\taobao\\"+city+"\\"+infos)
	if not isCityexists:
		os.makedirs("E:\\pythonTest\\taobao\\"+city+"\\"+infos)
	else:
		if not isPersonexists:
			os.makedirs("E:\\pythonTest\\taobao\\"+city+"\\"+infos)
	try:
		request.urlopen(req).read() 
	except Exception as e:
		print('保存失败...'+str(infos+pic))
		return
	f = open('E:\\pythonTest\\taobao\\'+city+'\\'+infos+'\\'+str(count)+".jpg", 'wb')
	f.write(request.urlopen(req).read())
	print('保存成功...'+str(infos+pic)) 
if __name__ == '__main__':
	srcs=[]
	count=1
	#爬取的页码数
	url='https://mm.taobao.com/search_tstar_model.htm'
	url='https://mm.taobao.com/search_tstar_model.htm?style=%E6%80%A7%E6%84%9F&place=city%3A'
	for i in range(1,1000):
		pages=filpage(url, i)
		print(pages)
		for page in pages:
			print(page)
			pics=getLinks(page['page'])
			for pic in pics:
				info=(page['name']+'_'+page['infos']).replace('/','_')
				save_pics(pic['url'],count,page['city'],info)
				count+=1
