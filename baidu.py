#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, urllib2, urllib, json, time, logging
from dotenv import load_dotenv
from splinter import Browser

class MigrateBaiduToAmap:

    size            = 500
    baiduFavListUrl = "https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=fav&mode=get&type=favdata&limit=%s&lastver=0&t=1542598987100" 
    amapPoiSearchUrl = "https://restapi.amap.com/v3/place/text?"
    amapPoiDetailUrl = "https://ditu.amap.com/detail/get/detail?id="

    #百度cookie BDUSS
    baiduBDUSS   = ""
    #高德地图cookie passport_login
    amapPassport = ""
    #高德地图开放平台 Web服务 key
    amapKey      = ""

    logger      = None
    baiduOpener = None
    amapOpener  = None
    browser     = None
    headless    = False

    def __init__(self, logger, baiduBDUSS, amapPassport, amapKey):
        self.logger       = logger
        self.baiduBDUSS   = baiduBDUSS
        self.amapPassport = amapPassport
        self.amapKey      = amapKey

    def run(self):
        self.initBaiduOpener()
        self.initAmapOpener()
        self.initBrowser()
        favList = self.getFavListFromBaidu()
        if favList == None: 
            return False

        for keyword in favList:
            if keyword:
                poiId = self.getAmapPoi(keyword)
                poiId and self.addAmapFav(poiId)
                time.sleep(1)

        self.browser.quit()


    def initBaiduOpener(self):
        self.logger.info('initBaiduOpener')
        self.baiduOpener = urllib2.build_opener()
        self.baiduOpener.addheaders.append(('Cookie', 'BDUSS=' + self.baiduBDUSS))
        self.baiduFavListUrl = self.baiduFavListUrl % self.size

    def initAmapOpener(self):
        self.logger.info('initAmapOpener')
        self.amapOpener = urllib2.build_opener()
        self.amapOpener.addheaders.append(('Cookie', 'passport_login=' + self.amapPassport))

    def initBrowser(self):
        self.logger.info('initBrowser')
        self.browser = Browser('chrome', headless=self.headless)
        self.browser.visit('https://ditu.amap.com')
        self.browser.cookies.add({'passport_login': self.amapPassport})

    def getFavListFromBaidu(self):
        self.logger.info('getFavListFromBaidu')
        res = self.baiduOpener.open(self.baiduFavListUrl)
        ret = res.read()

        jsonData = json.loads(ret)
        sync     = jsonData.get('sync')
        if sync == None: 
            self.logger.error('getFavListFromBaidu error %s' % sync)
            yield False

        favList  = sync.get('newdata')
        if favList==None:
            self.logger.error('getFavListFromBaidu error %s' % favList)
            favList = []
            yield False

        for item in favList:
            if item['detail']['data'] == False: continue

            data  = item['detail']['data']
            extra = data['extdata']
            #t       = data.get('type')
            name    = extra.get('name')
            content = extra.get('content')
            if name == None: continue
            if content == None: content = ''

            keyword = name.encode('utf8') + "|" + content.encode('utf8')
            yield keyword

    def getAmapPoi(self, keyword):
        self.logger.info('getAmapPoi %s' % keyword)
        params = {'key':self.amapKey, 'keywords':keyword, 'offset':1}
        url  = self.amapPoiSearchUrl + urllib.urlencode(params)
        res  = self.amapOpener.open(url)
        ret  = res.read()
        jsonData = json.loads(ret)
        pois = jsonData.get('pois')
        if pois == None  or type(pois) == unicode or not len(pois): 
            return False

        poiId = pois[0]['id']
        return poiId

    def addAmapFav(self, poiId):
        self.logger.info('addAmapFav %s' % poiId)
        url = 'https://ditu.amap.com/place/' + poiId
        self.browser.visit(url)
        btn = self.browser.find_by_css('span[class="collect favit"]')
        btn and btn.click()

    
if __name__ == "__main__":
    load_dotenv('.env')
    baiduBDUSS   = os.getenv('BAIDU_BDUSS')
    amapPassport = os.getenv('AMAP_PASSPORT')
    amapKey      = os.getenv('AMAP_KEY')

    logger = logging.getLogger('MigrateBaiduToAmap')

    fmt       = "[%(asctime)s] %(levelname)s: line %(lineno)d  %(message)s"
    datefmt   = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    stream = logging.StreamHandler(stream=None)
    logger.addHandler(stream)
    stream.setFormatter(formatter)

    logger.setLevel(logging.INFO) 

    handler = MigrateBaiduToAmap(logger, baiduBDUSS, amapPassport, amapKey)
    handler.run()
