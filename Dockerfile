FROM python:3
LABEL \
    name="CMSScan" \
    author="Ajin Abraham <ajin25@gmail.com>" \
    description="Scan WordPress, Joomla, vBulletin and Drupal CMS for Security issues"
RUN \
  apt-get update && \
  apt-get install -y ruby \
  ruby-dev \
  git

RUN gem install wpscan && \
  wpscan --update

WORKDIR /usr/src/app/
COPY . .
RUN python3 -m pip install virtualenv && \
  virtualenv venv -p python3 && \
  . venv/bin/activate && \
  pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/plugins/
RUN git clone https://github.com/rezasp/vbscan.git
RUN git clone https://github.com/rezasp/joomscan.git

EXPOSE 7070
CMD ["/usr/src/app/run.sh"]
