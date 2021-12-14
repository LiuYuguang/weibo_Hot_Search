import sqlite3
import datetime
import json
import os

# base_path = os.getenv('HOME') + '/Documents/Hot_Search'
base_path = '.'

if __name__ == '__main__':
    today = datetime.datetime.today()
    today = datetime.datetime(today.year, today.month, today.day)
    yesterday = today - datetime.timedelta(days = 1)
    today_timestamp = int(today.timestamp())
    yesterday_timestamp = int(yesterday.timestamp())

    db = sqlite3.connect(base_path + "/hot.db")
    cursor = db.cursor()
    cursor.execute('SELECT UPDATETIME FROM WEIBO_HOT WHERE UPDATETIME >= ? AND UPDATETIME < ? GROUP BY UPDATETIME ORDER BY UPDATETIME;',(yesterday_timestamp,today_timestamp))
    updatetime_all = cursor.fetchall()
    
    #print(updatetime_all)
    weibo_data_all = {}
    for updatetime, in updatetime_all:
        cursor.execute('SELECT RANK, TOPIC, COUNT, ATTACH FROM WEIBO_HOT WHERE UPDATETIME = ? ORDER BY RANK;',(updatetime,))
        data = cursor.fetchall()
        weibo_data = []
        for rank,topic,count,attach in data:
            weibo_data.append({'rank':rank,'topic':topic,'count':count,'attach':attach})
        weibo_data_all[datetime.datetime.fromtimestamp(updatetime).isoformat()] = weibo_data
    
    #print(weibo_data_all)
    db.close()
    json_filename = '/weibo_%04d%02d%02d.json'%(yesterday.year,yesterday.month,yesterday.day)
    json_path = f'{base_path}/data/{yesterday.year}/{yesterday.month}'
    if not os.path.isdir(json_path):
        os.makedirs(json_path)
    with open(json_path + json_filename,'w',encoding='utf8') as f:
        json.dump(weibo_data_all,f, indent=1, ensure_ascii=False)


    
