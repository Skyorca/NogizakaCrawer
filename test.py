import translator
import re

def test_file():
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

test_file()

'''
12 10 21
13 1 21
13 5 10
13 10 20
13 10 17
13 12 25 21
18  02--now


'''