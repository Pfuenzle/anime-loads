# -*- coding: utf-8 -*-

import hashlib
import random
import re
import string
import time
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from config import *
from DetailedSearch import DetailedSearchRelease

from animeloads import animeloads, utils

#TODO Multithreading
#TODO caching
#TODO rss

####################################


####################################
alapi = ""
tries = 0
maxLoginTries = 3
while(alapi == "" and tries < maxLoginTries):
    try:
        tries += 1
        alapi = animeloads(user=ALUsername, pw=ALPassword, browser=animeloads.CHROME, cacheTime=cacheTime)
        print("Logged in as " + alapi.username)
    except:
        print("Failed to login, trying " + str(maxLoginTries-tries) + " more times.")

if(alapi == ""):
    alapi = animeloads(browser=animeloads.CHROME, cacheTime=cacheTime)
    print("Login failed " + str(maxLoginTries) + " times, using anonymous account")

def getDownloadPath(webserver, releaseTitle):
    appendix = ""
    if(isSonarr(webserver)):
        print("Requesting Server is Sonarr, setting Directory")
        return sonarrPath + "/" + releaseTitle
    elif(isRadarr(webserver)):
        print("Requesting Server is Radarr, setting Directory")
        return radarrPath + "/" + releaseTitle
    raise UnsupportedPVRException("Unsupported PVR")

def isSonarr(webserver):
    if("Sonarr" in str(webserver.headers)):
        return True
    return False

def isRadarr(webserver):
    if("Radarr" in str(webserver.headers)):
        return True
    return False

def cleanString(inputstring):
    print("a" + inputstring)
    inputstring = inputstring.replace("é", "e")
    retstring = inputstring.encode('ascii', 'ignore').decode('utf-8', 'ignore')
    print("b" + retstring)
    return retstring

def generateNZBData(anime="", releaseTitle="", releaseID=-1, episode=-1):
    releaseTitle = cleanString(releaseTitle)
    if(releaseTitle=="" and releaseID==-1 and episode==-1 and anime != ""):
        releaseTitle = anime.releaseTitle
        releaseID = anime.releaseID
        episode = anime.episode
        logstr = "Generating nzb data for " + releaseTitle + ", Release " + str(releaseID)
        if(episode != -1):
            logstr = logstr + ", Episode " + str(episode)
        print(logstr)
    elif(releaseTitle!="" and releaseID!=-1 and episode!=-1):
        logstr = "Generating nzb data for " + releaseTitle + ", Release " + str(releaseID)
        if(episode != -1):
            logstr = logstr + ", Episode " + str(episode)
        print(logstr)
    else:
        return ""
    nzbdata = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nzb PUBLIC "-//newzBin//DTD NZB 1.1//EN" "http://www.newzbin.com/DTD/nzb/nzb-1.1.dtd">
<nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">

<file poster="%s" date="%s" subject="%s">
 <groups>
  <group>alt.anime.loads</group>
 </groups>
 <segments>
  <segment bytes="564" number="1">VmqtuNlXw5lNh0uaBVgS1_1o3@JBinUp.local</segment>
 </segments>
</file>
</nzb>""" % (releaseTitle, str(releaseID), str(episode))
    return nzbdata

def parseURLArgs(path):
    URL = "http://0.0.0.0" + path
    parsed_url = urlparse(URL)
    args = parse_qs(parsed_url.query)
    return args

categoryMapping = [["2000", "Movie"], ["5000", "Series"], ["100001", "Bonus"], ["100002", "Live-Action"], ["100003", "OVA"], ["100004", "Special"], ["100005", "Web"]]

def getCaps():
    caps = """<?xml version="1.0" encoding="UTF-8"?>
  <caps>
    <!-- server information -->
    <server version="1.0" title="Anime-Loads" strapline="Anime-Loads Indexer Proxy"
            email="pfuenzle@protonmail.com" url="https://www.anime-loads.org/"
            image="https://www.anime-loads.org/assets/pub/images/logo.png"/>

    <!-- limit parameter range -->
    <limits max="100" default="50"/>

    <!-- the server NZB retention -->
    <retention days="50000"/>

    <!-- registration available or not -->
    <registration available="no" open="no" />

        <searching>
        <search available="yes" supportedParams="q,season,ep"/>
        <tv-search available="yes" supportedParams="q,season,ep" />
         <movie-search available="yes" supportedParams="q" />
    </searching>

    <!-- supported categories -->
    <categories>

        <category id="2000" name="Movies"/>
        <category id="5000" name="TV">
          <subcat id="100001" name="Bonus"/>
          <subcat id="100002" name="Live-Action"/>
          <subcat id="100003" name="OVA"/>
          <subcat id="100004" name="Special"/>
          <subcat id="100005" name="Web"/>
        </category>
    </categories>
  </caps>"""
    return caps


def animeToItem(anime, episode):
    nzburl = externPath + "/api?t=download&anime=" + anime.url.split("/")[-1] + "&release=" + str(anime.releaseID)
    if(anime.episode != -1):
        nzburl = nzburl + "&episode=" + str(episode)
    nzburl = nzburl + "&releasetitle=" + anime.releaseName
    nzbdata = generateNZBData(anime)
    item = """<item>
	<title>%s</title>
	<guid isPermaLink="true">%s</guid>
	<link>TEST123TODO</link>
	<comments>%s</comments> 	
	<pubDate>Mon, 06 Dec 2021 %s:%s:%s +0100</pubDate> 
	<category>Anime-Loads</category> 	
	<description>%s</description>
	<enclosure url="%s" length="%s" type="application/x-nzb" />

	<newznab:attr name="category" value="5000" />
	<newznab:attr name="category" value="2000" />
	<newznab:attr name="size" value="%s" />
	<newznab:attr name="guid" value="%s" />
	<newznab:attr name="files" value="25" />
	<newznab:attr name="poster" value="%s@anime-loads.org" />
	<newznab:attr name="tvdbid" value="412252" />
	<newznab:attr name="grabs" value="0" />
	<newznab:attr name="comments" value="0" />
	<newznab:attr name="password" value="0" />
	<newznab:attr name="nfo" value="0" />
	<newznab:attr name="usenetdate" value="Mon, 06 Dec 2021 22:00:41 +0100" />
	<newznab:attr name="group" value="alt.anime.pfuenzle" />

</item>""" % (cleanString(anime.releaseTitle), anime.url + "/" + hashlib.md5(anime.releaseTitle.encode('utf-8')).hexdigest(), anime.url, str(random.randint(0, 24)).zfill(2), str(random.randint(0, 60)).zfill(2), str(random.randint(0, 60)).zfill(2), cleanString(anime.releaseTitle), nzburl, len(nzbdata), int(anime.size * 1000000), uuid.uuid4().hex, uuid.uuid4().hex)
    return item #TODO files
#	<newznab:attr name="season" value="S01" />

def detailResultsToXML(detailedResults, baseURL, episode, useAnimeProfile, season=-1):
    global keepWrongSeasons

    releasestring = ""
    print("KEEP")
    print(keepWrongSeasons)
    print(useAnimeProfile)

    for det in detailedResults:
        if(keepWrongSeasons == False and useAnimeProfile == False):
            isSeason = det.seasonInt
            wantSeason = season
            print(det.releaseTitle)
            if(wantSeason == -1 or isSeason == -1):
                print("Release is Season " + str(isSeason) + ", and want " + str(wantSeason) + ", adding unknown to results")
                releasestring += animeToItem(det, episode) + "\n"
            elif(wantSeason == isSeason):
                releasestring += animeToItem(det, episode) + "\n"
                print("Release is Season " + str(isSeason) + ", and want " + str(wantSeason) + ", adding to results")
            else:
                print("Release is Season " + str(isSeason) + ", but want " + str(wantSeason) + ", removing from results")
        else:
            releasestring += animeToItem(det, episode) + "\n"
    
    responseXML = """<?xml version="1.0" encoding="utf-8" ?> 
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:newznab="http://www.newznab.com/DTD/2010/feeds/attributes/">
<channel>
<atom:link href="%s" rel="self" type="application/rss+xml" />
<title>Anime-Loads</title>
<description>Anime-Loads Feed</description>
<link>https://www.anime-loads.org/</link>
<language>de-de</language>
<webMaster>pfuenzle@protonmail.com</webMaster>
<category></category>
<image>
	<url>https://www.anime-loads.org/assets/pub/images/logo.png</url>
	<title>Anime-Loads</title>
	<link>https://www.anime-loads.org/</link>
	<description>Anime-Loads</description>
</image>

<newznab:response offset="0" total="%s" />
%s</channel>
</rss>""" % (baseURL, str(len(detailedResults)), releasestring)
    responseXML = responseXML.replace("&", "&amp;")
#    s = open("out.txt", "w")
#    s.write(responseXML)
#    s.close()
    return responseXML


def search(series, baseURL, webserver, cats, episode=-1, useAnimeProfile=False, season=-1):
    global resultrange
    resrange = resultrange
    if(episode != -1):
        print("Searching for season of " + series + " with episode " + str(episode))
    else:
        print("Searching for season of " + series)
    searchresults = alapi.search(series)
    detailedResults = []
    print("Number of Results: " + str(len(searchresults)))
    print("Results: ")
    if(len(searchresults) < resrange):
        resrange = len(searchresults)

    for i in range(0, resrange):
#        print(searchresults[i].tostring())
        anime = searchresults[i].getAnime()

        doSkip = True

        animeCat = anime.getType()
        
        if(len(cats) == 0):
            print("No Categorie set, skipping everything")
            continue
        else:
            for cat in cats:
                if(doSkip == False):
                    break
                if(cat == "2000"):#Category is TV, include everything below
                    for idx,catMapping in enumerate(categoryMapping):
                        if(idx == 0):
                            continue
                        if(catMapping[1] == animeCat):
                            print("Category of " + anime.getName() + " (" + anime.getType() + ") is requested")
                            doSkip = False
                            break
                for idx,catMapping in enumerate(categoryMapping):
                    if(catMapping[0] == cat):
                        if(animeCat == catMapping[1]):
                            print("Category of " + anime.getName() + " (" + anime.getType() + ") is requested")
                            doSkip = False
                            break
        if(doSkip):
            print("Skipped " + anime.getName() + " as its category " + anime.getType() + " is not requested")
            continue
        
        releases = anime.getReleases()
        dubLang = "Japanese"
        subLang = ""
        for rel in releases:
            animeNameGer = str(anime.getName())
            animeNameEng = str(anime.getNameEnglish())
            print("Anime: " + animeNameGer)
            print("Release: " + str(rel.getID()))
            if(episode != -1):
                if(rel.hasEpisode(episode)):
                    print("Anime has requested episode, adding")
                    episodes = rel.getEpisodes(episode)
                else:
                    episodes = []
            if("Deutsch" in rel.getDubs()):
                if(len(rel.getDubs()) == 2):
                   dubLang = "German DL"
                elif(len(rel.getDubs()) > 2):
                   dubLang = "German ML"
                else:
                    dubLang = "German"
            elif("Deutsch" in rel.getSubs()):
                subLang = "GerSub"
            elif("Englisch" in rel.getDubs()):
                dubLang = "English"
            else:
                try:
                    subLang = rel.getSubs()[0] + " Subbed"
                except:
                    subLang = ""
            singleSize = float(rel.getSize())
            fullSize = float(rel.getSize()) * rel.getEpisodeCount()
            if(episode == -1):
                detail = DetailedSearchRelease(animeNameEng, rel.getID(), rel.getAnmerkung(), rel.getGroup(), rel.getResolution(), dubLang, rel.getDubs(), subLang, rel.getSubs(), fullSize, anime.getURL(), rel.getEpisodeCount(), anime.getMaxEpisodes(), anime.getSynonymes(), anime.getType(), anime.getYear())    #TODO check if release is complete
                detailedResults.append(detail)
                print("Added complete Season")
            else:
                if(useAnimeProfile):
                    detail = DetailedSearchRelease(animeNameEng, rel.getID(), rel.getAnmerkung(), rel.getGroup(), rel.getResolution(), dubLang, rel.getDubs(), subLang, rel.getSubs(), fullSize, anime.getURL(), rel.getEpisodeCount(), anime.getMaxEpisodes(), anime.getSynonymes(), anime.getType(), anime.getYear())    #TODO check if release is complete
                    detailedResults.append(detail)
                    print("Added complete Season as search is using Anime Profile")
                for ep in episodes:
                    detail = DetailedSearchRelease(animeNameEng, rel.getID(), rel.getAnmerkung(), rel.getGroup(), rel.getResolution(), dubLang, rel.getDubs(), subLang, rel.getSubs(), singleSize, anime.getURL(), rel.getEpisodeCount(), anime.getMaxEpisodes(), anime.getSynonymes(), anime.getType(), anime.getYear(), ep.getEpisodeNumber(), ep.getEpisodeName())    #TODO check if release is complete
                    detailedResults.append(detail)
                    print("Added Episode " + str(ep.getEpisodeNumber()) + ":" + ep.getEpisodeName())
            print("Current episodes of Release: " + str(rel.getEpisodeCount()))
            print("\n\n")

    for d in detailedResults:
        print(d.releaseTitle)

    print("Number of remaining results: " + str(len(detailedResults)))
    if(len(detailedResults) == 0):
        return getTestResponse()
    return detailResultsToXML(detailedResults, baseURL, episode, useAnimeProfile, season)
    
def getFunction(args):
    try:
        func = args["t"][0]
    except:
        func = ""
    return func

def sendResponse(server, response, content_type="text/xml", status_code=200):
    out = open("lastresponse.txt", "w")
    cleanedResponse = cleanString(response)
    out.write(cleanedResponse)
    out.close()
    server.send_response(status_code)
    server.send_header("Content-type", content_type)
    server.send_header("Content-Length", str(len(bytes(response, "utf-8"))))
    server.end_headers()
    server.wfile.write(bytes(response, "utf-8"))

def getRSSResponse():      #TODO replace with RSS
    testfile = open("testdata.xml", "r")
    testdata = testfile.read()
    testfile.close()
    return testdata

def sendRSSResponse(serverInstance):       #basically RSS, so TODO
    rssdata = getRSSResponse()
    sendResponse(serverInstance, rssdata)

def sendEmptyResults(serverInstance):
    emptydata = """<?xml version="1.0" encoding="utf-8" ?> 
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:newznab="http://www.newznab.com/DTD/2010/feeds/attributes/">
<channel>
<atom:link href="%s" rel="self" type="application/rss+xml" />
<title>Anime-Loads</title>
<description>Anime-Loads Feed</description>
<link>https://www.anime-loads.org/</link>
<language>de-de</language>
<webMaster>pfuenzle@protonmail.com</webMaster>
<category></category>
<image>
	<url>https://www.anime-loads.org/assets/pub/images/logo.png</url>
	<title>Anime-Loads</title>
	<link>https://www.anime-loads.org/</link>
	<description>Anime-Loads</description>
</image>

<newznab:response offset="0" total="0" />
</channel>
</rss>""" % (baseURL, str(len(detailedResults)))
    responseXML = responseXML.replace("&", "&amp;")
    serverInstance.send_response(200)
    serverInstance.send_header("Content-type", "text/xml")
    serverInstance.send_header("Content-Length", str(len(emptydata)))
    serverInstance.end_headers()
    serverInstance.wfile.write(bytes(emptydata, "utf-8"))

def getQuery(args):
    try:
        search = args["q"][0]
    except:
        search = ""
    try:
        rid = args["rid"][0]
    except:
        rid = ""
    try:
        cats = args["cat"][0]
    except:
        cats = ""
    return search, rid, cats

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        baseURL = "http://" + hostName + ":" + str(serverPort) + path
        args = parseURLArgs(path)
        print("Got request with " + str(args))
        function = getFunction(args)
        useAnimeProfile = False
        if(function == "caps"):
            print("Function: caps")
            response = getCaps()
            sendResponse(self, response)
        elif(function == "download"):
            print("Function: " + function)
            try:
                anime = args['anime'][0]
                release = args['release'][0]
                releaseTitle = args['releasetitle'][0]
            except Exception as e:
                print(e)
                print("Invalid donwload request.")
                print("Args:")
                print(args)
                return
            try:
                episode = args['episode'][0]
            except:
                episode = "-1"
            if(episode == "-1" and alapi.username == "anonymous"):
                print("Cant download complete season, need to be logged in for this action")
                sendResponse(self, "")
                return
            #ADD TO JD
            animeobject = alapi.getAnime("https://www.anime-loads.org/media/" + anime)
            releaseobject = animeobject.getRelease(int(release))
            links = animeobject.downloadEpisode(episode, releaseobject, hoster, browser)
            linkstring = ""
            for link in links:
                linkstring += link
            tries = 0
            success = False
            while(success == False and tries <= JDownloaderRetries):
                try:
                    if(int(episode)>=1):
                        episodeStr = str(episode)
                    else:                                    
                        episodeStr = "cnl"
                    retvalue = utils.addToMYJD(jdemail, jdpassword, jdname, linkstring, re.sub('[^.,a-zA-Z0-9 \n\.]', '', releaseTitle), releaseobject.getPassword(), destination=getDownloadPath(self, re.sub('[^.,a-zA-Z0-9 \n\.]', '', releaseTitle)))
                    if(retvalue == False):
                        raise Exception
                    print("JD Returnvalue: " + str(retvalue))
                    success= True
                except Exception as e:
                    print("Failed to add")
                    print(e)
                    tries += 1
            if(success == False):
                print("Failed to add Download to JD, not trying again...")
                sendResponse(self, "")
            else:
                print("Episode successfully added to JD")
                response = generateNZBData("", anime, release, episode)
                sendResponse(self, response)
        elif(function == "tvsearch" or function == "search" or function == "movie"):
            print("Function: " + function)
            query, rid, cats = getQuery(args)
            cats = cats.split(",")
            if(query == "" and rid == ""):
                print("Received empty query (very likely Sonarr/Radarr RSS), sending testdata back")
                response = sendRSSResponse(self)
                return
            if(rid != ""):
                sendEmptyResults(self)
                return
            try:
                episode = args["ep"][0]
            except:
                episode = ""
            try:
                season = int(args["season"][0])
            except:
                season = -1
            if(season == 0):
                query = query + " OVA"
            if(function == "search"):
                print("Got search, so use Anime profile")
                useAnimeProfile = True
                if(isRadarr(self)):
                    print("Search is from Radarr, omitting Year if needed")
                    if(query[-4].isnumeric()):
                        query = query[:-5]
                    if(query[-1] == "0"):
                        query = query[:-2]
                else:
                    tmpquery = query.split(" ")[:-1]
                    newquery = ""
                    for idx, t in enumerate(tmpquery):
                        newquery = newquery + t
                        if(len(tmpquery)-1 != idx):
                            newquery = newquery + " "
                    episode = query.split(" ")[-1]
                    if(episode.isnumeric() == False):
                        episode = 1
                    else:
                        query = newquery
                print("New query: " + query + ", episode: " + str(episode))
            if(episode != ""):
                response = search(query, baseURL, self, cats, int(episode), useAnimeProfile=useAnimeProfile, season=season)
            else:
                response = search(query, baseURL, self, cats, useAnimeProfile=useAnimeProfile, season=season)
            sendResponse(self, response)
        else:
            print("Invalid function: " + str(function))
            response = ""
            sendResponse(self, response, status_code=404)


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

class UnsupportedPVRException(Exception):
    pass
