# -*- coding:utf-8 -*-  
import urllib    # Python中的cURL库  
from urllib import request
import random
import time    # 时间函数库，包含休眠函数sleep()  
from bs4 import BeautifulSoup
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    # 伪装成Chrome浏览器  
#user_agent= "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
#user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"
#user_agent= ""
refererData = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=csdn%20%E6%80%9D%E6%83%B3%E7%9A%84%E9%AB%98%E5%BA%A6%20csdnzouqi&oq=csdn%20%E6%80%9D%E6%83%B3%E7%9A%84%E9%AB%98%E5%BA%A6&rsv_pq=fe7241c2000121eb&rsv_t=0dfaTIzsy%2BB%2Bh4tkKd6GtRbwj3Cp5KVva8QYLdRbzIz1CCeC1tOLcNDWcO8&rqlang=cn&rsv_enter=1&rsv_sug3=11&rsv_sug2=0&inputT=3473&rsv_sug4=3753'    
# 伪装成是从baidu.com搜索到的文章  
#refererData = 'https://www.baidu.com/s?wd=python%20%E8%99%9A%E6%8B%9F%E6%9C%BA%20Linux%20csdn&rsv_spt=1&rsv_iqid=0xa79c7e3700006d95&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=02003390_3_hao_pg&rsv_enter=1&rsv_t=d6861dgZgc6hXo9bysn2uNe1mjyMnJNJrpjtTPRLE2Y86c90nrsoSmXqrl2o9PtOVFN4HUnniVg&oq=python%2520%25E8%2599%259A%25E6%258B%259F%25E6%259C%25BA%2520Linux&inputT=2189&rsv_pq=c7aedfaf00022711&rsv_sug3=67&rsv_sug1=45&rsv_sug7=100&rsv_sug2=0&rsv_sug4=3228'
headers = {'User-Agent' : user_agent, 'Referer' : refererData}    # 构造GET方法中的Header  
count=0
#刷的地址
url='https://blog.csdn.net/weixin_42350212'
def getArcList(url):
	req = request.Request(url, headers=headers) 
	page = request.urlopen(req).read()  
	soup = BeautifulSoup(page,'lxml')
	h4=soup.find_all('h4',attrs={'class':'text-truncate'})
	all_src=[]
	for item in h4:
		href=item.select("a")[0].get('href')
		description=item.select("a")[0].get_text().replace(" ","").replace("\n","")
		link={'des':description,'url':href}
		all_src.append(link)
	return all_src
def getUp(arcUrl,arcDes):
	req = request.Request(arcUrl, headers=headers) 
	request.urlopen(req)
if __name__ == '__main__':
	count=0
	all_src=getArcList(url)
	while 1:
		for src in all_src:
      #过滤只刷原创
			if src['des'][0:1]=="原":
				count+=1    # 计数器加1  
				print (str(count)+":"+src['des'])    # 打印当前循环次数  
				getUp(src['url'],src['des'])
				time.sleep(random.randint(6, 8))
