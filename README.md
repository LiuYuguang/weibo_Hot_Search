# Weibo_Hot_Search  
参考 <https://github.com/Writeup007/weibo_Hot_Search>  
每天都在见证历史  

---
# 运行环境  
Python 3.6 +  
```bash
# python -m pip3 freeze > requirements.txt
python -m pip3 install -r requirements.txt
```

---
# 运行
```bash
# 抓取数据
python weibo_Hot_Search.py

# 将db的数据下入到json文件中, 默认为前一天的数据
python db_to_json.py
```

---
# json文件格式  
```json
{
 "2021-07-10T15:26:02": [
  {
   "rank": 1,
   "topic": "被当街强塞进车女子回应",
   "count": 3064751,
   "attach": "沸"
  },
  //...
 ],
 "2021-07-10T15:27:02": [
   {
   "rank": 3,
   "topic": "被当街强塞进车女子回应",
   "count": 1202878,
   "attach": "沸"
  },
  //...
 ],
 //...
}
```

---
# 接口来源
使用的是新浪微博的公开热搜榜单 链接：<https://s.weibo.com/top/summary>