import http.client
import hashlib
import urllib.parse
import random
import json
import re


 
def transformer(content):
    appid = '20190608000305785' #你的appid
    secretKey = '_8C9_ppTTBlwJUi0tRxf' #你的密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = 'jp'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
    
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        c = response.read()  #???why这里返回的突然变成了bytes
        s = json.loads(c)
        dst = s["trans_result"][0]["dst"]
        return dst
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

 

