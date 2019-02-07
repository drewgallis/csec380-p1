#
# Drew Gallis
# CSEC 380
# Nginx Dockerfile Config File
#

# Pull base image.
FROM nginx:alpine

# File Author / Maintainer
MAINTAINER Drew Gallis

# Install Nginx and related directories.
COPY index.html /usr/share/nginx/html/


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
