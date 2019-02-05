#
# Drew Gallis
# CSEC 380
# HW 1
# Nginx Dockerfile Config File
#

# Pull base image.
FROM ubuntu

# File Author / Maintainer
MAINTAINER Drew Gallis

# Finding and Installing Proper Libraries
RUN apt-get update
RUN apt-get install -y software-properties-common

# Install Nginx and related directories.
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y nginx 
RUN rm -rf /var/lib/apt/lists/*
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf 
RUN chown -R www-data:www-data /var/lib/nginx
RUN rm -rf /var/www/html/index.nginx-debian.html
ADD index.html /var/www/html/
RUN mkdir /etc/nginx/logs


# Defining Voulmes needed for nginx to work properly
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx", "/var/www/html"]

# Base Working Director
WORKDIR /etc/nginx

# Add load balancing
#LABEL traefik.backend=backend-nginx-web
#LABEL traefik.frontend.rule=Host:nginx-web.docker.localhost,nginx-web.dgallis.local

#allows me to control precedence in load balancing applications
#LABEL traefik.weight=2

# Defining Ports
EXPOSE 80
EXPOSE 443

# Setting Command Base Call
CMD ["nginx"]
