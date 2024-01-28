# cat Dockerfile
FROM mysql:5.7

#COPY .env /app/env
RUN chown -R mysql:root /var/lib/mysql/

ARG MYSQL_DATABASE
ARG MYSQL_ROOT_PASSWORD

VOLUME /data:/var/lib/mysql
VOLUME ./mysql/my.cnf:/etc/mysql/my.cnf

ENV MYSQL_DATABASE="weblogin"
ENV MYSQL_ROOT_PASSWORD=123456
ENV MYSQL_PORT=3306
COPY code_create_database.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

