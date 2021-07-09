import re
import requests
import bs4
import datetime
import os
import sqlite3

import logging
import logging.handlers
base_path = '/home/lyg001/Documents/Hot_Search'

log_path = f'{base_path}/log'
if not os.path.isdir(log_path):
	os.makedirs(log_path)

TimeHandler = logging.handlers.TimedRotatingFileHandler(log_path + '/log',when='MIDNIGHT')
TimeHandler.suffix = '%Y%m%d'
logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',level = logging.DEBUG,handlers = [TimeHandler])

def crawl():
	url = 'https://s.weibo.com/top/summary'
	headers = {}
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
	headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
	headers['Connection'] = 'keep-alive'
	headers['Referer'] = 'https://weibo.com/'
	try:
		r = requests.get(url,headers=headers,timeout=10)
		return r.text
	except Exception as e:
		logging.error(f'str(e)')
		return None

def analyze(data):
	data_list = []

	soup = bs4.BeautifulSoup(data,features="html.parser")

	div = soup.find('div',attrs={'class':'data','id':'pl_top_realtimehot'})
	if div == None:
		logging.error('<div class="data" id="pl_top_realtimehot"> no found')
		return data_list
	
	tbody = div.find('tbody')
	if tbody == None:
		logging.error('<tbody> no found')
		return data_list

	now = datetime.datetime.now()
	now = int(now.timestamp())

	tr_set = tbody.find_all('tr')
	for tr in tr_set:
		td_set = tr.find_all('td')
		td_icon,td_rank,td_topic,td_count,td_attach = None,None,None,None,None
		for td in td_set:
			if re.match('^td-01',td.attrs['class'][0]) != None:
				if td.i != None:
					td_icon = td.i.attrs['class'][0]
				td_rank = td.text
			
			if re.match('^td-02',td.attrs['class'][0]) != None:
				l = td.text.split('\n')
				if len(l) > 1:
					td_topic = l[1]
				if len(l) > 2:
					td_count = l[2]
			
			if re.match('^td-03',td.attrs['class'][0]) != None:
				td_attach = td.text
		
		logging.info(f'{td_icon},{td_rank},{td_topic},{td_count},{td_attach}')
		
		if not td_rank.isnumeric():
			continue
			
		td_rank = int(td_rank)
		if not td_count.isnumeric():
			td_count = 0
		else:
			td_count = int(td_count)
		
		data_list.append([now,td_rank,td_topic,td_count,td_attach])

	return data_list

def dump(data):
	now = datetime.datetime.now()
	day = now.strftime('%Y%m%d')
	time = now.strftime('%H%M%S')

	path = f'{base_path}/html/{day}/weibo_{time}.html'
	dirname = os.path.dirname(path)
	if not os.path.isdir(dirname):
		os.makedirs(dirname)
	with open(path,'w') as f:
		f.write(data)

db = sqlite3.connect(base_path + "/hot.db")
def create_db():
	cursor = db.cursor()
	cursor.execute(f'CREATE TABLE IF NOT EXISTS WEIBO_HOT (UPDATETIME INTEGER NOT NULL, RANK INTEGER NOT NULL, TOPIC TEXT, COUNT INTEGER, ATTACH TEXT, PRIMARY KEY(UPDATETIME,RANK));')
	db.commit()
	cursor.close()
	pass

def insert_db(data_list):
	cursor = db.cursor()
	for updatetime,rank,topic,count,attach in data_list:
		cursor.execute(f'INSERT INTO WEIBO_HOT (UPDATETIME, RANK, TOPIC, COUNT, ATTACH) VALUES (?,?,?,?,?);',(updatetime,rank,topic,count,attach))
	db.commit()
	cursor.close()
	pass

if __name__ == '__main__':
	data = crawl()
	if data == None:
		exit(0)
	
	dump(data)
	
	data_list = analyze(data)

	create_db()
	insert_db(data_list)
