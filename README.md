# Weibo_Hot_Search  
参考 <https://github.com/Writeup007/weibo_Hot_Search>  
每天都在见证历史  

---
# 运行环境  
Python 3.6 +  
```bash
python -m pip install beautifulsoup4 requests
```
或者执行
```bash
# python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

---
# 运行
```bash
# 抓取当前时间的热搜数据, 需配合定时任务
python weibo_Hot_Search.py

# 将db的数据写入到json文件中, 默认为前一天的数据
python db_to_json.py
```

---
# json文件格式  
```json
{
 "timestamp1": [
  {
   "rank": 1,
   "topic": "xxx",
   "count": 100,
   "attach": "沸"
  },
  {
   "rank": 2,
   "topic": "xxxx",
   "count": 99,
   "attach": "热"
  },
 ],
 "timestamp2": [
   {
   "rank": 1,
   "topic": "xxx",
   "count": 100,
   "attach": "沸"
  },
  {
   "rank": 2,
   "topic": "xxxx",
   "count": 99,
   "attach": "热"
  },
 ]
}
```

---
# 接口来源
使用的是新浪微博的公开热搜榜单 链接：<https://s.weibo.com/top/summary>