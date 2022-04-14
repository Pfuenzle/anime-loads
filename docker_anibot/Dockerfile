FROM python:3

WORKDIR /usr/src/app

RUN apt-get update -y

RUN apt-get install firefox-esr -y

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux32.tar.gz

RUN tar -xf geckodriver-v0.31.0-linux32.tar.gz

RUN rm geckodriver-v0.31.0-linux32.tar.gz

RUN mv geckodriver /usr/bin/

RUN git clone https://github.com/Pfuenzle/anime-loads.git

RUN mv anime-loads/* .

RUN rm -rf anime-loads

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./anibot.py", "--configfile", "/config/ani.json", "--docker" ]