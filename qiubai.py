import urllib
import urllib2
import re
import sys
import time



filename = 'qiubaipage.txt'
file = open(filename,"w+")

# page = 1
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = { 'User-Agent' : user_agent }
# try:
#     request = urllib2.Request(url,headers = headers)
#     response = urllib2.urlopen(request)
#  
#     #print response.read().decode('utf-8')
#     content = response.read().decode('utf-8')
# #     pattern = re.compile('<div class="author clearfix">.*?<a href="/users/(.*?)".*?<img.*?alt="(.*?)"/></a>.*?<div.*?'+
# #                          'content">(.*?)<!--(.*?)-->.*?</div>.*?<div class="stats.*?class="number">(.*?)</i>',re.S)
#      
#     pattern = re.compile('<h2>(.*?)</h2>.*?<div class="content">(.*?)<!--(.*?)-->.*?<span class="stats-vote"><i class="number">(.*?)</i>',re.S)
#      
# #     items = re.findall(pattern,content)
#     items = re.findall(pattern,content)
#     for item in items:
#         print item[0],":",item[1],item[2],item[3]
#         stringline = "\n"+str(item[0].encode('utf-8'))+str(item[1].encode('utf-8'))+str(item[3].encode('utf-8'))
#         file.write(stringline)
# except urllib2.URLError,e:
#     if hasattr(e,"code"):
#         print e.code
#     if hasattr(e,"reason"):
#         print e.reason

class jokedownTool:
    def __init__ (self,str):
        self.pageindex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.stories = []
        self.enable = False
        self.strcomple = str
        
    def getpage(self,pageindex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageindex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print str("connection failed"),e.reason
                return None
            
    def getpageitems(self,pageindex):
        pagecode = self.getpage(pageindex)
        if not pagecode:
            print "load page failed...."
            return None
        pattern = re.compile(self.strcomple,re.S)
        items = re.findall(pattern,pagecode)
        pageStories = []
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,"\n",item[1])
            pageStories.append([item[0].strip(),text.strip(),item[3].strip(),item[2].strip()])
        return pageStories
        
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getpageitems(self.pageindex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageindex += 1 
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print "page:%d\tAuthor:%s\tfavar:%s,date:%s\n%s" %(page,story[0],story[2],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(story[3]))),story[1])  
            
    def start(self):
        print "reading joke press'enter'to get latest,'Q'"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)
                
    
    
spider = jokedownTool('<h2>(.*?)</h2>.*?<div class="content">(.*?)<!--(.*?)-->.*?<span class="stats-vote"><i class="number">(.*?)</i>')
spider.start()   
        