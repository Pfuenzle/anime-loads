import time
import sys, os

import json

from animeloads import animeloads
from animeloads import ALCaptchaException

import selenium

arglen = len(sys.argv)

def compare(inputstring, validlist):
    for v in validlist:
        if(v.lower() in inputstring.lower()):
            return True
    return False

def settings():
    try:
        file = open("settings.json", "r")
        jdata = json.load(file)
        for key in jdata:
            if(key == "jdhost"):
                jdhost = jdata[key]       
            if(key == "mode"):
                mode = jdata[key]
            if(key == "hoster"):
                hoster = jdata[key]
            if(key == "browserengine"):
                browserengine = jdata[key]
            if(key == "browserlocation"):
                browserlocation = jdata[key]
        file.close()
    except:
        jdhost = ""
        mode = ""
        hoster = ""
        browserengine = ""
        browserlocation = ""

    if(hoster == 1):
        hosterstr = "ddownload"
    elif(hoster == 0):
        hosterstr = "uploaded"
    changehoster  = True
    if(hoster != ""):
        if(compare(input("Dein gewählter hoster: " + hosterstr + ", möchtest du ihn wechseln? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
            changehoster = False
    if(changehoster):
        while(True):
            host = input("Welchen hoster bevorzugst du? uploaded oder ddownload: ")
            if("uploaded" in host):
                hoster = animeloads.UPLOADED
                break
            elif("ddownload" in host):
                hoster = animeloads.DDOWNLOAD
                break
            else:
                print("Bitte gib entweder uploaded oder ddowwnload ein")

    changemode = True
    if(mode != ""):
        if(compare(input("Dein gewählter modus: " + mode + ", möchtest du ihn wechseln? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
            changemode = False

    if(changemode):
        if(compare(input("Möchtest du Jdownloader2 nutzen? Andernfalls werden die Links in der Konsole zurückgegeben [J/N]: "), {"j", "ja", "yes", "y"})):
            if(input("Läuft dein JD2 auf deinem Lokalen Computer? Dann Eingabe leer lassen und bestätigen, falls nicht, gib die Adresse des Zeilrechners an: ") != ""):
                jdhost = input
            else:
                jdhost = "127.0.0.1"
            mode = "jdownloader"
        else:
            print("Gebe links in Console aus...")
            mode = "console"

    if(browserengine == 0):
        browserstring = "Firefox"
    elif(browserengine == 1):
        browserstring = "Chrome"

    changebrowser = True
    if(browserengine != ""):
        if(compare(input("Dein gewählter Browser: " + browserstring + ", möchtest du ihn wechseln? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
            changebrowser = False
    if(changebrowser):
        while(True):
            browser = input("Welchen Browser möchtest du nutzen? Darunter fallen auch forks der jeweiligen Browser (Chrome/Firefox)? Achte darauf, dass Chromedriver (Chrome) oder Geckodriver (Firefox) im gleichen Ordern wie das Script liegt: ")
            if(browser == "Chrome"):
                browserengine = animeloads.CHROME
                break
            elif(browser == "Firefox"):
                browserengine = animeloads.FIREFOX
                break
            else:
                print("Fehlerhafter Input, entweder Chrome oder Firefox")
                
        if(compare(input("Ist dein Browser ein fork von chrome/firefox oder an einem anderen als dem standardpfad installiert? [J/N]: "), {"j", "ja", "yes", "y"})):
            browserlocation = input("Dann gib jetzt den Pfad der Browserdatei an (inklusive Endung): ")

    data = {
        "hoster": hoster,
        "browserengine": browserengine,
        "mode": mode,
        "browserlocation": browserlocation,
        "jdhost": jdhost
        }

    jdata = json.dumps(data)

    file = open("settings.json", "w")
    file.write(jdata)
    file.close()

def loadSettings():
    file = open("settings.json", "r")
    jdata = json.load(file)
    for key in jdata:
        if(key == "jdhost"):
            jdhost = jdata[key]       
        if(key == "mode"):
            mode = jdata[key]
        if(key == "hoster"):
            hoster = jdata[key]
        if(key == "browserengine"):
            browserengine = jdata[key]
        if(key == "browserlocation"):
            browserlocation = jdata[key]
    file.close()
    return jdhost, mode, hoster, browserengine, browserlocation

def interactive():
    al = animeloads()

    mode = ""

    while(mode == ""):
      
        try:
            jdhost, mode, hoster, browserengine, browserlocation = loadSettings()
        except:
            print("Du hast noch keine Einstellungen festgelegt")
            settings()

    if(compare(input("Möchtest du dich anmelden? [J/N]: "), {"j", "ja", "yes", "y"})):
        user = input("Username: ")
        password = getpass("Passwort: ")
        try:
            al.login(user, password)
        except:
            print("Fehlerhafte Anmeldedaten, fahre mit anonymen Account fort")
    else:
        print("Überspringe Anmeldung")
        
    print("Angemeldet als Nutzer " + al.username + ", VIP: " + str(al.isVIP))

    if(compare(input("Möchtest du deine Einstellungen ändern? [J/N]: "), {"j", "ja", "y", "yes"})):
        settings()
        jdhost, mode, hoster, browserengine, browserlocation = loadSettings()

    exit = False
    search = False

    while(exit == False):
        search = False
        aniquery = input("Nach welchem Anime möchtst du suchen? (Du kannst jederzeit \"suche\" eingeben, um zurück zur Suche zu kommen oder \"exit\", um das Programm zu beenden): ")
        if(aniquery == "exit"):
            break
        elif(aniquery != "suche"):
            results = al.search(aniquery)
        
            if(len(results) == 0):
                print("Keine Ergebnisse")
                search = True
                break

            print("Ergebnisse: ")
    
            for idx, result in enumerate(results):
                print("[" + str(idx + 1) + "] " + result.tostring())
    
            while(True):
                anichoice = input("Wähle einen Anime (Zahl links daneben eingeben): ")
                if(anichoice == "exit"):
                    exit = True
                    break
                elif(anichoice == "suche"):
                    search = True
                    break
                try:
                    anichoice = int(anichoice)
                    anime = results[anichoice - 1].getAnime()
                    break
                except:
                    print("Fehlerhafte eingabe, versuche erneut")
    
            if(search or exit):
                continue

            releases = anime.getReleases()
        
            print("\n\nReleases:\n")
        
            for rel in releases:
                print(rel.tostring())
    
            print("\n")

            print("Bestes Release nach Qualität: " + anime.getBestReleaseByQuality().tostring())

            relchoice = ""
            while(True):
                relchoice = input("Wähle eine Release ID: ")
                if(relchoice == "exit"):
                    exit = True
                    break
                elif(relchoice == "suche"):
                    search = True
                    break
                try:
                    relchoice = int(relchoice)
                    if(relchoice <= len(releases)):
                        break
                    else:
                        raise Exception()
                except:
                    print("Fehlerhafte Eingabe, versuche erneut")
    
            if(search or exit):
                continue

            release = releases[relchoice-1]
            print("Du hast folgendes Release gewählt: " + str(release.tostring()))
    
            print("Das Release hat " + str(release.getEpisodeCount()) + " Episode(n)")
    
            epichoice = ""
            while(True):
                epichoice = input("Welche Episode möchtest du herunterladen? (0 für alle (Achtung: Lädt im Moment noch jede Episode einzeln runter, zählt also zum Downloadlimit)): ")
                if(epichoice == "exit"):
                    exit = True
                    break
                elif(epichoice == "suche"):
                    search = True
                    break
                try:
                    epichoice = int(epichoice)
                    if(epichoice <= release.getEpisodeCount()):
                        break
                    else:
                        raise Exception()
                except:
                    print("Fehlerhafte Episodennummer")
    
            if(search or exit):
                continue
            try:
                if(epichoice != 0):
                    if(mode == "jdownloader"):
                        ret = anime.downloadEpisode(epichoice, release, hoster, browserengine, browserlocation=browserlocation, jdhost=jdhost)
                        print(ret)
                    else:
                        ret = anime.downloadEpisode(epichoice, release, hoster, browserengine, browserlocation=browserlocation)
                        for idx, link in enumerate(ret):
                            print("Part " + str(idx+1) + ": " + link)
                elif(epichoice == 0):
                    for i in range(0, release.getEpisodeCount()):
                        print("Lade episode " + str(i))
                        if(mode == "jdownloader"):
                            ret = anime.downloadEpisode(i + 1, release, hoster, browserengine, browserlocation=browserlocation, jdhost=jdhost)
                            print(ret)
                        else:
                            ret = anime.downloadEpisode(i + 1, release, hoster, browserengine, browserlocation=browserlocation)
                            for idx, link in enumerate(ret):
                                print("Part " + str(idx+1) + ": " + link)
    

            except selenium.common.exceptions.WebDriverException:
                print("[Fehler] Du musst chromedriver.exe (Chrome) oder geckodriver.exe (Firefox) im selben Ordner oder Pfad haben")
            except ALCaptchaException:
                print("Download benötigt captchas, bitte hole dir VIP für mehr Captcha-freie Zugriffe oder warte bis morgen")

            if(ret == False):
                print("Fehler beim hinzufügen zu JDownloader, ist er gestartet?")

    print("Programm wird beendet, vielen Dank fürs benutzen")

if(arglen > 1):
    al = animeloads()
    for arg in sys.argv:
        if("--help" in arg):
            print("Syntax: <downloader.py> [--url URL] [--user username] [--passwd password] [--list listfile] [--release release] [--episode episode] [--hoster hoster] [--jd 127.0.0.1] [--browser chrome] [--browserloc Browserpfad]")
            sys.exit(1)
    url = ""            #done
    username = ""       #done
    passwd = ""         #done
    release = ""        #done
    episodes = []       #done
    hoster = ""         #done
    jdhost = ""         #done
    browser = ""        #done
    browserlocation = ""     #done
    linklist = ""           #done
    for i in range(1, arglen):
        if(sys.argv[i] == "--url"):
            try:
                url = sys.argv[i+1]
                if("www.anime-loads.org" not in url):
                    sys.exit(1)
                print("Set url to " + url)
            except:
                print("Error, url is missing or invalid")
                sys.exit(1)
        if(sys.argv[i] == "--user"):
            try:
                user = sys.argv[i+1]
                print("Set user to " + user)
            except:
                print("Error, invalid User")
                sys.exit(1)

        if(sys.argv[i] == "--hoster"):
            try:
                hoster = sys.argv[i+1]
                if("uploaded".lower() in hoster.lower()):
                    hoster = animeloads.UPLOADED
                elif("ddownload".lower() in hoster.lower()):
                    hoster = animeloads.DDOWNLOAD
                else:
                    raise Exception()
                print("Set hoster to " + sys.argv[i+1])
            except:
                print("Error, invalid hoster [only \"uploaded\" or \"ddownload\"]: " + hoster)
                sys.exit(1)
        
        if(sys.argv[i] == "--jd"):
            try:
                jdhost = sys.argv[i+1]
                print("Set jdhost to " + jdhost)
            except:
                print("Error, invalid jdhost")
                sys.exit(1)

        if(sys.argv[i] == "--browser"):
            try:
                browser = sys.argv[i+1]
                if("chrome".lower() in browser.lower()):
                    browser = animeloads.CHROME
                elif("firefox".lower() in browser.lower()):
                    browser = animeloads.FIREFOX
                else:
                    raise Exception()
                print("Set browser to " + sys.argv[i+1])
            except:
                print("Error, invalid browser [only \"Chrome\" or \"Firefox\"]: " + browser)
                sys.exit(1)

        if(sys.argv[i] == "--browserloc"):
            try:
                browserlocation = sys.argv[i+1]
                print("Set browserlocation to " + sys.argv[i+1])
            except:
                print("Error, invalid browserlocation: " + browser)
                sys.exit(1)

        if(sys.argv[i] == "--pass"):
            try:
                passwd = sys.argv[i+1]
            except:
                print("Error, invalid PW")
                sys.exit(1)

        if(sys.argv[i] == "--release"):
            try:
                release = int(sys.argv[i+1])
                print("Set release to " + str(release))
            except:
                print("Error, either release is missing or not a number")
                sys.exit(1)
        if(sys.argv[i] == "--episode" or sys.argv[i] == "--episodes"):
            try:
                tempEpisodes = sys.argv[i+1].split(",")
                for ep in tempEpisodes:
                    episodes.append(int(ep))
                    print("Added episode " + str(ep) + " to download list")
            except:
                print("Error, either episode is missing or not a number")
                sys.exit(1)
        if(sys.argv[i] == "--list"):
            try:
                linklist = sys.argv[i+1]
                print("Set listfile to " + linklist)
            except:
                print("Error, list argument is missing")
                sys.exit(1)
        if(sys.argv[i] == "-- settings"):
            try:
                settingsfile = sys.argv[i+1]
                file = open(settingsfile, "r")
                jdata = json.load(file)
                for key in jdata:
                    if(key == "jdhost"):
                        jdhost = jdata[key]       
                    if(key == "hoster"):
                        hoster = jdata[key]
                    if(key == "browserengine"):
                        browserengine = jdata[key]
                    if(key == "browserlocation"):
                        browserlocation = jdata[key]
            except:
                print("Error, list argument is missing")
                sys.exit(1)
    
    if(linklist != ""):
        try:
            link = open(linklist, 'r') 
            lines = link.readlines()
        except:
            print("Konnnte Linkliste nicht öffnen: " + linklist)
            sys.exit(1)
        
        for line in lines:
            if(line[0] == "#"):
                continue
            splitline = line.split(",")
            if(len(splitline) > 2):
                link = splitline[0]
                release = splitline[1]

                anime = al.getAnime(link)

                releases = anime.getReleases()
                try:
                    rel = releases[int(release) - 1]
                except:
                    continue

                print("Lade anime " + link + " mit release " + release.tostring())
                for i in range(2, len(splitline)):
                    episode = int(splitline[i])
                    try:
                        print("Lade Episode : " + str(episode))
                        print(anime.downloadEpisode(episode, rel, hoster, browser, browserlocation, jdhost))
                    except Exception as e:
                        print(e)


            else:
                link = splitline[0]
                release = splitline[1]
                print("Lade ganzen Anime " + link + " mit release " + release.tostring())

                anime = al.getAnime(link)

                releases = anime.getReleases()
                try:
                    rel = releases[int(release) - 1]
                except:
                    continue

                for epi in range(1, rel.getEpisodeCount() + 1):
                    try:
                        print(anime.downloadEpisode(epi, rel, hoster, browser, browserlocation, jdhost))
                    except Exception as e:
                        print(e)


    elif(url == ""):                                #Kein Anime gesetzt
        print("No URL and no linklist, exiting...")

    elif(len(episodes) == 0 and release != 0):      #Anime mit festem Release, alle Folgen
        anime = al.getAnime(url)
        relFound = True
        try:
            release = anime.getReleases()[release-1]
            print("Lade ganzen Anime " + url + " mit release " + release.tostring())
        except:
            print("Release konnte nicht gefunden werden ")
            relFound = False
            
        if(relFound):
            for i in range(1, release.getEpisodeCount() + 1):
                print("Lade episode " + str(i))
                try:
                    print(anime.downloadEpisode(i, release, hoster, browser, browserlocation, jdhost))
                except Exception as e:
                    print(e)

    elif(len(episodes) != 0 and release == 0):      #Kein Release gesetzt
        print("Kein Release gesetzt, nehme bestes nach qualität")
        anime = al.getAnime(url)
        rel = anime.getBestReleaseByQuality()
        for episode in episodes:
            print("Lade " + url + " episode " + str(episode))
            try:
                print(anime.downloadEpisode(episode, rel, hoster, browser, browserlocation, jdhost))
            except Exception as e:
                print(e)

    elif(len(episodes) == 0 and release == 0):      #Keine Episode und kein Release
        print("Lade ganzen Anime mit bestem Release nach Qualität")
        anime = al.getAnime(url)
        rel = anime.getBestReleaseByQuality()
        for epi in range(1, rel.getEpisodeCount()+1):
            try:
                print(anime.downloadEpisode(epi, rel, hoster, browser, browserlocation, jdhost))
            except Exception as e:
                print(e)

    else:                                           #Alles gesetzt
        anime = al.getAnime(url)
        try:
            release = anime.getReleases()[release-1]
        except:
            print("Release konnte nicht gefunden werden ")
        for episode in episodes:
            print("Lade " + url + " episode " + str(episode) + " mit release " + release.tostring())
            try:
                print(anime.downloadEpisode(episode, release, hoster, browser, browserlocation, jdhost))
            except Exception as e:
                print(e)    
    
elif(arglen == 1):
    print("Starte interaktiven Modus")
    interactive()
else:
    print("Falsche Argumente: <downloader.py> [--url URL] [--user username] [--passwd password] [--list listfile] [--release release] [--episode episode] [--hoster hoster] [--jd 127.0.0.1] [--browser chrome] [--browserloc Browserpfad]")
    sys.exit(1)
