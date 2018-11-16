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
RUN ./setup.sh
EXPOSE 7070

CMD ["/usr/src/app/run.sh"]
