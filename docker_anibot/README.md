# Animeloads


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

## Docker Quickstart

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

