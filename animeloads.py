import requests, http.cookiejar

import myjdapi

from lxml import etree
from lxml import html

from html_table_parser import HTMLTableParser

import subprocess

from Cryptodome.Cipher import AES
from binascii import unhexlify
import base64

import numpy, random, time

import re

import os, sys, time

from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.webdriver.chrome.options
import selenium.webdriver.firefox.options


class CacheAnime:
    def __init__(self, cacheTime):
        self.cacheTime = cacheTime
        self.cacheList = []

    def addToCache(self, identifier, anime):
        entry = [identifier, int(time.time()), anime]
        self.cacheList.append(entry)

    def getFromCache(self, identifier):
        for entry in self.cacheList:
            if(entry[0] == identifier):
                dbgprint(entry[1])
                dbgprint(int(time.time()))
                dbgprint((entry[1] - int(time.time())) / 60)
                if(((entry[1] - int(time.time())) / 60) > -self.cacheTime):
                    return entry[2]
        return False

class CacheSearch:
    def __init__(self, cacheTime):
        self.cacheTime = cacheTime
        self.cacheList = []

    def addToCache(self, query, resultList):
        entry = [query, int(time.time()), resultList]
        self.cacheList.append(entry)

    def getFromCache(self, query):
        for entry in self.cacheList:
            if(entry[0] == query):
                dbgprint(entry[1])
                dbgprint(int(time.time()))
                dbgprint((entry[1] - int(time.time())) / 60)
                if(((entry[1] - int(time.time())) / 60) > -self.cacheTime):
                    return entry[2]
        return False


#captcha
import time, json, hashlib, cv2, numpy, shutil

logfile = open("animeloads.log", "a")

dbg = True

def dbgprint(msg, loglevel="verbose", dep=""):
    msg = str(msg)
    loglevel = str(loglevel)
    dep = str(dep)
    if(loglevel != ""):
        loglevel = "[" + loglevel + "] "
    if(dep != ""):
        dep = "[" + dep + "] "
    if(dbg):
        try:
            print(loglevel + dep + msg)
        except:
            pass
    try:
        logfile.write(loglevel + dep + msg + "\n")
    except:
        pass
    

class animeloads:

    FIREFOX = 0
    CHROME = 1
    UPLOADED = 0
    DDOWNLOAD = 1
    RAPIDGATOR = 2

    def __init__(self, user="", pw="", browser="", browserloc="", cacheTime=0):
        self.user = user
        self.pw = pw
        self.session = requests.session()
        self.username = "anonymous"
        self.isVIP = False
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

        self.cacheAnime = CacheAnime(cacheTime)
        self.cacheSearch = CacheSearch(cacheTime)
            
        if(browser == animeloads.CHROME):
            options = selenium.webdriver.chrome.options.Options()
            options.headless = True
            if(browserloc != ""):
                options.binary_location = browserloc
            driver = webdriver.Chrome(service_log_path=os.devnull, options=options)
        elif(browser == animeloads.FIREFOX):
            options = selenium.webdriver.firefox.options.Options()
            options.headless = True
            if(browserloc != ""):
                options.binary_location = browserloc
            driver = webdriver.Firefox(service_log_path=os.devnull, options=options)
        else:
            raise ALInvalidBrowserException("Nicht unterstützter Browser")

        #Erster besuch auf der Seite, damit cookies hinzugefügt werden können
        driver.get("https://www.anime-loads.org/assets/pub/images/logo.png")
        
        cookies = driver.get_cookies()
        
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
        driver.quit()

        if(user != "" and pw != ""):
            self.login(self.user, self.pw)
        
    def search(self, query):
        cacheResults = self.cacheSearch.getFromCache(query)
        if(cacheResults != False):
            print("Got query " + query + " from cache")
            return cacheResults
            
        searchdata = self.session.get(apihelper.getSearchURL(query), allow_redirects=False)
        searchresults = []
        print(searchdata.status_code)
        if(searchdata.status_code == 403):
            print("Got Access Denied")
            open('accessdenied.html', 'wb').write(searchdata.content)
        if(searchdata.status_code == 302):  #only 1 result, got redirect
            redir_url = searchdata.headers['Location']
            identifier = redir_url.split("/")[-1]
            cacheResult = self.cacheAnime.getFromCache(identifier)
            if(cacheResult != False):
                print("Got anime " + identifier + " from cache")
                redir_anime = cacheResult
            else:
                redir_anime = anime(redir_url, self.session, self)
            #num__results = 1
            result = searchResult(redir_url, redir_anime.getName(), redir_anime.getType(), redir_anime.getYear(), redir_anime.getCurrentEpisodes(), redir_anime.getMaxEpisodes(), ["UNKNOWN"], ["UNKNOWN"], redir_anime.getMainGenre(), self.session, self)
            searchresults.append(result)
        else:
            search_dom = etree.HTML(searchdata.text)
            searchboxes = search_dom.xpath("//div/div[@class='panel panel-default' and 1]/div[@class='panel-body' and 1]")
            #num__results = len(searchboxes)
            for result in searchboxes:
                url = ""                #done
                name = ""               #done
                typ = ""                #done
                relDate = ""            #done
                epCountCurrent = 0      #done
                epCountMax = 0          #done
                dubLang = []            #done
                subLang = []            #done
                genre = ""              #done
                boxtree = etree.HTML(html.tostring(result))
                result_links = boxtree.xpath("//a")
                isFirst = True              #Check if link is first entry, cause there are two
                for link in result_links:
                    linktext = link.text
                    href = link.get('href')
                    #if linktext is None or href is None:
                    #    continue
                    if("genre" in href):
                        genre = linktext
                    elif("https://www.anime-loads.org/anime-series" in href):
                        typ = "Series"
                    elif("https://www.anime-loads.org/anime-movies" in href):
                        typ = "Movie"
                    elif("https://www.anime-loads.org/bonus" in href):
                        typ = "Bonus"
                    elif("https://www.anime-loads.org/live-action" in href):
                        typ = "Live-Action"
                    elif("https://www.anime-loads.org/ova" in href):
                        typ = "OVA"
                    elif("https://www.anime-loads.org/special" in href):
                        typ = "Special"
                    elif("https://www.anime-loads.org/web" in href):
                        typ = "Web"
                    elif("https://www.anime-loads.org/year/" in href):  #Year-element
                        yearsplit = href.split("/")
                        year = yearsplit[len(yearsplit)-1]
                    elif("https://www.anime-loads.org/media/" in href): #href to detail site, contains link and name
                        if(isFirst):
                            isFirst = False
                            continue
                        url = href
                        name = linktext
                        isFirst = True
    
                result_span = boxtree.xpath("//span[@class='label label-gold']")    #Span-Element for Episode count
                for span in result_span:
                    epsplit = str(html.tostring(span)).split("/")
                    epCountCurrent = re.sub("[^0-9]", "", epsplit[1])   #Remove non-numbers from string
                    epCountMax = re.sub("[^0-9]", "", epsplit[2])
    
                lang_class = boxtree.xpath("//div[@class='mt10 mb10' and 3]")[0]       #Line which contains language flags, take first line as there is only one
                langsplit = str(html.tostring(lang_class)).split("\"")
                for substring in langsplit:
                    if("Sprache: " in substring):
                        dubLang.append(substring.replace("Sprache: ", ""))
                    elif("Untertitel: " in substring):
                        subLang.append(substring.replace("Untertitel: ", ""))
                result = searchResult(url, name, typ, relDate, epCountCurrent, epCountMax, dubLang, subLang, genre, self.session, self)
                searchresults.append(result)
        self.cacheSearch.addToCache(query, searchresults)
        return searchresults
            
    
    def getAnime(self, url):
        identifier = url.split("/")[-1]
        cacheResult = self.cacheAnime.getFromCache(identifier)
        if(cacheResult != False):
            print("Got anime " + identifier + " from cache")
            return(cacheResult)
        return anime(url, self.session, self)


    def login(self, user, pw):
        data = {"identity": user, "password": pw, "remember": "1"}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        r = self.session.post("https://www.anime-loads.org/auth/signin", data=data, headers=headers)

        for c in self.session.cookies:
            if("username" in c.value):
                data = unquote(c.value)
                jdata = json.loads(data)
                for key in jdata:
                    if(key == "username"):
                        self.username = jdata[key]
                    elif(key == "is_vip"):
                        if(jdata[key] == True):
                            self.isVIP = True
                return True
        print("Login failed. Cookies: ")
        print(self.session.cookies)
        raise ALInvalidLoginException("Login data is invalid")

    def getNewestEpisodes():
        pass

class utils:
    @staticmethod
    def decodeCNL(k, crypted):
#        k_list = list(k)
#        tmp = k_list[15]
#        k_list[15] = k_list[16]
#        k_list[16] = tmp
#        k = "".join(k_list)

        key = unhexlify(k)
        data = base64.standard_b64decode(crypted)
        obj = AES.new(key, AES.MODE_CBC, key)
        d = obj.decrypt(data)
        d = map(lambda x: x.strip(b'\r\x00'), d.split(b'\n'))
        d = list(d)
        return d
    
    @staticmethod
    def b(s):
        s = str(s)
        a = numpy.int32(0)
        if(len(s) == 0):
            return 0
        for curChar in range(0, len(s)):
            a = numpy.int32(a)
            a = ((a << 5) - a + ord(s[curChar]))
        return abs(a)
        
    @staticmethod
    def getAdString():
        rand1 = random.uniform(0, 1)
        first = ("" + str(utils.b(str(abs(rand1)))))
        
        
        date = str(round(time.time() * 1000))
        sec = ("" + str(utils.b(date)))
        
        rand3 = random.uniform(0, 1)
        third = ("" + str(utils.b(str(abs(rand3)))))
        
        return first + "" + sec + third

    @staticmethod
    def addToJD(host, passwords, source, crypted, jk):
        data = {
            "passwords": str(passwords),
            "source": str(source),
            "jk": str(jk),
            "crypted": str(crypted)
        }
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0 Waterfox/78.7.0"
        }
        try:
            req = requests.post("http://" + host + ":9666/flash/addcrypted2", data=data, headers=headers)
        except:
            return False
        retdata = req.text
        if(retdata == "failed"):
            return False
        else:
            return True

    @staticmethod
    def addToMYJD(myjd_user, myjd_pass, myjd_device, links, pkgName, pwd, destination=None):
        jd=myjdapi.Myjdapi()
        jd.set_app_key("animeloads")
        jd.connect(myjd_user, myjd_pass)
        jd.update_devices()

        devices = jd.list_devices() 
             
        dbgprint("Deine verbundenen Geräte: ")
        for dev in devices:
            dbgprint(dev['name'])

        try:
            device=jd.get_device(myjd_device)
        except:
            print("Jdownloader Device does not exist")
            return False
        
        dl = device.linkgrabber


        print(destination)
        try:
            retvalue = dl.add_links(params=[{
                              "autostart": True,
                              "links": links,
                              "packageName": pkgName,
                              "extractPassword": pwd,
                              "priority": "DEFAULT",
                              "downloadPassword": None,
                              "destinationFolder": destination,
                              "overwritePackagizerRules": False
                          }])
        except myjdapi.exception.MYJDConnectionException as e:
            dbgprint(e)
            retvalue = False
        return retvalue

    @staticmethod
    def getDifference(img1, img2):
        res = cv2.absdiff(img1, img2)
        res = res.astype(numpy.uint8)
        percentage = (numpy.count_nonzero(res) * 100)/ res.size
        return percentage

    @staticmethod
    def doCaptcha(cID, driver,session, b64):
        captcha_baseURL = "https://www.anime-loads.org/files/captcha"
        img_baseURL = captcha_baseURL + "?cid=0&hash="
    

        #get captcha images

        print("Getting captcha images")

        js = "var xhr2 = new XMLHttpRequest(); \
xhr2.open('POST', 'https://www.anime-loads.org/files/captcha', false); \
xhr2.setRequestHeader('Content-type', 'application/x-www-form-urlencoded'); \
xhr2.send('cID=0&rT=1'); \
return xhr2.response;"

        ajaxresponse = driver.execute_script(js)

        captchaIDs = ajaxresponse.replace("\"", "").replace("[", "").replace("]", "").split(",")

        request_cookies_browser = driver.get_cookies()

        c = [session.cookies.set(c['name'], c['value']) for c in request_cookies_browser]

        images = []
        images_url = []
        correct_index = -1

        session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }

        for c in captchaIDs:
            url = img_baseURL + c
            images_url.append(c)
#            print(url)
            response = session.get(url, stream=True, headers=headers)

#            print(response.status_code)
#            with open('img.png', 'wb') as out_file:
#               shutil.copyfileobj(response.raw, out_file)
#            del response
            images.append(response.content)

        print("Got captcha images")

        #solve captcha images

        print("Calculating correct captcha")

        cv_images = []

        for image in images:
            nparr = numpy.frombuffer(image, numpy.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv_images.append(img_np)

        perc = []

        for img in cv_images:
            iPerc = 0
            for i in cv_images:
                if(hashlib.md5(i).digest() == hashlib.md5(img).digest()):
                    pass
                else:
                    iPerc += utils.getDifference(img, i)
            perc.append(iPerc)

        biggest = 0
        bigI = -1

        for idx, iPerc in enumerate(perc):
            print("Percentage img " + str(idx) + ": " + str(iPerc))
            if(iPerc > biggest):
                biggest = iPerc
                bigI = idx

        print("Correct captcha: Image Nr. " + str(bigI + 1) + " with a confidence of " + str(biggest))

        #send right captcha image

        print("Checking if captcha is correct")

        capURL = captcha_baseURL + "?cID=0&pC=" + images_url[bigI] + "&rT=2"

        js = "var xhr2 = new XMLHttpRequest(); \
 xhr2.open('POST', '" + captcha_baseURL + "', false); \
xhr2.setRequestHeader('Content-type', 'application/x-www-form-urlencoded'); \
xhr2.send('cID=0&pC=" + images_url[bigI] + "&rT=2'); \
return xhr2.response;"

        ajaxresponse = driver.execute_script(js)

#        if(ajaxresponse == "1"):
#            print("Captcha was correct")
#        else:
#            print(ajaxresponse)
#            return False




        #parse right links


        js = "var xhr = new XMLHttpRequest(); \
xhr.open('POST', 'https://www.anime-loads.org/ajax/captcha', false); \
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded'); \
xhr.send('enc=" + b64.decode('ascii') + "&response=captcha&captcha-idhf=0&captcha-hf=" + images_url[bigI] + "'); \
return xhr.response"

        ajaxresponse = driver.execute_script(js)

        print(ajaxresponse)

        code = ""
        message = ""
        reflinks = ""
        content_uploaded = ""
        content_ddl = ""
        content_rappid = ""

        response_json = json.loads(ajaxresponse)

        return response_json


class apihelper:
    @staticmethod
    def getSearchURL(query):
        return "https://www.anime-loads.org/search?q=" + query




class searchResult():
    def __init__(self, url, name, typ, relDate, epCountCurrent, epCountMax, dubLang, subLang, genre, session, animeloads):
        self.url = url
        self.animeloads = animeloads
        self.name = name
        self.typ = typ
        self.relDate = relDate
        self.epCountCurrent = epCountCurrent
        self.epCountMax = epCountMax
        self.dubLang = dubLang
        self.subLang = subLang
        self.genre = genre
        self.session = session

    def getUrl(self):
        return self.url

    def getIdentifier(self):
        return self.url.split("/")[-1]

    def getName(self):
        return self.name
    
    def getTyp(self):
        return self.typ

    def getReleaseDate(self):
        return self.relDate

    def getCurrentEpisodeCount(self):
        return self.epCountCurrent

    def getMaxEpisodeCount(self):
        return self.epCountMax

    def getDubLang(self):
        return self.dubLang

    def getSubLang(self):
        return self.getSubLang

    def getGenre(self):
        return self.genre

    def tostring(self):
        return "Name: " + self.name + ", Typ: " + self.typ + ", Episoden: " + str(self.epCountCurrent) + "/" + str(self.epCountMax) + ", Dub: " + str(self.dubLang) + ", Subs: " + str(self.subLang)

    def getAnime(self):
        cacheResult = self.animeloads.cacheAnime.getFromCache(self.getIdentifier())
        if(cacheResult != False):
            print("Got anime " + self.getIdentifier() + " from cache")
            return cacheResult
        return anime(self.url, self.session, self.animeloads)   #todo session redundant

class anime():
    def __init__(self, url, session, animeloads):
        self.url = url
        self.animeloads = animeloads
        self.session = session
        self.gerName = ""
        self.engName = ""
        self.japName = ""
        self.synonymes = []     
        self.type = ""
        self.year = 0
        self.runtime = 0
        self.status = ""
        self.mainGenre = ""
        self.sideGenres = []
        self.tags = []
        self.releases = []
        self.curEpisodes = 1337
        self.maxEpisodes = 1337
        self.updateInfo()
        animeloads.cacheAnime.addToCache(self.getIdentifier(), self)

    def updateInfo(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        
        #Ad Adstring, an attempt to bypass adblock detection
        #adstring = utils.getAdString()
        #self.session.cookies.set("adcashufpv3", adstring, domain="www.anime-loads.org")
        
        self.session.cookies.set("adsblocked", "0", domain="www.anime-loads.org")
        self.session.cookies.set("hideads", "1", domain="www.anime-loads.org")

        detailPage = self.session.get(self.url, headers=headers)
        cock = [
            {'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path}
            for c in self.session.cookies
        ]

        #Load all JS scripts in an attempt to bypass adblock detection
#        js = detailPage.text.split("<script type=\"text/javascript\" src=\"")
#        for j in js:
#            if(j[0:4] == "http"):
#                self.session.get(j.split("\"")[0])

        try:

            p = HTMLTableParser()
            p.feed(detailPage.text)
    
            detailtable = p.tables[0]
            for detail in detailtable:
                leftEntry = detail[0]
                rightEntry = detail[1]
                if("Titel" == leftEntry):
                    if(self.japName == ""):
                        self.japName = rightEntry
                    elif(self.gerName == ""):
                        self.gerName = rightEntry
                    else:
                        self.engName = rightEntry
                elif("Synonyme" == leftEntry):
                    self.synonymes = rightEntry.split(", ")
                elif("Typ" == leftEntry):
                    if(rightEntry == "Anime Serie"):
                        self.type = "Series"
                    elif(rightEntry == "Web"):
                        self.type = "Web"
                    elif(rightEntry == "Special"):
                        self.type = "Special"
                    elif(rightEntry == "OVA"):
                        self.type = "OVA"
                    elif(rightEntry == "Anime Film"):
                        self.type = "Movie"
                    elif(rightEntry == "Bonus"):
                        self.type = "Bonus"
                    elif(rightEntry == "Live Action"):
                         self.type = "Live-Action"

                    
                elif("Episoden" == leftEntry):
                    epString = rightEntry.split("/")
                    try:
                        self.curEpisodes = int(epString[0])
                    except:
                        self.curEpisodes = 0
                    try:
                        self.maxEpisodes = int(epString[1])
                    except:
                        self.maxEpisodes = 999999
                elif("Jahr" == leftEntry):
                    self.year = int(rightEntry)
                elif("Laufzeit" == leftEntry):
                    runtimestring = re.sub("[^0-9]", "", rightEntry)
                    if(runtimestring == ""):
                        runtimestring = "0"
                    self.runtime = int(runtimestring)
                elif("Status" == leftEntry):
                    self.status = rightEntry
                elif("Hauptgenre" == leftEntry):
                    self.mainGenre = rightEntry
                elif("Nebengenre" == leftEntry):
                    self.sideGenres = rightEntry.split("  ")
                elif("Tags" == leftEntry):
                    self.tags = rightEntry.split("  ")
    
    
            rel_dom = etree.HTML(detailPage.text)
            releases_unparsed = rel_dom.xpath("//div[@id='downloads']/div[@class='row' and 1]/div[@class='col-sm-3' and 1]/ul[@class='nav nav-pills nav-stacked' and 1]")[0]    #Get left list of releases
            releases_dom = etree.HTML(html.tostring(releases_unparsed))
            releases = releases_dom.xpath("//li")   #Get single releases from list
    
            numReleases = len(releases) - 1         #Last release is "Add release", ignoring
    
            #rid, group, res, dubs, subs, format, size, password, anmerkung=""
            for relIndex in range(0, numReleases):
                relID = relIndex + 1
                group = ""      #done
                res = ""        
                dubs = []       #done
                subs = []       #done
                videoformat = ""    
                size = 0            
                password = ""       
                anmerkung = ""      
                episodes = 0
                table = p.tables[relID]    #First release, get name and anmerkung
    
                for idx in range(0, len(table)):
                    try:
                        tLeft = table[idx][0]
                        tRight = table[idx][1]
                    except:
                        continue
    
                    if(tLeft == "Release Gruppe"):
                        group = tRight
                    elif(tLeft == "Auflösung"):
                        res = tRight.split("x")[1] + "p"
                    elif(tLeft == "Typ"):
                        videoformat = tRight
                    elif(tLeft == "Größe"):
                        if("GB" in tRight):
                            try:
                                size = float(re.sub("[^0-9.]", "", tRight)) * 1000
                            except:
                                size = 0.0
                        else:
                            try:
                                size = float(re.sub("[^0-9.]", "", tRight))
                            except:
                                size = 0.0
                    elif(tLeft == "Passwort"):
                        password = tRight
                    elif(tLeft == "Release Anmerkungen"):
                        anmerkung = tRight
    
        
                detailhtmlstring = str(html.tostring(releases[relIndex]))        #Detail html from release for languages#
    
                ###################
                #WARNING: UGLY CODE
                ###################
    
                dublangsubstring = detailhtmlstring.split("title=\"Sprache: ")      #HTMLCode split for Languages
                for idx in range(1, len(dublangsubstring)):                         #Start with second result, first is always garbage
                    dublang = dublangsubstring[idx].split("\"")[0]                  #Cut string after ", language end there
                    dubs.append(dublang)                                            #Add to dublist
    
    
    
                sublangsubstring = detailhtmlstring.split("title=\"Untertitel: ")   #HTMLcode split for Subtitles
                for idx in range(1, len(sublangsubstring)):                         #Start with second result, first is always garbage
                    sublang = sublangsubstring[idx].split("\"")[0]                  #Cut string after ", subtitle end there
                    subs.append(sublang)                                            #Add to sublist
    
                ##############
                #UGLY CODE END
                ##############
                #TODO Search for faster method for episode traversal        SLOOOOOOOOOOW
                episodes = []
                epnum = 0
#                singleEP = rel_dom.xpath("//a[@aria-controls='downloads_episodes_" + str(relID) + "_" + str(epnum) + "']")
#                print("Episodenumber: " + str(epnum))
#                print("Len: " + str(len(rel_dom.xpath("//*[@id=\"downloads_episodes_" + str(relID) + "\"]/div/a[" + str(epnum) + "]/span"))))
#                rel_dom.xpath("//*[@id=\"downloads_episodes_" + str(relID) + "\"]/div/a[" + str(epnum+2) + "]/span/text()")
                allEpisodes = rel_dom.xpath("//*[@id=\"downloads_episodes_" + str(relID) + "\"]/div/a[*]/span/text()")
#                print("Number of Episodes: " + str(len(allEpisodes)))
                for idx, epi in enumerate(allEpisodes):
#                    print(epi[1:])
                    if(idx == 0 and len(allEpisodes) > 1):
                        continue
                    if(len(allEpisodes) == 1):
                        cnlfix = 1
                    else:
                        cnlfix = 0
                    curepisode = episode(idx + cnlfix, epi)
                    episodes.append(curepisode)

                if(len(allEpisodes) > 1):
                    removeCNLfromList = 1
                else:
                    removeCNLfromList = 0
                tmprel = release(self.url, relID, group, res, dubs, subs, len(allEpisodes) - removeCNLfromList, videoformat, size, password, episodes, anmerkung, detailPage.text, self.session)
                self.releases.append(tmprel)
            return True

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            if("IndexError" in str(exc_type)):
                print("Fehler beim parsen. Dies liegt sehr wahrscheinlich daran, dass anime-loads gerade offline ist oder einen Fehler hat.\nWenn der Fehler länger besteht, bitte auf Github melden.")
                print(exc_type, fname, exc_tb.tb_lineno)
            else:
                print("Fehler beim parsen, bitte auf Github melden")
                print(exc_type, fname, exc_tb.tb_lineno)
            return False

    
    #quality: prefer 1080p/DTS
    def getBestReleaseByQuality(self, releaseList=[]):
        if(len(releaseList) == 0):
            releaseList = self.releases

        if(len(releaseList) == 1): #Only 1 release available, has to be the best
            return releaseList[0]

        rel720p = []
        rel1080p = []
        relrest = []
        for rel in releaseList:
            if(rel.getResolution() == "1080p"):
                rel1080p.append(rel)
            elif(rel.getResolution() == "720p"):
                rel720p.append(rel)
            else:
                relrest.append(rel)
        if(len(rel1080p) == 0):         #Get best video quality
            if(len(rel720p) == 0):
                bestList = relrest
            else:
                bestList = rel720p
        else:
            bestList = rel1080p
        
        #PCM>FLAC=DTS>AC3>AAC>MP3           #Thx to Toastkiste21 & Tanukichan
        pointlist = []
        for rel in bestList:            #Get best audio quality
            points = 0
            audio = rel.getAudioCodec()
            audiotypes = ["MP3", "AAC", "AC3", "DTS", "FLAC&DTS", "PCM"]        #list, from worse to best
            for idx, typ in enumerate(audiotypes):
                audios = typ.split("&")
                for splitaudio in audios:
                    if(splitaudio == audio):
                        points += idx       #Audio found, add index to points(best has highest index)
                    else:
                        points += 1         #Other, unknown audio, only one point
            pointlist.append(points)


        bestrel = bestList[0]
        bestscore = 0
        for idx, rel in enumerate(bestList):
            score = pointlist[idx]
            codec = rel.getVideoCodec().lower()
            if(codec == "x265" or codec == "hevc"):
                score += 2
            #print("Release " + str(rel.getID()) + " with " + str(score) + " points")
            if(score > bestscore):
                bestscore = score
                bestrel = rel
        
        return rel


    #language: prefer GerDub/GerSub
    def getBestReleaseByLanguage(self, releaseList=[]):
        if(len(releaseList) == 0):
            releaseList = self.releases

        if(len(releaseList) == 1): #Only 1 release available, has to be the best
            return releaseList[0]

        dubreleases = []
        for rel in releaseList:
            for dub in rel.getDubs():
                if(dub == "Deutsch"):
                    dubreleases.append(rel)
        if(len(dubreleases) == 0):
            for rel in releaseList:
                for dub in rel.getDubs():
                    if(dub == "Englisch"):
                        dubreleases.append(rel)
        if(len(dubreleases) == 0):
            dubreleases = releaseList #No (Eng/Ger)dub releases, just going with subs
        maxsubs = 0
        relmaxsubs = []
        for rel in dubreleases:
            if(len(rel.getSubs()) >= maxsubs):
                maxsubs = len(rel.getSubs())
                relmaxsubs.append(rel)

        return self.getBestReleaseByQuality(relmaxsubs)


    #episodes: most episodes
    def getBestReleaseByEpisodes(self, releaseList=[]):
        if(len(releaseList) == 0):
            releaseList = self.releases

        if(len(releaseList) == 1): #Only 1 release available, has to be the best
            return releaseList[0]

        max = 0
        maxrel = []
        for rel in releaseList:
            if(rel.getEpisodeCount() >= max):
                max = rel.getEpisodeCount()
                maxrel.append(rel)
        return self.getBestReleaseByQuality(maxrel)


    def getName(self):
        if(self.gerName != ""):
            return self.gerName
        elif(self.engName != ""):
            return self.engName
        else:
            return self.japName

    def getNameGerman(self):
        return self.gerName

    def getNameJapanese(self):
        if(self.japName != ""):
            return self.japName
        else:
            return self.getName()

    def getNameEnglish(self):
        if(self.engName != ""):
            return self.engName
        else:
            return self.getName()

    def getURL(self):
        return self.url

    def getIdentifier(self):
        return self.url.split("/")[-1]

    def getRuntime(self):
        return self.runtime

    def getType(self):
        return self.type

    def getSynonymes(self):
        return self.synonymes
    
    def getYear(self):
        return self.year

    def getCurrentEpisodes(self):
        return self.curEpisodes
    
    def getMaxEpisodes(self):
        return self.maxEpisodes

    def getStatus(self):
        return self.status

    def getMainGenre(self):
        return self.mainGenre

    def getSideGenres(self):
        return self.sideGenres
    
    def getTags(self):
        return self.tags

    def getReleases(self):
        return self.releases

    def getRelease(self, releaseID):
        return self.releases[releaseID-1]


    def tostring(self):
        return str("[Jap/Ger/EngName]: " + self.japName + "/" + self.gerName + "/" + self.engName + ", [Synonyms]: " + str(self.synonymes) + ", [Type]: " + \
            self.type + ", [Episodes]: " + str(self.curEpisodes) + "/" + str(self.maxEpisodes) + ", [Status]: " + self.status + ", [Year]: " + str(self.year) \
                + ", [Maingenre]: " + self.mainGenre + ", [Sidegenres]: " + str(self.sideGenres) + ", [Tags]: " + str(self.tags))


    def downloadEpisode(self, episode, release, hoster, browser, browserlocation="", jdhost="", myjd_user="", myjd_pw="", myjd_device="", pkgName=""):
        if(str(browser).isnumeric() == False):
            if("firefox" in browser.lower()):
                browser = animeloads.FIREFOX
            elif("chrome" in browser.lower()):
               browser = animeloads.CHROME
            else:
                raise ALInvalidBrowserException("Nicht unterstützter Browser: " + str(browser))
        if(str(hoster).isnumeric() == False):
            if("uploaded" in hoster.lower()):
                hoster = animeloads.UPLOADED
            elif("ddownload" in hoster.lower()):
                hoster = animeloads.DDOWNLOAD
            elif("rapidgator" in hoster.lower()):
                hoster = animeloads.RAPIDGATOR
            else:
                raise ALInvalidHosterException("Nicht unterstützter Hoster: " + str(hoster))

        anime_identifier = self.url.split("/")[len(self.url.split("/"))-1] #Name of Anime, used for POST Request
        try:
            episodeStr = str(int(episode)-1)
        except:
            episodeStr = "cnl"
        if(int(episode) <=0):
            episodeStr = "\"cnl\""
        unenc_request = "[\"media\",\"" + anime_identifier + "\",\"downloads\"," + str(release.getID()) + "," + episodeStr + "]"
        dbgprint("Download request:")
        dbgprint(unenc_request)
        #print(unenc_request)
        b64 = base64.b64encode(unenc_request.encode("ascii"))
        data = {"enc": b64,
       "response": "nocaptcha"}

        ######################################
        #Requests code ohne benötigten Browser, wird allerdings als adblock erkannt
        ######################################


#        headers = {
#        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
#        "Referer": self.url,
#        "Accept": "application/json, text/javascript, */*; q=0.01",
#        "Accept-Language": "en-US,en;q=0.5",
#        "Connection": "keep-alive",
#        "Content-Length": "83",
#        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#        "TE": "Trailers",
#        "X-Requested-With": "XMLHttpRequest",
#        "Cookie": "ci_session=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%227fda60af7999159425b7143f63cd5202%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2289.244.161.10%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A94%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%3B+rv%3A78.0%29+Gecko%2F20100101+Firefox%2F78.0+Waterfox%2F78.7.0%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1612911522%3B%7D3a772b4afefd4887a6eba3fffd868265c5769de6"
#        }

#        print("Session Cookies: " + str(cock))
#        r = requests.post("https://webhook.site/75132056-b86a-4285-ab83-2cf785a202a1", data=data, headers=headers)
#        rad = self.session.get("https://www.anime-loads.org/assets/pub/js/ads.com/ads.js?cb=13881964231")
#        print(rad.text)
#        print(rad.status_code)
#        print(rad.cookies)
#        r = self.session.post("https://www.anime-loads.org/ajax/captcha", data=data)
#        print(r.text)
#        r.raw.decode_content = True
#        print("Response: " + str(r.text))
#        cock = [
#            {'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path}
#            for c in self.session.cookies
#        ]
#        print("d_Cock: " + str(cock))
#        print("\n\n\n\ndl_Other cookies: " + str(r.cookies))


        ############################################################################
        #Solange wird dieser Code benutzt, benötigt einen Browser, funktioniert aber
        ############################################################################

        #Create Headless browser to bypass adblock detection
        if(browser == animeloads.CHROME):
            options = selenium.webdriver.chrome.options.Options()
            options.headless = True
            if(browserlocation != ""):
                options.binary_location = browserlocation
            driver = webdriver.Chrome(service_log_path=os.devnull, options=options)
        elif(browser == animeloads.FIREFOX):
            options = selenium.webdriver.firefox.options.Options()
            options.headless = True
            if(browserlocation != ""):
                options.binary_location = browserlocation
            driver = webdriver.Firefox(service_log_path=os.devnull, options=options)
        else:
            raise ALInvalidBrowserException("Nicht unterstützter Browser")

        #Erster besuch auf der Seite, damit cookies hinzugefügt werden können
        driver.get("https://www.anime-loads.org/assets/pub/images/logo.png")

        #Login cookies auf Selenium übertragen
        for c in self.session.cookies:
            driver.add_cookie({'name': c.name, 'value': c.value})

        driver.get(self.url)


        #JS to make post request to get URLs
        js = "var xhr = new XMLHttpRequest(); \
xhr.open('POST', 'https://www.anime-loads.org/ajax/captcha', false); \
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded'); \
xhr.send('enc=" + b64.decode('ascii') + "&response=nocaptcha'); \
return xhr.response"

        ajaxresponse = driver.execute_script(js)

        code = ""
        message = ""
        reflinks = ""
        content_uploaded = ""
        content_ddl = ""
        content_rapid = ""

        response_json = json.loads(ajaxresponse)

        dbgprint(response_json)

        for key in response_json:
            value = response_json[key]
            if(key == "code"):
                code = value
            elif(key == "message"):
                message = value
            elif(key == "reflink"):
                reflinks = value
            elif(key == "content"):
                try:
                    content_uploaded = value[0]
                except:
                    pass
                try:
                    content_ddl = value[1]
                except:
                    pass
                try:
                    content_rapid = value[2]
                except:
                    pass

        if(episodeStr == "cnl" and code == "error" and message == "Unknown Error"):
            print("Probably no CNL available, downloading episode 1 instead (Movies etc...)")
            driver.quit()
            return self.downloadEpisode(1, release, hoster, browser, browserlocation, jdhost, myjd_user, myjd_pw, myjd_device, pkgName)
            
        tries = 0
        while(code != "success" and ("noadblock" in message or "The captcha ID was invalid." in message) and tries < 5):
            print("Need to solve a captcha")
            cID = ""
            response_json = utils.doCaptcha(cID, driver, self.session, b64)
            if response_json == False:
                raise ALUnknownException("Ein unbekannter Fehler beim lesen der Hosterlinks aufgetreten, möglicherweise serverseitig.")
            for key in response_json:
                value = response_json[key]
                if(key == "code"):
                    code = value
                elif(key == "message"):
                    message = value
                elif(key == "reflink"):
                    reflinks = value
                elif(key == "content"):
                    try:
                        content_uploaded = value[0]
                    except:
                        pass
                    try:
                        content_ddl = value[1]
                    except:
                        pass
                    try:
                        content_rapid = value[2]
                    except:
                        pass
            if(episodeStr == "cnl" and code == "error" and message == "Unknown Error"):
                print("Probably no CNL available, downloading episode 1 instead (Movies etc...)")
                driver.quit()
                return self.downloadEpisode(1, release, hoster, browser, browserlocation, jdhost, myjd_user, myjd_pw, myjd_device, pkgName)
            tries += 1
            time.sleep(5)
            
#            raise ALCaptchaException("Captcha is needed to get download links")

        if(code == "error"):
            if(message == "cnl_login"):
                print("Not logged in and tried to download CNL")
                print("Trying to log in again")
                try:
                    self.animeloads.login(self.animeloads.user, self.animeloads.pw)
                except:
                    print("Failed to login, exiting...")
                    raise ALNotLoggedInException("Um CNLs laden zu können, muss man angemeldet sein")
                

        if(code != "success"):
            dbgprint("Code: " + code)
            dbgprint("Message: " + message)
            raise ALUnknownException("Ein unbekannter Fehler beim lesen der Hosterlinks aufgetreten, möglicherweise serverseitig oder das Captcha konnte nach 5 Versuchen nicht gelöst werden.")

        driver.quit()

        reflinks = ""
        k = ""
        jk = ""
        crypted = ""


        if(hoster == animeloads.DDOWNLOAD):
            cnldata = content_ddl
        elif(hoster == animeloads.RAPIDGATOR):
            cnldata = content_rapid
        else:
            cnldata = content_uploaded

        dbgprint("CNLdata: ")
        dbgprint(cnldata)

        for key in cnldata:
            value = cnldata[key]
            if(key == "links"):
                reflinks = value
            elif(key == "cnl"):
                try:
                    k = value['jk']
                except:
                    raise ALLinkExtractionException("AES-Key konnte nicht gelesen werden")
                try:
                    crypted = value['crypted']
                except:
                    raise ALLinkExtractionException("Linkdaten konnten nicht gelesen werden")

        k_list = list(k)
        dbgprint("k: ")
        dbgprint(k)
        dbgprint("klist: ")
        dbgprint(k_list)
        tmp = k_list[15]
        k_list[15] = k_list[16]
        k_list[16] = tmp
        k = "".join(k_list)

        jk = "function f(){ return \'" + k + "\';}"

        if(pkgName == ""):
            pkgName = anime_identifier

        if(jdhost != "" and myjd_user == ""):
            return utils.addToJD(jdhost, release.getPassword(), self.url, crypted, jk)
        elif(jdhost == "" and myjd_user != ""):
            links_decoded = utils.decodeCNL(k, crypted)
            links = []
            linkstring = ""
            for link in links_decoded:
                linkstring += link.decode('ascii')
            myjd_return = utils.addToMYJD(myjd_user, myjd_pw, myjd_device, linkstring, pkgName, release.getPassword())
            try:
                pkgID = myjd_return['id']
                return True
            except Exception as e:
                print(e)
                return False
        else:
            links_decoded = utils.decodeCNL(k, crypted)
            links = []
            for link in links_decoded:
                links.append(link.decode('ascii'))
            return links
        

class episode:
    def __init__(self, episodenumber, episodename):
        self.episodenumber = episodenumber
        try:
            self.episodename = episodename.replace("ü", "ue").replace("ö", "oe").replace("ä", "ae")
        except Exception as e:
            print(e)
            self.episodename = ""
        #print("Episode " + str(self.episodenumber) + ": " + self.episodename)

    def getEpisodeNumber(self):
        return self.episodenumber

    def getEpisodeName(self):
        return self.episodename

class release:

    @staticmethod
    def parseAudioCodec(anmerkung):
        if(anmerkung == ""):
            return ""
        formats = ["PCM", "FLAC", "DTS", "AC3", "AAC", "MP3"]
        format = "UNKNOWN"
        for f in formats:
            if(f in anmerkung.upper()):
                format = f
        return format

    @staticmethod
    def parseVideoCodec(anmerkung):
        if(anmerkung == ""):
            return ""
        codecs = ["x264", "x265", "xvid"]
        codec = "UNKNOWN"
        for c in codecs:
            if(c in anmerkung.lower()):
                codec = c
        return codec

    def __init__(self, url, rid, group, res, dubs, subs, episodeCount, videoformat, size, password, episodes, anmerkung="", sitesource="", session=""):   #TODO sortieren
        self.url = url
        self.rid = rid
        self.group = group
        self.res = res
        self.audiocodec = self.parseAudioCodec(anmerkung)
        self.dubs = dubs
        self.subs = subs
        self.videoformat = videoformat
        self.size = size
        self.episodeCount = episodeCount
        self.password = password
        self.episodes = episodes
        self.videocodec = self.parseVideoCodec(anmerkung)
        self.anmerkung = anmerkung
        self.sitesource = sitesource
        self.session = session

    def getID(self):
        return self.rid

    def getGroup(self):
        return self.group

    def getResolution(self):
        return self.res
        
    def getAudioCodec(self):
        return self.audiocodec

    def getDubs(self):
        return self.dubs

    def getSubs(self):
        return self.subs

    def getVideoFormat(self):
        return self.videoformat
    
    def getSize(self):
        return self.size
    
    def getPassword(self):
        return self.password

    def getAnmerkung(self):
        return self.anmerkung

    def getVideoCodec(self):
        return self.videocodec

    def tostring(self):
        return "Release ID: " + str(self.rid) + ", Group: " + self.group + ", Resolution: " + self.res + ", Videocodec: " + self.videocodec + ", Audiocodec: " + self.audiocodec + ", Dubs: " + str(self.dubs) + \
            ", Subs: " + str(self.subs) + ", Format: " + self.videoformat + ", Size: " + str(self.size) + "MB, Password: " + self.password

    def getEpisodeCount(self):
        return self.episodeCount

    def hasEpisode(self, episode):
        zint = len(str(self.getEpisodeCount()))
        for ep in self.episodes:
            if(ep.getEpisodeNumber() == episode or ("Episode " + str(episode).zfill(zint)) in ep.getEpisodeName()):
                dbgprint("Found episode: " + str(ep.getEpisodeNumber()) + ": " + ep.getEpisodeName())
                return True
        return False

    def getEpisodes(self, episode):
        zint = len(str(self.getEpisodeCount()))
        episodes = []
        for ep in self.episodes:
            if(ep.getEpisodeNumber() == episode or ("Episode " + str(episode).zfill(zint)) in ep.getEpisodeName()):
                dbgprint("Found episode: " + str(ep.getEpisodeNumber()) + ": " + ep.getEpisodeName())
                episodes.append(ep)
        return episodes

    def getEpisodeTitle(self, episode):
        for ep in self.episodes:
            if(ep.getEpisodeNumber() == episode):
                return ep.getEpisodeName()
        return ""
        


#Exceptions
class ALCaptchaException(Exception):
    pass

class ALInvalidBrowserException(Exception):
    pass

class ALInvalidHosterException(Exception):
    pass

class ALLinkExtractionException(Exception):
    pass

class ALInvalidLoginException(Exception):
    pass

class ALUnknownException(Exception):
    pass
