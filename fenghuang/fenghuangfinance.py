#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-03-29 16:52:52
# Project: fenghuangfinance

from pyspider.libs.base_handler import *
import re
from pymongo import MongoClient

class Handler(BaseHandler):
    crawl_config = {
    }
    
    

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://app.finance.ifeng.com/list/stock.php?t=ha', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
       
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://finance.ifeng.com/app/hq/stock/sh(\d+)/index.shtml",each.attr.href, re.U) or re.match("http://finance.ifeng.com/app/hq/stock/sz(\d+)/index.shtml",each.attr.href, re.U):
                self.crawl(each.attr.href,callback=self.detail_page)
                
      
        if response.doc('td > a[href^="http://app.finance.ifeng.com/list/stock.php?t=ha&f=chg_pct&o=desc&p="]').eq(1).attr.href==None:
            next=response.doc('td > a[href^="http://app.finance.ifeng.com/list/stock.php?t=ha&f=chg_pct&o=desc&p="]').eq(0).attr.href
            self.crawl(next, callback=self.index_page)
        else:
            next=response.doc('td > a[href^="http://app.finance.ifeng.com/list/stock.php?t=ha&f=chg_pct&o=desc&p="]').eq(1).attr.href
            self.crawl(next, callback=self.index_page)
            
    def detail_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("(.*?)symbol(.*?)",each.attr.href, re.U):
                self.crawl(each.attr.href,fetch_type='js',callback=self.data_page)
        
    @config(priority=2)
    def data_page(self, response):
        print(response.doc('td').nextAll())
        print(response.doc('td').nextAll().eq(15).text())
        print(re.findall('gsgg',response.url))
        if re.findall('gsgg',response.url)==['gsgg']:
            print(0)
            return {
                "url": response.url,
                "title": response.doc('title').text(),
                "personal_profile0":response.doc('td').nextAll().eq(30).text(),
                "personal_profile1":response.doc('td').nextAll().eq(61).text(),
                "personal_profile2":response.doc('td').nextAll().eq(92).text(),
                "personal_profile3":response.doc('td').nextAll().eq(123).text(),
                "personal_profile4":response.doc('td').nextAll().eq(154).text(),
                "personal_profile5":response.doc('td').nextAll().eq(185).text(),
                "executive_positions0":response.doc('td').nextAll().eq(2).text(),
                "executive_positions1":response.doc('td').nextAll().eq(33).text(),
                "executive_positions2":response.doc('td').nextAll().eq(64).text(),
                "executive_positions3":response.doc('td').nextAll().eq(95).text(),
                "executive_positions4":response.doc('td').nextAll().eq(126).text(),
                "executive_positions5":response.doc('td').nextAll().eq(157).text(),
            }
        elif re.findall('zcfzb',response.url)==['zcfzb']:
            print(1)
            return {
                "url": response.url,
                "title": response.doc('title').text(),
                "report_period0":response.doc('td').nextAll().eq(0).text(),
                "report_period1":response.doc('td').nextAll().eq(1).text(),
                "report_period2":response.doc('td').nextAll().eq(2).text(),
                "report_period3":response.doc('td').nextAll().eq(3).text(),
                "cash0":response.doc('td').nextAll().eq(22).text(),
                "cash1":response.doc('td').nextAll().eq(23).text(),
                "cash2":response.doc('td').nextAll().eq(24).text(),
                "cash3":response.doc('td').nextAll().eq(25).text(),
                "transactional_financial_assets0":response.doc('td').nextAll().eq(32).text(),
                "transactional_financial_assets1":response.doc('td').nextAll().eq(33).text(),
                "transactional_financial_assets2":response.doc('td').nextAll().eq(34).text(),
                "transactional_financial_assets3":response.doc('td').nextAll().eq(35).text(),
            }
        elif re.findall('gdgb',response.url)==['gdgb']:
            print(1)
            return {
                "url": response.url,
                "title": response.doc('title').text(),
                "sharehold_name0":response.doc('td').nextAll().eq(15).text(),
                "sharehold_name1":response.doc('td').nextAll().eq(30).text(),
                "sharehold_name2":response.doc('td').nextAll().eq(45).text(),
                "sharehold_name3":response.doc('td').nextAll().eq(60).text(),
                "sharehold_name4":response.doc('td').nextAll().eq(75).text(),
                "sharehold_name5":response.doc('td').nextAll().eq(90).text(),
                "sharehold_name6":response.doc('td').nextAll().eq(105).text(),
                "sharehold_name7":response.doc('td').nextAll().eq(120).text(),
                "sharehold_name8":response.doc('td').nextAll().eq(135).text(),
                "sharehold_name9":response.doc('td').nextAll().eq(150).text(),
                "amount_of_holding_shares0":response.doc('td').nextAll().eq(16).text(),
                "amount_of_holding_shares1":response.doc('td').nextAll().eq(31).text(),
                "amount_of_holding_shares2":response.doc('td').nextAll().eq(46).text(),
                "amount_of_holding_shares3":response.doc('td').nextAll().eq(61).text(),
                "amount_of_holding_shares4":response.doc('td').nextAll().eq(76).text(),
                "amount_of_holding_shares5":response.doc('td').nextAll().eq(91).text(),
                "amount_of_holding_shares6":response.doc('td').nextAll().eq(106).text(),
                "amount_of_holding_shares7":response.doc('td').nextAll().eq(121).text(),
                "amount_of_holding_shares8":response.doc('td').nextAll().eq(136).text(),
                "amount_of_holding_shares9":response.doc('td').nextAll().eq(151).text(),
                "shareholding_proportion0":response.doc('td').nextAll().eq(17).text(),
                "shareholding_proportion1":response.doc('td').nextAll().eq(32).text(),
                "shareholding_proportion2":response.doc('td').nextAll().eq(47).text(),
                "shareholding_proportion3":response.doc('td').nextAll().eq(62).text(),
                "shareholding_proportion4":response.doc('td').nextAll().eq(77).text(),
                "shareholding_proportion5":response.doc('td').nextAll().eq(92).text(),
                "shareholding_proportion6":response.doc('td').nextAll().eq(107).text(),
                "shareholding_proportion7":response.doc('td').nextAll().eq(122).text(),
                "shareholding_proportion8":response.doc('td').nextAll().eq(137).text(),
                "shareholding_proportion9":response.doc('td').nextAll().eq(152).text(),
                "frozen_shares0":response.doc('td').nextAll().eq(18).text(),
                "frozen_shares1":response.doc('td').nextAll().eq(33).text(),
                "frozen_shares2":response.doc('td').nextAll().eq(48).text(),
                "frozen_shares3":response.doc('td').nextAll().eq(63).text(),
                "frozen_shares4":response.doc('td').nextAll().eq(78).text(),
                "frozen_shares5":response.doc('td').nextAll().eq(93).text(),
                "frozen_shares6":response.doc('td').nextAll().eq(108).text(),
                "frozen_shares7":response.doc('td').nextAll().eq(123).text(),
                "frozen_shares8":response.doc('td').nextAll().eq(138).text(),
                "frozen_shares9":response.doc('td').nextAll().eq(153).text(),
                "pledged_shares0":response.doc('td').nextAll().eq(19).text(),
                "pledged_shares1":response.doc('td').nextAll().eq(34).text(),
                "pledged_shares2":response.doc('td').nextAll().eq(49).text(),
                "pledged_shares3":response.doc('td').nextAll().eq(64).text(),
                "pledged_shares4":response.doc('td').nextAll().eq(79).text(),
                "pledged_shares5":response.doc('td').nextAll().eq(94).text(),
                "pledged_shares6":response.doc('td').nextAll().eq(109).text(),
                "pledged_shares7":response.doc('td').nextAll().eq(124).text(),
                "pledged_shares8":response.doc('td').nextAll().eq(139).text(),
                "pledged_shares9":response.doc('td').nextAll().eq(154).text(),
                
            }
    def on_result(self,result):
        print(result)
        if result:
            self.mongo_save(result)
                
    def mongo_save(self,result):
        client=MongoClient(host='127.0.0.1',port=27017)
        db_conn=client['tianmin']
        db_conn.authenticate('tianmin','111111')
        db=db_conn.get_collection('fenghuang')
        cc=db.insert(result)
        print(result)
            
            
