FROM python:3.6.7-stretch

RUN apt-get update && apt-get install -y \
		default-libmysqlclient-dev build-essential \
		libssl-dev libffi-dev python3-dev python3-pip && \
	apt-get clean && \
	cp /usr/local/lib/python3.6/configparser.py /usr/local/lib/python3.6/ConfigParser.py

COPY ./pyladies/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && \
	rm  /tmp/requirements.txt

# supervisor
RUN apt-get install -y supervisor && \
	echo """[program:flask]\n\
directory=/var/www/html/website2018/pyladies\n\
command=python manage.py runserver --host=0.0.0.0\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/supervisor/flask.err.log\n\
stdout_logfile=/var/log/supervisor/flask.out.log""" > /etc/supervisor/conf.d/flask.conf

RUN echo """[supervisord]\nnodaemon=true""" > /etc/supervisor/conf.d/supervisord.conf


EXPOSE 5000
WORKDIR /var/www/html/website2018/pyladies
CMD /usr/bin/supervisord