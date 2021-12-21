externPath = "http://127.0.0.1:8080"                                     #Adresse, auf die Sonarr auf den Indexer zugreift. Muss also von Sonarr erreichbar sein
hostName = "127.0.0.1"                                                   #Adresse auf der der Indexer hört
serverPort = 8080                                                        #Port auf dem der Indexer hört
resultrange = 5                                                          #Wie viele Ergebnisse nach Releasen durchsucht werden sollen

ALUsername = ""                                                          #AL-Nutzername (falls nicht benötigt oder nicht vorhanden leerlassen)
ALPassword = ""                                                          #Login wird nur für komplette Seasondownloads benötigt
cacheTime = 15                                                          #Zeit in Minute, wie lange Ergebnisse gecachet werden sollen

jdname = ""                                                              #Name der MyJDownloader Instanz, zu dem die Downloads hinzugefügt werden
jdemail = ""                                                             #Email für MyJDownloader Login
jdpassword = ""                                                          #Passwort für MyJdownloader Login
downloadpath = "/downloads/anime-loads-completed"                        #Dieser und die 2 unteren Pfade müssen von Jdownloader und Sonarr les/- und beschreibbar sein.
sonarrPath = downloadpath + "/sonarr"                                    #In diesen Ordner werden die Dateien für Sonarr runtergeladen
radarrPath = downloadpath + "/radarr"                                    #In diesen Ordner werden die Dateien für Radarr runtergeladen

JDownloaderRetries = 7                                                   #Wie oft nach einem Fehlschlag versucht werden soll, einen Download zu JDownloader hinzuzufügen

hoster = "uploaded"                                                      #"uploaded", "ddownload" oder "rapidgator"
browser = "chrome"                                                       #"chrome" oder "firefox"
keepWrongSeasons = True                                                  #Falls False: Wenn nach Season 01 gesucht wird, werden alle Ergebnisse, die nicht S01 sind, nicht gesendet. Funktioniert nur bei Serientyp "Standard"

#########################################
#Startanleitung

#Vorraussetzungen
#  - Python 3.x
#  - Entweder:
#    - Chrome + chromedriver (https://chromedriver.chromium.org/downloads)      (Die chromedriver version muss identisch zu der Chromeversion sein)
#    - Firefox + geckodriver (https://github.com/mozilla/geckodriver/releases)



###################
#Python:
#In der Konsole im Indexerordner:
# "python -m pip install -r requirements.txt"
# Chromedriver/Geckodriver in den Indexerordner verschieben


###################
#Sonarr/Radarr:
#Settings -> Indexers -> (Custom) NewzNab Indexer hinzufügen.
#URL muss auf den oben festgelegt "externPath" gesetzt werden. API-Key ist egal. Dann auf Test und bei einem grünen Haken bei Categories die gewünschte Kategorie auswählen.
#
#Settings -> Download Clients -> Usenet Blackhole hinzufügen.
#Nzb Folder kann auf einen beliebigen Ordner gesetzt werden.
#Watch Folder muss auf den gleichen Pfad wie oben gesetzt werden(Bei Sonarr wie in der Variable "sonarrPath", bei Radarr wie in "radarrPath").
#Im obigen Beispiel wäre der Watch Folder für Sonarr also "/downloads/anime-loads-completed/sonarr/".
#In diesen Ordner werden die Dateien runtergeladen und dann von Sonarr aufgesammelt.
#Für Docker können beide Pfade unterschiedliche sein, müssen aber auf dem Hostsystem auf den gleichen Ordner verweisen
#Beide Ordner müssen von Sonarr & JDownloader les- und beschreibbar sein.

###################
#Jdownloader:
#MyJDownloader aktivieren
#Archive Extractor aktivieren (Optional: "Delete Archive Files after successful extraction" aktivieren, um nach dem Entpacken keine unnötigen RAR Dateien auf dem Rechner zu haben)
#Optional: "Restart Download when SFV/CRC check fails" aktivieren


###################
#Tipps:
#In Sonarr gibt es zwei Serienarten (die für Anime nutzbar sind):
#Normal & Anime
#
#Bei Serienart Normal wird bei einer Staffelsuche nur nach dem Serienname + der gesuchten Staffel gesucht. Dadurch werden mit dem Indexer (falls oben die Option "keepWrongSeasons = False" gesetzt ist),
#alle falschen Ergebnisse weggelassen.
#Bei der Serienart Anime wird bei einer Staffelsuche die Staffel nicht angegeben, sondern Sonarr sucht nach "Serienname + Episode". Dadurch wird die Staffel nicht angegeben und Sonarr sucht nach jeder in der Staffel
#vorhandenen Episode einzeln, wodurch die Suche sehr viel länger dauert und bei vielen Episoden manchmal sogar austimet.
#Falls also manuell nach einer Staffel gesucht wird, empfehle ich den Serientyp temporär auf Normal zu stellen.
