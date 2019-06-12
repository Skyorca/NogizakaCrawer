import translator
import requests
import re
from lxml import etree
import global_var

def test_file():
    '''
    测试读取已存储日文博客并调用百度翻译接口翻译
    '''
    strlength = 300
    with open("./manatsu.akimoto/201210/2012-10-21-Sun.txt",'r') as f:
        c = f.read()
        c = c.replace('\n','')
        blog_pieces = re.findall(r'.{'+str(strlength)+'}', c)
        blog_pieces.append(c[len(blog_pieces)*strlength:])
        res = str()
        for s in blog_pieces:
            s_tran = translator.transformer(s)
            res += s_tran
        print(res)

#test_file()

def test_format():
    '''
    根据不同网页的不同内容格式测试提取内容的方法
    '''
    new_url = "http://blog.nogizaka46.com/kazumi.takayama/smph/2012/12/009392.php"
    content_ = requests.get(url=new_url, headers=global_var.headers).text
    content  = re.sub('\n','',content_).encode('utf8')
    tree     = etree.HTML(content)
    blogcontents = tree.xpath("//*[@id='sheet']/div[@class='unit']//div[@class='entrybodyin']/div")
    blogcontents += tree.xpath("//*[@id='sheet']/div[@class='unit']//div[@class='entrybodyin']//p")
    if len(blogcontents)==0:
        blogcontents = tree.xpath("//*[@id='sheet']/div[@class='unit']//div[@class='entrybodyin']")
    print(blogcontents[0].text)
    blogcontent = str()
    for c in blogcontents:
        if str(c.text)!= 'None': blogcontent += str(c.text) 
        else: blogcontent += '\n'
    #print(blogcontent)

test_format()










'''
12 10 21
13 1 21
13 5 10
13 10 20
13 10 17
13 12 25 21
18  02--now


'''