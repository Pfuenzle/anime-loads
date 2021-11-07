import time
import sys, os

import myjdapi

import json

from animeloads import animeloads
from animeloads import ALCaptchaException

from getpass import getpass

import selenium

settingsfile = "config/settings.json"
settingsfolder = "config/"

arglen = len(sys.argv)

def compare(inputstring, validlist):
    for v in validlist:
        if(v.lower() in inputstring.lower()):
            return True
    return False

def settings():
    try:
        os.makedirs(os.path.dirname(settingsfolder), exist_ok=True)
        file = open(settingsfile, "r")
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
            if(key == "myjd_user"):
                jd_user = jdata[key]
            if(key == "myjd_pw"):
                jd_pass = jdata[key]
            if(key == "myjd_device"):
                jd_device = jdata[key]
        file.close()
    except:
        jdhost = ""
        mode = ""
        hoster = ""
        browserengine = ""
        browserlocation = ""
        jd_user = ""
        jd_pass = ""
        jd_device = ""

    if(hoster == 2):
        hosterstr = "rapidgator"
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
            host = input("Welchen hoster bevorzugst du? rapidgator, uploaded oder ddownload: ")
            if("uploaded" in host):
                hoster = animeloads.UPLOADED
                break
            elif("ddownload" in host):
                hoster = animeloads.DDOWNLOAD
                break
            elif("rapidgator" in host):
                hoster = animeloads.RAPIDGATOR
                break
            else:
                print("Bitte gib entweder uploaded, rapidgator oder ddowwnload ein")

    changemode = True
    if(mode != ""):
        if(compare(input("Dein gewählter modus: " + mode + ", möchtest du ihn wechseln? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
            changemode = False

    if(changemode):
        if(compare(input("Möchtest du Jdownloader2 nutzen? Andernfalls werden die Links in der Konsole zurückgegeben [J/N]: "), {"j", "ja", "yes", "y"})):
            change_jdhost = True
        
        
            jd_device = ""
            jd_user = ""
            jd_pass = ""
        
            jd_choice = input("Läuft Jdownloader auf deinem lokalen Rechner[1] oder möchtest du MyJdownloader nutzen[2]?  (1 oder 2): ")
            if(jd_choice == 1):
                if(jdhost != ""):
                    if(compare(input("Deine Adresse des Computers, auf dem JDownloader läuft lautet: " + jdhost + ", möchtest du ihn wechseln? [J/N]: "), {"j", "ja", "yes", "y"}) == False):
                        change_jhdhost = False
              
                if(change_jdhost):
                    if(input("Läuft dein JD2 auf deinem Lokalen Computer? Dann Eingabe leer lassen und bestätigen, falls nicht, gib die Adresse des Zeilrechners an: ") != ""):
                        jdhost = input
                    else:
                        jdhost = "127.0.0.1"
                jd_device = ""
                jd_pass = ""
                jd_user = ""
            
            else:
                jd_choice = 2
                jd=myjdapi.Myjdapi()
                jd.set_app_key("animeloads")
                
                logincorrect = False
                while(logincorrect == False):
                    jd_user = input("MyJdownloader Nutzername: ")
                    jd_pass = getpass("MyJdownloader Passwort: ")
                    
                    try:
                      jd.connect(jd_user, jd_pass)
                      logincorrect = True
                    except:
                        print("Fehlerhafte Logindaten")
                
                print("Logindaten sind korrekt")
                jd.update_devices()
                devices = jd.list_devices() 
                
                print("Deine verbundenen Geräte: ")
                for dev in devices:
                    print(dev['name'])
                
                foundDevice = False
                while(foundDevice == False):
                    jd_device = input("Gib den Namen des Gerätes, welches du benutzen willst ein: ")
                    for dev in devices:
                        devname = dev['name']
                        if(jd_device == devname):
                            foundDevice = True
                            break
                    if(foundDevice == False):
                        print("Gerät nicht gefunden...")
                
                print("Nutze Gerät: " + jd_device)
                
                if(compare(input("Möchtest du das MyJDownloader passwort speichern (unverschlüsselt!!!)? Andernfalls musst du es jeden Programmstart eingeben [J/N]: "), {"j", "ja", "yes", "y"}) == False):
                    jd_pass = ""
        
                jdhost = ""
            mode = "jdownloader"
        else:
            print("Gebe links in Console aus...")
            mode = "console"
            jdhost = ""
            jd_user = ""
            jd_pass = ""
            jd_device = ""

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
        "mode": mode,
        "browserengine": browserengine,
        "browserlocation": browserlocation,
        "jdhost": jdhost,
        "myjd_user": jd_user,
        "myjd_pw": jd_pass,
        "myjd_device": jd_device
    }

    jdata = json.dumps(data, indent=4, sort_keys=True)

    os.makedirs(os.path.dirname(settingsfolder), exist_ok=True)
    file = open(settingsfile, "w")
    file.write(jdata)
    file.close()

def loadSettings():
    os.makedirs(os.path.dirname(settingsfolder), exist_ok=True)
    file = open(settingsfile, "r")
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
        if(key == "myjd_user"):
            myjd_user = jdata[key]
        if(key == "myjd_pw"):
            myjd_pass = jdata[key]
        if(key == "myjd_device"):
            myjd_device = jdata[key]
    file.close()
    return jdhost, mode, hoster, browserengine, browserlocation, myjd_user, myjd_pass, myjd_device

def interactive():

    mode = ""

    while(mode == ""):
      
        try:
            jdhost, mode, hoster, browserengine, browserlocation, myjd_user, myjd_pass, myjd_device = loadSettings()
        except:
            print("Du hast noch keine Einstellungen festgelegt")
            settings()


    al = animeloads(browser=browserengine, browserloc=browserlocation)

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

    if(jdhost == "" and myjd_pass == "" and mode != "console"):
        print("Kein MyJdownloader Passwort gesetzt")
        logincorrect = False 
        jd=myjdapi.Myjdapi()
        jd.set_app_key("animeloads")
        while(logincorrect == False):
            myjd_pass = getpass("MyJdownloader Passwort: ")
          
            try:
              jd.connect(myjd_user, myjd_pass)
              logincorrect = True
            except:
                print("Fehlerhafte Logindaten")
    print("Erfolgreich eingeloggt")

    if(compare(input("Möchtest du deine Einstellungen ändern? [J/N]: "), {"j", "ja", "y", "yes"})):
        settings()
        jdhost, mode, hoster, browserengine, browserlocation, myjd_user, myjd_pass, myjd_device = loadSettings()

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
            episodes = []
            while(True):
                epichoice = input("Welche Episode möchtest du herunterladen? (Mehrere mit Komma getrennt, 0 für alle (Achtung: Lädt im Moment noch jede Episode einzeln runter, zählt also zum Downloadlimit)): ")
                if(epichoice == "exit"):
                    exit = True
                    break
                elif(epichoice == "suche"):
                    search = True
                    break
                if("," in epichoice):
                    try:
                        episodes_str = epichoice.split(",")
                        for ep in episodes_str:
                            episodes.append(int(ep))
                            if(int(ep) <= release.getEpisodeCount()):
                                pass
                            else:
                                raise Exception
                        break
                    except:
                        print("Fehlerhafte Episodennummern")
                else:
                    try:
                        episodes.append(int(epichoice))
                        if(episodes[0] <= release.getEpisodeCount()):
                            break
                        else:
                            raise Exception()
                    except:
                        print("Fehlerhafte Episodennummer")
    
            if(search or exit):
                continue
            try:
                if(episodes[0] != 0):
                    for i in episodes:
                        if(mode == "jdownloader"):
                            ret = anime.downloadEpisode(i, release, hoster, browserengine, browserlocation=browserlocation, jdhost=jdhost, myjd_user=myjd_user, myjd_pw=myjd_pass, myjd_device=myjd_device)
                            print(ret)
                        else:
                            ret = anime.downloadEpisode(i, release, hoster, browserengine, browserlocation=browserlocation)
                            for idx, link in enumerate(ret):
                                print("Part " + str(idx+1) + ": " + link)
                elif(episodes[0] == 0):
                    for i in range(0, release.getEpisodeCount()):
                        print("Lade episode " + str(i))
                        if(mode == "jdownloader"):
                            ret = anime.downloadEpisode(i + 1, release, hoster, browserengine, browserlocation=browserlocation, jdhost=jdhost, myjd_user=myjd_user, myjd_pw=myjd_pass, myjd_device=myjd_device)
                            print(ret)
                        else:
                            ret = anime.downloadEpisode(i + 1, release, hoster, browserengine, browserlocation=browserlocation)
                            for idx, link in enumerate(ret):
                                print("Part " + str(idx+1) + ": " + link)
    

            except selenium.common.exceptions.WebDriverException as e:
                print("[Fehler] Du musst chromedriver.exe (Chrome) oder geckodriver.exe (Firefox) im selben Ordner oder Pfad haben")
            except ALCaptchaException:
                print("Download benötigt captchas, bitte hole dir VIP für mehr Captcha-freie Zugriffe oder warte bis morgen")

    print("Programm wird beendet, vielen Dank fürs benutzen")

if(arglen > 1):
    al = animeloads()
    for arg in sys.argv:
        if("--help" in arg):
            print("Syntax: <downloader.py> [--url URL] [--user username] [--passwd password] [--list listfile] [--release release] [--episode episode] [--hoster hoster] [--jd 127.0.0.1] [--browser chrome] [--browserloc Browserpfad] [--myjd_user username/email] [--myjd_pw password] [--myjd_device Devicename]")
            sys.exit(1)
    url = ""            #done
    username = ""       #done
    passwd = ""         #done
    release = ""        #done
    episodes = []       #done
    hoster = ""         #done
    jdhost = ""         #done
    browser = ""        #done
    myjd_user = ""      #done
    myjd_pass = ""        #done
    myjd_device = ""    #done
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
                elif("rapidgator".lower() in hoster.lower()):
                    hoster = animeloads.rapidgator
                else:
                    raise Exception()
                print("Set hoster to " + sys.argv[i+1])
            except:
                print("Error, invalid hoster [only \"uploaded\", \"rapidgator\" or \"ddownload\"]: " + hoster)
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
        if(sys.argv[i] == "--myjd_user"):
            try:
                myjd_user = sys.argv[i+1]
                print("Set MyJD User to " + myjd_user)
            except:
                print("Error, User argument is missing")
                sys.exit(1)
        if(sys.argv[i] == "--myjd_pw"):
            try:
                myjd_pass = sys.argv[i+1]
                print("Set MyJD Password to " + myjd_pw)
            except:
                print("Error, Password argument is missing")
                sys.exit(1)
        if(sys.argv[i] == "--myjd_device"):
            try:
                myjd_device = sys.argv[i+1]
                print("Set MyJD Device to " + myjd_device)
            except:
                print("Error, Device argument is missing")
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
                    if(key == "myjd_user"):
                        myjd_user = jdata[key]
                    if(key == "myjd_pw"):
                        myjd_pass = jdata[key]
                    if(key == "myjd_device"):
                        myjd_device = jdata[key]
            except:
                print("Error, list argument is missing or list is invalid")
                sys.exit(1)
    
    al = animeloads(browser=browser, browserloc=browserlocation)
    
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
                        print(anime.downloadEpisode(episode, rel, hoster, browser, browserlocation, jdhost, myjd_user=myjd_user, myjd_pw=myjd_pass, myjd_device=myjd_device))
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
                        print(anime.downloadEpisode(epi, rel, hoster, browser, browserlocation, jdhost, myjd_user=myjd_user, myjd_pw=myjd_pass, myjd_device=myjd_device))
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
                    print(anime.downloadEpisode(i, release, hoster, browser, browserlocation, jdhost, myjd_user=myjd_user, myjd_pw=myjd_pass, myjd_device=myjd_device))
                except Exception as e:
                    print(e)

    elif(len(episodes) != 0 and release == 0):      #Kein Release gesetzt
        print("Kein Release gesetzt, nehme bestes nach qualität")
        anime = al.getAnime(url)
        rel = anime.getBestReleaseByQuality()
        for episode in episodes:
            print("Lade " + url + " episode " + str(episode))
            try:
                print(anime.downloadEpisode(episode, rel, hoster, browser, browserlocation, jdhost, myjd_user=myjd_user, myjd_pw=myjd_pass, myjd_device=myjd_device))
            except Exception as e:
                print(e)

    elif(len(episodes) == 0 and release == 0):      #Keine Episode und kein Release
        print("Lade ganzen Anime mit bestem Release nach Qualität")
        anime = al.getAnime(url)
        rel = anime.getBestReleaseByQuality()
        for epi in range(1, rel.getEpisodeCount()+1):
            try:
                print(anime.downloadEpisode(epi, rel, hoster, browser, browserlocation, jdhost, myjd_user=myjd_user, myjd_pw=myjd_pass, myjd_device=myjd_device))
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
                print(anime.downloadEpisode(episode, release, hoster, browser, browserlocation, jdhost, myjd_user=myjd_user, myjd_pw=myjd_pass, myjd_device=myjd_device))
            except Exception as e:
                print(e)    
    
elif(arglen == 1):
    print("Starte interaktiven Modus")
    interactive()
else:
    print("Falsche Argumente: <downloader.py> [--url URL] [--user username] [--passwd password] [--list listfile] [--release release] [--episode episode] [--hoster hoster] [--jd 127.0.0.1] [--browser chrome] [--browserloc Browserpfad] [--myjd_user username/email] [--myjd_pw password] [--myjd_device Devicename]")
    sys.exit(1)
