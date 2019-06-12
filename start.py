import crawer
import re
import global_var
import time
import os
import sys
from threading import Thread

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

poolnum = 10

def start_craw(start):
    nogi = crawer.Nogizaka()
    pool = []
    #嫂子是从201210开始
    idol_url = global_var.url33
    idolname = re.findall('http://blog.nogizaka46.com/(.*)/smph/',idol_url)[0]
    for d in range(start,len(callender)):
        os.makedirs("./{}/{}".format(idolname,  callender[d]))
        blogdir = idolname+'/'+ callender[d]
        task = Thread(target=nogi.craw_whole_pages, args=(blogdir, idol_url,callender[d],))
        task.start()
        pool.append(task)
        if len(pool) == poolnum: 
            crawer.wait_tasks_done(pool)
        print(callender[d]+' DONE!!!')
        time.sleep(1)

start_craw(int(sys.argv[1]))