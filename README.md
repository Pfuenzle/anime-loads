# Animeloads

Das Projekt besteht aus 3 Teilen:

## anibot.py

    Ein vollautomatischer Bot für Anime-Loads für automatische Downloads, mit optionalem Support für Pushbullet 
    für mobile Benachrichtigungen

    Erlaubt das hinzufügen/löschen von Anime zu einer Liste, entweder durch Suche oder Eingabe eines Links. 
    Diese Anime in dieser Liste werden alle X Sekunden nach neuen Folgen geprüft.

    Falls der Anime mehr Folgen hat, als bereits runtergeladen wurde, werden sie automatisch zu 
    JDownloader hinzugefügt.
    Falls JDownloader zu dem Zeitpunkt nicht verfügbar ist, werden die 
    Episoden zu der Liste fehlender Episoden hinzugefügt und zu einem 
    späteren Zeitpunk heruntergeladen.

    Anime können außerdem mit 0 bereits runtergeladenen Episoden hinzugefügt werden, daraufhin 
    wird der ganze Anime komplett heruntergeladen

    In nächster Zeit wird noch direkter Support für den Download von Serien kommen, damit die 
    Abhängigkeit zu JDownloader wegfällt

[Mehr Infos und Installation](#anibot.py)

<br>

## animeloads.py
    
    Die eigentliche API, mit ihr kann einfach mit Serien und Filmen auf Anime-Loads interagiert werden

    - Erlaubt Suche nach Anime oder direktes Eingeben der URL eines Anime
    - Einloggen in Accounts für mehr Downloads und Verlauf im Webinterface
    - Details über Anime:
        - Name (Englisch, Deutsch, Japanisch)
        - Episoden, Genre, Jahr, Status, Laufzeit
    - Details über Releases:
        - Qualität (Auflösung und Audio/Video-Format)
        - Sprachen (Audio und Untertitel) und verfügbare Episoden
    - Extrahieren von Downloadlinks oder direktes hinzufügen zu JDownloader

[Mehr Infos und Dokumentation](#animeloads.py)

<br>

## downloader.py

    Ein Kommandozeilen-Tool für Anime-Loads
    - Unterstützt Suche nach Anime oder direkte Eingabe der URL
    - Auflistung der Releases
    - Login für mehr tägliche Downloads/Verlauf im Webinterface
    - Ausgabe von uploaded/ddownload links
    - Automatisches hinzufügen von Links zu JDownloader
    - Auswählen von bestimmten Releases
    - Zeigt Release mit bester Qualität, meisten Episoden oder meisten Sprachen an
    - Download von ein einzelnen Episoden oder ganzen Staffeln
    - Download einer Liste mit mehreren Anime

[Mehr Infos und Installation](#downloader.py)

<br>
Im js Ordner sind 2 Javascript Dateien, mit denen Ad-Cookies erstellt werden in einem Versuch, nicht mehr als Adblock erkannt zu werden
<br>

## Docker Quickstart

Die Dockerbefehle erstellen in dem aktuellen Ordner einen Unterordner "config", in dem die Einstellungen etc. gespeichert werden

Info für Raspberry Pi:
für das Dockerimage immer `pfuenzle/anime-loads:arm` anstatt dem normalen verwenden.


### anibot.py:

Container pullen:

    - docker pull pfuenzle/anime-loads

Falls noch keine Config existiert:

    - docker run --rm -it -v $PWD/config:/config pfuenzle/anime-loads --interactive

andernfalls einen Ordner "config" erstellen und eine bereits vorhandene ani.json reinverschieben

Container starten (-it durch -dit ersetzen, um den Container im Hintergrund zu starten:

    - docker run --rm -it -v $PWD/config:/config pfuenzle/anime-loads

Docker-compose:
```
---
version: "2.1"
services:
  anime-loads:
    image: pfuenzle/anime-loads:latest
    container_name: anime-loads
    volumes:
      - ./config:/config
    restart: unless-stopped
```

Config ändern:

    - docker run --rm -it -v $PWD/config:/config pfuenzle/anime-loads add

    - docker run --rm -it -v $PWD/config:/config pfuenzle/anime-loads edit

    - docker run --rm -it -v $PWD/config:/config pfuenzle/anime-loads remove


### downloader.py:

Container erstellen:
    - `docker build docker_downloader/ -t anidownloader`

Falls noch keine Settings existieren:
    - `docker run --rm -it -v $PWD/config:/config anidownloader`
andernfalls einen Ordner "config" erstellen und settings.json reinverschieben

Container starten (mögliche gewünschte Argumente einfach hinter Befehl einfügen):
    - `docker run --rm -it -v $PWD/config:/config anidownloader`


<br><br><br><br>

<h2 id="anibot.py">
anibot.py
</h2>

Benötigte Software:

    - Firefox und Geckodriver ( https://github.com/mozilla/geckodriver/releases )
    ODER
    - Chrome und Chromedriver ( https://chromedriver.chromium.org/ )
    - Python 3
    - JDownloader2

Der Driver wird dazu genutzt, um den jeweiligen Browser fernzusteuern, 
um der Seite zu überzeugen, dass der Bot ein vollwertiger Nutzer wird, 
da er sonst andernfalls aus irgendeinem Grund als Adblock erkannt wird.
Hierbei wird allerdings kein Fenster geöffnet, d.h. alles funktioniert auch über SSH oder in der Konsole
Der Driver wird nur für den Download verwendet, alle anderen Funktionen funktionieren 
auch ohne ihn
(Bin dabei zu versuchen, die Erkennung zu umgehen)

!!!
Falls man einen Fork der oben genannten Browser (z.B. Waterfox) hat oder er in einem anderen als in 
dem Standardpfad installiert ist, muss der Pfad (inklusive .exe auf Windows oder Binary auf Linux) zu dem Browser angegeben werden,
falls das Script danach fragt, da er sonst nicht  gefunden werden kann
!!!
<br><br><br>
Ersteinrichtung:
<br><br>
Nach der Installation von Python 3 muss man nun das Repository runterladen.

Das geht entweder (falls man GIT installiert hat) mit:

`git clone https://github.com/Pfuenzle/anime-loads.git`

Falls nicht, einfach [hier](https://github.com/Pfuenzle/anime-loads/releases) das neueste Release runterladen: https://github.com/Pfuenzle/anime-loads/releases und irgendwo entpacken.

Unter Windows muss Geckodriver/Chromedriver in den aktuellen Ordner kopiert werden, damit er vom Script gefunden wird
Unter Linux muss Chromedriver/Geckodriver stattdessen in "/usr/local/bin" kopiert werden.

Nun öffnet CMD/Powershell/Shell in dem Ordner. Dazu klickt man in Windows entweder im Explorer auf die Leiste, die den aktuellen Pfad anzeigt und tippt "cmd" ein, oder öffnet CMD über die Suche und navigiert mit "cd \<Pfad\>" manuell in den Ordner
Wenn man Linux nutzt, gehe ich davon aus, dass man weiß wie man eine Shell in dem Ordner bekommt

Dort angekommen tippt man in die Konsole `pip install -r requirements.txt` ein. Damit werden alle abhängigkeiten installiert

<br><br>

Konfiguration und Start:
<br><br>
Die Allgemeine Benutzung funktioniert wie folgt:

`python anibot.py <Befehl>`

Mögliche Befehle:

    help        Gibt Hilfe aus
    start       Startet den Bot
    edit        Einstellungen ändern, z.b. Welcher Browser, etc.. (Wird beim ersten mal zwingend aufgerufen)
    add         Neuen Anime hinzufügen, entweder durch Suche oder eine URL
    remove      Anime von Downloadliste löschen

Wenn anibot.py normal durch einen Doppelklick geöffnet wird, startet der Bot normal, vorrausgesetzt, es ist mindestes bereits ein Anime in der Liste hinzugefügt

Vor dem Start wird man zusätzlich noch gefragt, ob man sich einloggen oder die Einstellungen ändern möchte.

Sobald der Bot gestartet ist, prüft er alle Anime in der Liste alle X Sekunden nach neuen verfügbaren Episoden und falls welche gefunden wurden, fügt er sie automatisch bei JDownloader ein


Im Projekt enthalten ist eine Beispiel-Liste für die Season 2020/2021
Um sie zu nutzen, einfach "ani.json.example_season2020_2021" in "ani.json" umbennen. 
Beim nächsten Start werden automatisch neue Episoden der aktuellen Season heruntergeladen


<br><br>

<h2 id="animeloads.py">
animeloads.py
</h2>

Bei selbsterklärenden Methoden wird nur der Rückgabewert genannt


```
Klassen:
    -   animeloads:
        -   __init__(user="", pw=""):
                Falls user und pw gegeben ist, wird der Nutzer automatisch eingeloggt
        -   search(query):
                Sucht nach "query" und gibt eine Liste der Klasse "searchResult" zurück
        -   getAnime(URL):
                Gibt ein Anime-Objekt der Klasse anime zurück
        -   login(user, pw):
                Meldet den User nachträglich an
    -   searchResult:
        -   getURL()                string
        -   getName()               int
        -   getTyp()                string
        -   getReleaseDate()        int
        -   getCurrentEpisodeCount()int
        -   getMaxEpisodeCount()    int
        -   getDubLang()            list(string)
        -   getSublang()            list(string)
        -   getGenre()              string
        -   tostring()              string
        -   getAnime()              anime
    -   anime:
        -   downloadEpisode(episode, release, hoster, browser, optional browserlocation, optional jdhost):
                episode:            int
                release:            release
                hoster:             0/1/animeloads.UPLOADED/animeloads.DDOWNLOAD
                browser:            0/1/animeloads.CHROME/animeloads.FIREFOX
                browserlocation:    str(Pfad zum Browser)
                jdhost:             str(Hostname/IP von JDownloader, normalerweise 127.0.0.1) 
        -   updateInfo():
                Updated Info des Anime(z.B. Episodeanzahl)
        -   getBestReleaseByQuality(optional releaseList):
                Gibt bestes Release nach Qualität zurück
        -   getBestReleaseByLanguage(optional releaseList):
                Gibt Release mit meisten Sprachen zurück
        -   getBestReleaseByEpisodes(optional releaseList):
                Gibt Release mit meisten Episoden zurück
        -   getName()               string
        -   getNameGerman()         string
        -   getNameJapanese()       string
        -   getNameEnglish()        string
        -   getURL()                string
        -   getRuntime()            int
        -   getType()               string
        -   getSynonymes()          list(string)
        -   getYear()               int
        -   getCurrentEpisodes()    int
        -   getMaxEpisodes()        int
        -   getStatus()             string
        -   getMainGenre()          string
        -   getSideGenres()         list(string)
        -   getTags()               list(tags)
        -   getReleases()           list(release)
        -   tostring()              string      
    -   release:
        -   getID()                 int
        -   getGroup()              string
        -   getResolution()         int
        -   getAudioCodec()         string
        -   getDubs()               list(string)
        -   getSubs()               list(string)
        -   getVideoFormat()        list(string)
        -   getSize()               int         in MB
        -   getPassword()           string
        -   getAnmerkung()          string
        -   getVideoCodec()         string

Exceptions:
    -   ALCaptchaException
        -   Wird geworfen, falls die Seite ein Captcha zum download benötigt
    -   ALInvalidBrowserException
        -   Falls der gesetzte Browser nicht gesetzt oder nicht unterstützt wird
    -   ALLinkExtractionException
        -   Falls es einen Fehler beim holen der Links gibt, z.B. Serverseitig geändert
    -   ALInvalidLoginException
        -   Falls der Login mit den angegebenen Daten fehlgeschlagen ist
```


Beispielcode:

```
from animeloads import animeloads

al = animeloads()                           #Erstellt das Animeloads Objekt, optional mit user/pw für login

anime = al.getAnime("https://www.anime-loads.org/media/...")    #Holt Anime der URL im Parameter

releases = anime.getReleases()              #Holt alle Release

for release in releases:
    print(release.tostring())               #Gibt alle Releases mit allen Attributen aus

hoster = animeloads.UPLOADED                #Setzt hoster auf uploaded.net
browser = animeloads.CHROME                 #Nutzt Chrome

downloadlink = anime.downloadEpisode(1, releases[0], hoster, browser)   
#Gibt den Downloadlink der ersten Episode des Anime mit dem ersten Release von Uploaded zurück

print(downloadlink)                         #Gibt den/die Downloadlink(s) zurück
```

<br><br>

<h2 id="downloader.py">
downloader.py
</h2>

Lies zur Installation den Teil Ersteinrichtung von [anibot.py](#anibot.py) durch.

Nach der Einrichtung kann der Downloader auf 2 Arten gestartet werden.
<br><br>
Methode 1 ist der interaktive Download, entweder durch doppelklick auf downloader.py 
oder durch 
`python downloader.py`

Im interaktiven Modus wird man alles nötige gefragt und danach entweder der Link zurückgegeben oder zu JDownloader hinzugefügt. Die hierbei festgelegten Einstellungen werden in settings.json gespeichert und können wiederverwendet werden
<br><br>
Methode 2 ist die nicht-interaktive Art, bei der alle nötigen Parameter direkt übergeben werden müssen

```<downloader.py> [--url URL] [--user username] [--passwd password] [--list listfile] [--release release] [--episode episode] [--hoster hoster] [--jd 127.0.0.1] [--browser chrome] [--browserloc Browserpfad]```
  

Mögliche Parameter:

    --help        Gibt Hilfe aus
    --url         URL des Animes
    --user        Nutzername zum Einloggen
    --passwd      Passwort des Nutzer
    --list        name der Liste mit Anime
    --release     ID des Releases, das geladen werden soll
    --episode     Episode(n), die geladen werden. Entweder als Zahl allein oder mehrere, getrennt durch Kommas
    --hoster      Entweder uploaded oder ddownload
    --jd          Falls Jdownloader benutzt werden soll: Als parameter dahinter den Host nennen, normalerweise 127.0.0.1
    --browser     Genutzter Browser, chrome oder firefox
    --browserloc  Pfad des gewählten Browser, falls Fork oder nicht an Standardpfad installiert

<br><br>
Download einer Liste:

```
Die Liste muss folgendens Format haben:

url,release,episode1,episode5,episode6

Die Parameter werden durch ein Komma getrennt.
Der erste ist die URl des Anime und der zweite die ID des Releases das gewählt wurde.
Diese zwei müssen mindestens gegeben sein. Danach können noch unendlich Episoden kommen,
welche von dem Anime runtergeladen werden sollen, jeweils mit einem Komma getrennt

Beispiel:
https://www.anime-loads.org/media/anime,2
Um alle Folgen des 2. Release des Anime runterzuladen

Oder

https://www.anime-loads.org/media/anime,1,4,5,6,9
Um die Folgen 4,5,6 und 9 des ersten Release des Anime runterzuladen
```
