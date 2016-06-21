# CNKICrawler

---

这个程序用来抓取cnki上论文的摘要等信息。目前实现的功能是抓取所有博士论文的相关信息。最终每条纪录的JSON如下：
```
{
    "school" : "北京大学",    // 作者所属学校
    "name" : "**",           // 作者姓名
    "title" : "基于动态随机一般均衡模型的中国经济波动数量分析",                        // 论文题目
    "abstract" : "我国自改革开放以来,经济在高速增长的同时也经历了较大幅度的波动。GDP增长速度有时高达15%,而有时却低至不足4%,相差超过11个百分点。而同时,我国通货膨胀的波动还更大。面对如此幅度的经济波动,一个自然的问题是:什么原因造成了我国的经济波动?这正是本文研究的主要课题。当今宏观经济学认为经济波动是由外生的随机冲击所驱动的。弄清冲击的来源,是了解经济波动机制的关键一步。目前,通常被认为是经济波动驱动力的冲击有技术冲击、货币政策冲击、偏好冲击、及成本冲击等数种。但究竟哪几种冲击在经济波动的过程中更为重要,不同的理论有着不同的看法。本文的研究从冲击的分解入手,来研究我国经济波动的机制。在总结了我国经济波动的典型事实后,本文构建了两个动态随机一般均衡模型作为分析的工具。利用贝叶斯方法估计了模型参数后,又通过卡尔曼平滑算法估计了模型中各个外生冲击的实现值。将估计得到的各个冲击分别带回模型进行模拟,可以研究在各冲击单独作用下,模型中各个内生变量的波动情况。这样,在模型的帮助下我们分解了各个冲击对经济波动的影响,进而找出了其中比较重要的冲击,最终帮助我们加深了对中国经济波动机制的理解...",                   // 论文摘要
    "uri" : "/kns/detail/detail.aspx?QueryID=2&CurRec=10&recid=&FileName=2008114441.nh&DbName=CDFD9908&DbCode=CDFD&pr=",     // cnki的uri后缀
    "author_other" : [ "北京大学", "金融学", "2008", "博士" ],  // 作者其他信息，专业，论文发表年限，学位等
    "other" : { 
        "download" : "6405",   // 下载次数
        "tag" : [ "F224" ],    // 分类标签，有些会分到多个标签
        "reference" : "74"     // 被引用次数
    }, 
    "keywords" : [ "经济波动", "货币政策", "动态随机一般均衡模型", "冲击分解" ],   // 关键词
    "teacher" : [ "陈平；" ]    // 指导老师
}
```
目前总共收集到373581条纪录。
收集这些数据的主要目的还是为了之后NLP或者其他ML/DL实验使用。比如接下来我会拿这些数据试一试文本分类。
当然，如果你对这些数据感兴趣或者有什么想法，欢迎联系我。
email：279581355@qq.com、roliygu@gmail.com
额，值得一提的是，中间数据并没有用git管理起来，所以直接跑cnki.py是跑不起来的，如果想自己跑一下的话，可以等我再完善一下。

### 1. Dependency

If you want run this program, you need install some other python package. Including requests, BeautifulSoup4, etc...
There should be the mongoDB on your pc, because the latest program's data storage base on mongoDB.
To install python package, you can use "pip install package_name" command (require pip had been installed in your pc successfully).
And make sure your mongoDB can be connected, such as ip, port, username and password, etc, are right. Mongo's connect options all in the mongo_utils/mongo_utils.py

### 2. DataStruct

#### 2.1 PaperURL

The PaperURL model is crawler/cnki_class.PaperURL. It represents the url list of paper with different tag.

