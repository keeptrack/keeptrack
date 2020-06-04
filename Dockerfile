FROM httpd
RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN apt-get install wget -y
RUN mkdir /root/mod_wsgi \
    && cd /root/mod_wsgi \
    && wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.7.1.tar.gz \
    && tar xfz 4.7.1.tar.gz \
    && cd mod_wsgi-4.7.1 \
    && ./configure --with-python=/usr/bin/python3 \
    && make \
    && cp src/server/.libs/mod_wsgi.so /usr/local/apache2/modules/mod_wsgi.so \
    && cd /root \
    && rm -R mod_wsgi
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt && rm /root/requirements.txt
RUN mkdir /var/django && chown -R daemon:daemon /var/django
RUN chown -R daemon:daemon /usr/local/apache2/logs
ADD --chown=daemon:daemon . /var/django/
RUN mv /var/django/docker_httpd.conf /usr/local/apache2/conf/httpd.conf
USER daemon
RUN rm -R /var/django/static && SECRET_KEY=dummy APP_DEBUG=1 python3 /var/django/manage.py collectstatic
RUN SECRET_KEY=dummy APP_DEBUG=1 python3 /var/django/manage.py migrate
CMD ["httpd-foreground"]
