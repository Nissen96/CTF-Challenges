# Pull from own fork of i3geo/i3geo to avoid challenge breaking from official updates to :latest
FROM nissen96/i3geo:8.0-alfa

USER root

WORKDIR /var/www/i3geo/

COPY src/flag.php ./
COPY src/ms_configura.php ./
COPY src/index.js ./init/
COPY src/psymap.png ./init/imagens

RUN apt update && apt upgrade -y

# Runs on port 8080 by default, update Apache configs to use port 80
RUN sed -i 's/8080/80/g' /etc/apache2/ports.conf /etc/apache2/sites-available/000-default.conf

ENTRYPOINT ["bash"]

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]
