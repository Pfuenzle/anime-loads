FROM python:3.9-slim-bullseye

WORKDIR /usr/src/app
RUN apt update \
&& apt install --no-install-recommends git wget libxt6 libgl1-mesa-glx libdbus-glib-1-2 libgtk-3-0 firefox-esr lbzip2 gcc -y \
&& apt clean \
&& rm -rf /var/lib/apt/lists/* \
&& git clone https://github.com/Pfuenzle/anime-loads.git

WORKDIR /usr/src/app/anime-loads
RUN wget -nv https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz && tar -xf geckodriver-v0.31.0-linux64.tar.gz \
&& rm geckodriver-v0.30.0-linux64.tar.gz \
&& mv geckodriver /bin/geckodriver \
&& chmod +x /bin/geckodriver
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "anibot.py", "--configfile", "/config/ani.json" ]
CMD [ "--docker" ]
