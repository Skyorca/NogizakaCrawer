# idea
啊，是偶像宅的想法
因为才入坑乃团所以要通过阅读member之前的博客来进一步了解！
因为日语不上手所以引入谷歌机翻！
一点点在改进中，不过确实能收很多图！

# 爬虫趴下来的内容树
文件按照日期分类，包含博客主体和博客照片。注：因为妹子们照片的链接有两种格式，但是其中一种格式的链接大多是她们用的各种emoji...所以照片里可能包含大量emoji...不过每个妹子使用的emoji系列不同，可以收获很大有趣的表情也能看出妹子的性格。

# 如何启动
因为是多线程爬虫，通过bash multi_thread.sh启动start.py文件

然后需要在start.py修改line 28里面的idol_url来爬取对应小偶像的博客（参照global_var.py）

start.py调用crawer.py和translator.py。注意翻译接口有点问题，正在调试，即不能一次性完成写入日文，写入图片，翻译并写入中文三种操作，只能完成前两者。

test.py就是测试函数的集合，主要是看内容格式怎么提取。其他随用随加。

![正在爬取...](https://github.com/Skyorca/NogizakaCrawer/blob/master/crawing.png)