FROM python:3.9-slim-bullseye

WORKDIR /usr/src/app
RUN apt update \
&& apt install --no-install-recommends git wget libxslt-dev openexr ffmpeg libatlas-base-dev libopenjp2-7 libxt6 libgl1-mesa-glx libdbus-glib-1-2 libgtk-3-0 firefox-esr lbzip2 unzip -y \
&& apt clean \
&& rm -rf /var/lib/apt/lists/* \
&& git clone https://github.com/Pfuenzle/anime-loads.git

WORKDIR /usr/src/app/anime-loads
# get self-compiled geckodriver, as Mozilla doesn't provide an arm7 build anymore
RUN wget -nv https://pheromir.tech/geckodriver-arm7.zip && unzip geckodriver-arm7.zip \
&& rm geckodriver-arm7.zip \
&& mv geckodriver /bin/geckodriver \
&& chmod +x /bin/geckodriver

RUN sed -i 's/numpy/numpy==1.21.1/g' requirements.txt
RUN sed -i 's/opencv-python/opencv-python==4.5.3.56/g' requirements.txt
RUN pip install --extra-index-url https://www.piwheels.org/simple --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "anibot.py", "--configfile", "/config/ani.json" ]
CMD [ "--docker" ]
