import requests
import re
from lxml import etree
import global_var
import translator
import os




class Nogizaka:

    def check_month(self, url, date):
        '''
        如果这个月没有更博，就跳过，防止内容错乱
        '''
        new_url = url+"?d="+date
        content_ = requests.get(url=new_url, headers=global_var.headers ).text
        content  = re.sub('\n','',content_).encode('utf8')
        tree     = etree.HTML(content)
        yearmonth = tree.xpath("//*[@id='sheet']/div[@class='unit']//span[@class='yearmonth']")
        ym = yearmonth[0].text.replace('/','')
        if ym == date: return True
        else: return False


    def get_max_page(self,url,date):
        new_url = url+"?d="+date
        content_ = requests.get(url=new_url, headers=global_var.headers ).text
        content  = re.sub('\n','',content_).encode('utf8')
        tree     = etree.HTML(content)
        pagectrl = tree.xpath("//*[@id='blogstyle1']/div[@class='paginate']")
        if len(pagectrl) !=0 :
            pages = pagectrl[0].xpath('a')
            self.pagenum = int(pages[-2].text)
        else:
            self.pagenum = 1
        
    def craw_whole_pages(self, blogdir, url, date):
        if self.check_month(url, date):
            self.get_max_page(url, date)
            if self.pagenum>1:
                for p in range(1, self.pagenum+1):
                    new_url = url+"?p="+str(p)+"&"+"d="+date
                    content_ = requests.get(url=new_url, headers=global_var.headers).text
                    content  = re.sub('\n','',content_).encode('utf8')
                    tree     = etree.HTML(content)
                    blogurls = tree.xpath("//*[@id='sheet']/div[@class='unit']//span[@class='entrytitle']")
                    yearmonth = tree.xpath("//*[@id='sheet']/div[@class='unit']//span[@class='yearmonth']")
                    dd1 = tree.xpath("//*[@id='sheet']/div[@class='unit']//span[@class='dd1']")
                    dd2 = tree.xpath("//*[@id='sheet']/div[@class='unit']//span[@class='dd2']")
                    blognum = len(yearmonth) # len(yearmonth)=len(dd1)=len(dd2)
                    for l in range(blognum):
                        blogdate = yearmonth[l].text.replace('/','-') +'-'+dd1[l].text+'-'+dd2[l].text
                        blogurl  = blogurls[l].xpath('a')[0].attrib['href']
                        blogtitle = blogurls[l].xpath('a')[0].text
                        self.craw_one_blog(blogdir, blogtitle, blogdate, blogurl)

            else:
                new_url = url+"?p=1"+"&"+"d="+date
                content_ = requests.get(url=new_url, headers=global_var.headers).text
                content  = re.sub('\n','',content_).encode('utf8')
                tree     = etree.HTML(content)
                blogurls = tree.xpath("//*[@id='sheet']/div[@class='unit']//span[@class='entrytitle']")
                yearmonth = tree.xpath("//*[@id='sheet']/div[@class='unit']//span[@class='yearmonth']")
                dd1 = tree.xpath("//*[@id='sheet']/div[@class='unit']//span[@class='dd1']")
                dd2 = tree.xpath("//*[@id='sheet']/div[@class='unit']//span[@class='dd2']")
                blognum = len(yearmonth) # len(yearmonth)=len(dd1)=len(dd2)
                for l in range(blognum):
                    blogdate = yearmonth[l].text.replace('/','-') +'-'+dd1[l].text+'-'+dd2[l].text
                    blogurl  = blogurls[l].xpath('a')[0].attrib['href']
                    blogtitle = blogurls[l].xpath('a')[0].text
                    self.craw_one_blog(blogdir, blogtitle, blogdate, blogurl)
                    

    def craw_one_blog(self, blogdir, blogtitle, date, url):
        content_ = requests.get(url=url, headers=global_var.headers).text
        content  = re.sub('\n','',content_).encode('utf8')
        tree     = etree.HTML(content)
        #好像在某年网站保存内容的标签格式发生了变化，从<p>移到了<div> 故保险起见全部带上
        blogcontents = tree.xpath("//*[@id='sheet']/div[@class='unit']//div[@class='entrybodyin']/div")
        blogcontents += tree.xpath("//*[@id='sheet']/div[@class='unit']//div[@class='entrybodyin']//p")
        pics     = tree.xpath("//*[@id='sheet']/div[@class='unit']//div[@class='entrybodyin']//img")
        blogcontent = str()
        for c in blogcontents:
            if str(c.text)!= 'None': blogcontent += str(c.text) 
            else: blogcontent += '\n'
        
        with open("./{}/{}.txt".format(blogdir, date),'w+') as f:
            f.write(blogtitle+'\n\n')
            f.write(blogcontent) 
        try:
            p_num = 1
            for p in pics:
                pic_url = p.attrib['src']
                pic = requests.get(url=pic_url, headers=global_var.headers)
                with open("./{}/{}-{}.jpg".format(blogdir, date, p_num),'wb') as f:
                    f.write(pic.content)
                p_num += 1
        except:
            pass
        print("./{}/{}.txt Success!".format(blogdir, date))
        #self.tran_to_CN(blogdir, date)
        #末尾别忘记擦除一个blog的记录
        self.blogtitle = str()
        self.blogcontent = str()

        
        
    def tran_to_CN(self, blogdir, date):
        try:
            with open("./{}/{}-CN.txt".format(blogdir, date),'w') as f:
                trans_title = translator.transformer(self.blogtitle)
                f.write(trans_title+'\n\n')
                strlength = 300
                blog_pieces = re.findall(r'.{'+str(strlength)+'}', self.blogcontent)
                blog_pieces.append(self.blogcontent[len(blog_pieces)*strlength:])
                res = str()
                for s in blog_pieces:
                    s_tran = translator.transformer(s)
                    res += s_tran
                if len(res)>0: 
                    f.write(res)
                    print("./{}/{}-CN.txt Success!".format(blogdir, date))
        except Exception as e:
            print(e)
            print("./{}/{}-CN.txt Fail!!".format(blogdir, date))


def wait_tasks_done(pool):
    for t in pool:
        if not t.alive():
            pool.remove(t)
        else:
            t.join()  

        