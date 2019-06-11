import requests
import re
from lxml import etree
import time
import global_var
import translator
import os
#from mysql_manager import MySQLManager
from threading import Thread


class Nogizaka:
    
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
                    self.craw_one_blog(blogdir, blogdate, blogtitle, blogurl)
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
                self.craw_one_blog(blogdir, blogdate, blogtitle, blogurl)

    def craw_one_blog(self, blogdir, date, title, url):
        content_ = requests.get(url=url, headers=global_var.headers).text
        content  = re.sub('\n','',content_).encode('utf8')
        tree     = etree.HTML(content)
        blogcontents = tree.xpath("//*[@id='sheet']/div[@class='unit']//div[@class='entrybodyin']/div")
        pics     = tree.xpath("//*[@id='sheet']/div[@class='unit']//div[@class='entrybodyin']/div//img")
        blogcontent  = str()
        for c in blogcontents:
            blogcontent += str(c.text)
        blogcontent.replace(' ','\n')
        '''
        with open("./{}/{}.txt".format(blogdir, date),'w') as f:
            f.write(title+'\n\n')
            f.write(blogcontent) 
        p_num = 1
        for p in pics:
            pic_url = p.attrib['src']
            pic = requests.get(url=pic_url, headers=global_var.headers)
            with open("./{}/{}-{}.jpg".format(blogdir, date, p_num),'wb') as f:
                f.write(pic.content)
            p_num += 1
        '''
        try:
            with open("./{}/{}-CN.txt".format(blogdir, date),'w') as f:
                trans_title = translator.transformer(title)
                f.write(trans_title+'\n\n')
                strlength = 300
                blog_pieces = re.findall(r'.{'+str(strlength)+'}', blogcontent)
                blog_pieces.append(blogcontent[len(blog_pieces)*strlength:])
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

callender = [global_var.date1,global_var.date2,global_var.date3,global_var.date4,global_var.date5,global_var.date6,global_var.date7
,global_var.date8,global_var.date9,global_var.date10,global_var.date11,global_var.date12,global_var.date13,global_var.date14,
global_var.date15,global_var.date16,global_var.date17,global_var.date18,global_var.date19,global_var.date20,global_var.date21,
global_var.date22,global_var.date23,global_var.date24,global_var.date25,global_var.date26,global_var.date27,global_var.date28,
global_var.date29,global_var.date30,global_var.date31,global_var.date32,global_var.date33,global_var.date34,global_var.date35,global_var.date36,
global_var.date37,global_var.date38,global_var.date39,global_var.date40,global_var.date41,global_var.date42,global_var.date43,global_var.date44,
global_var.date45,global_var.date46,global_var.date47,global_var.date48,global_var.date49,global_var.date50,global_var.date51,global_var.date52,
global_var.date53,global_var.date54,global_var.date55,global_var.date56,global_var.date57,global_var.date58,global_var.date59,global_var.date60,
global_var.date61,global_var.date62,global_var.date63,global_var.date64,global_var.date65,global_var.date66,global_var.date67,global_var.date68,
global_var.date69,global_var.date70,global_var.date71,global_var.date72,global_var.date73,global_var.date74,global_var.date75,global_var.date76,
global_var.date77,global_var.date78,global_var.date79,global_var.date80,global_var.date81,global_var.date82,global_var.date83,global_var.date84,
global_var.date85,global_var.date86,global_var.date87,global_var.date88,global_var.date89,global_var.date90,global_var.date91]


if __name__ == "__main__":
    nogi = Nogizaka()
    #嫂子是从201210开始
    idolname = re.findall('http://blog.nogizaka46.com/(.*)/smph/',global_var.url12)[0]
    for d in range(0,len(callender)):
        os.makedirs("./{}/{}".format(idolname,  callender[d]))
        blogdir = idolname+'/'+ callender[d]
        nogi.craw_whole_pages(blogdir, global_var.url1,callender[d])
        print(callender[d]+' trans DONE!!!')
        time.sleep(1)
    