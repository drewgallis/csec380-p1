#
# Drew Gallis
# CSEC 380
# Flask Dockerfile Config File
# Personal GAM


FROM mariadb:10
COPY schema.sql /docker-entrypoint-initdb.d/schema.sql
ENV MYSQL_ROOT_PASSWORD = "test123"
ENV MYSQL_DATABASE = "mydb"
EXPOSE 3306
