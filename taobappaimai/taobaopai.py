#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-03-22 14:31:09
# Project: taobaopai

from pyspider.libs.base_handler import *
import re
import requests
from  lxml import etree
import lxml
import random
import json
from pymongo import MongoClient

class Prepareation:
    def random_agent():
        user_agent_list = [\
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
            "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
            "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
            "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
            "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
            "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
            "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
            "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
            "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
           ]
        return random.choice(user_agent_list)


    def get_headers():
        return {'Host': 'sf.taobao.com',
                'User-Agent':Prepareation.random_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://sf.taobao.com/item_list.htm',
                'Connection': 'keep-alive',}

    def PAGE_END():
        url='https://sf.taobao.com/item_list.htm?spm=a213w.7398504&category=50025969&city=&province=%D5%E3%BD%AD&auction_start_seg=-1'
        urlrequest=requests.get(url,headers=Prepareation.get_headers())
        first_page=etree.HTML(urlrequest.text)
        max_pagenum=''.join(first_page.xpath('//div[3]/div[4]/span[4]/em/text()'))
        
        return max_pagenum
    
 
class Handler(BaseHandler):
    crawl_config = {
    }
    
    def __init__(self):
        self.base_url='https://sf.taobao.com/list/50025969____%D5%E3%BD%AD.htm?spm=a213w.7398504&auction_start_seg=-1&page='
        self.page_num=1
        self.total_num=int(Prepareation.PAGE_END())
        self.pre=Prepareation()
        self.info=[]

    @every(minutes=24 * 60)
    def on_start(self):
        while self.page_num<=self.total_num:
            url=self.base_url+str(self.page_num)
            self.crawl(url,fetch_type='js',callback=self.index_page,headers=Prepareation.get_headers())
            self.page_num+=1
   
    
    @catch_status_code_error        
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        a=response.doc('#sf-item-list-data').text()
        b=json.loads(a)
        data=b["data"]
        for each in data:
            if each['status']=="done":
                print("拍卖已经结束了，不需要了.")
            else:
                self.crawl('https:'+each['itemUrl'],fetch_type='js',callback=self.detail_page,headers=Prepareation.get_headers())
    
    
    @config(priority=2)
    def detail_page(self, response):
        url_noticedetail=response.doc('#J_NoticeDetail').attr('data-from')
        url_noticedetail='https:'+url_noticedetail
        request1=requests.get(url_noticedetail,headers=Prepareation.get_headers())
        page1=etree.HTML(request1.text)
        noticedetail=''.join(page1.xpath('//span/text()'))
        url_itemNotice=response.doc('#J_ItemNotice').attr('data-from')
        url_itemNotice='https:'+url_itemNotice
        request2=requests.get(url_itemNotice,headers=Prepareation.get_headers())
        page2=etree.HTML(request2.text)
        itemnotice=''.join(page2.xpath('//span/text()'))
        return {
            "url": response.url,
            "title": response.doc('h1').text(),
            "start price":response.doc('.pay-price > .J_Price').eq(0).text(),
            "place bid range":response.doc('.pay-price > .J_Price').eq(1).text(),
            "valuation price":response.doc('.pay-price > .J_Price').eq(2).text(),
            "recognizance":response.doc('.pai-save-price > .J_Price').text(),
            "type":response.doc('.J_Type_p > .pay-type').text(),
            "bidding period":response.doc('td > span').eq(9).text(),
            "delay period":response.doc('.delay-td > span').eq(1).text(),
            "bidding info":response.doc('.pai-info > p').text(),
            "notice detail":noticedetail,
            "item notice":itemnotice
            
        }
    
    def on_result(self,result):
        if result:
            self.mongo_save(result)
                
    def mongo_save(self,result):
        client=MongoClient(host='127.0.0.1',port=27017)
        db_conn=client['tianmin']
        db_conn.authenticate('tianmin','111111')
        db=db_conn.get_collection('taobaopai')
        cc=db.insert(result)
        
    
    
    

     
        
            
    
   
