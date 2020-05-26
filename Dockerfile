FROM httpd
RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN pip3 install Django==3.0.6
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
COPY docker_httpd.conf /usr/local/apache2/conf/httpd.conf
RUN mkdir /root/keeptrack
ADD . /root/keeptrack/
RUN rm /root/keeptrack/docker_httpd.conf /root/keeptrack/Dockerfile
RUN chmod +x /root
EXPOSE 80
CMD ["httpd-foreground"]
