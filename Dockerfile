FROM python:3
LABEL \
    name="CMSScan" \
    author="Ajin Abraham <ajin25@gmail.com>" \
    description="Scan WordPress, Joomla, vBulletin and Drupal CMS for Security issues"
RUN \
  apt-get update && \
  apt-get install -y ruby \
  ruby-dev \
  git \
  libwww-perl

RUN gem install wpscan && \
  wpscan --update

WORKDIR /usr/src/app/
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/rezasp/vbscan.git
RUN git clone https://github.com/rezasp/joomscan.git

RUN mv vbscan /usr/src/app/plugins/vbscan
RUN mv joomscan /usr/src/app/plugins/joomscan

EXPOSE 7070
CMD ["gunicorn", "--bind", "0.0.0.0:7070", "app:app", "--workers 3", "--timeout", "10000"]
