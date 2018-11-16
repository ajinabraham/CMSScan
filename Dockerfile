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

WORKDIR /usr/src/app/
COPY . .

RUN gem install wpscan && \
  wpscan --update
RUN python3 -m pip install virtualenv && \
  virtualenv venv -p python3 && \
  . venv/bin/activate && \
  pip install --no-cache-dir -r requirements.txt
RUN git submodule update --init --recursive

WORKDIR /usr/src/app/plugins/vbscan/
RUN git pull origin master

WORKDIR /usr/src/app/plugins/joomscan/
RUN git pull origin master

EXPOSE 7070
CMD ["/usr/src/app/run.sh"]
