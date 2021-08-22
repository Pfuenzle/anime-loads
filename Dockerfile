FROM python:3-slim-bullseye

WORKDIR /usr/src/app
RUN apt update && apt install git wget libgl1-mesa-glx libdbus-glib-1-2 libgtk-3-0 lbzip2 -y && apt clean && git clone https://github.com/Pfuenzle/anime-loads.git

WORKDIR /usr/src/app/anime-loads
RUN wget -nv https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz && tar -xf geckodriver-v0.29.1-linux64.tar.gz \
&& wget -nv https://download-installer.cdn.mozilla.net/pub/firefox/releases/78.13.0esr/linux-x86_64/de/firefox-78.13.0esr.tar.bz2 && tar -xf firefox-78.13.0esr.tar.bz2 \
&& rm geckodriver-v0.29.1-linux64.tar.gz && rm firefox-78.13.0esr.tar.bz2 && mv geckodriver /bin/geckodriver && chmod +x /bin/geckodriver
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "anibot.py" ]
CMD [ "--docker" ]
