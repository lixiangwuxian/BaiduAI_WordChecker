# BaiduAI_WordChecker
用来过滤敏感词，防止被炸号

How to use:
```python
import word_checker

API_key="..."#from baidu
Secret_key="..."
c=Word_checker(API_key,Secret_key)
print(c.check_word("*******"))
print(c.word_replace("*******"))
```
