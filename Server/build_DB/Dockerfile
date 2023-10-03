# cat Dockerfile
FROM mysql:5.7

#COPY .env /app/env
RUN chown -R mysql:root /var/lib/mysql/

ARG MYSQL_DATABASE
ARG MYSQL_ROOT_PASSWORD

VOLUME /data:/var/lib/mysql
VOLUME ./mysql/my.cnf:/etc/mysql/my.cnf

ENV MYSQL_DATABASE="weblogin"
ENV MYSQL_ROOT_PASSWORD=12345
ENV MYSQL_PORT=3306
COPY code_create_database.sql /docker-entrypoint-initdb.d/

# RUN sed -i 's/MYSQL_DATABASE/'$MYSQL_DATABASE'/g' /etc/mysql/data.sql
# RUN cp data.sql /docker-entrypoint-initdb.d

EXPOSE 3306

#  docker build -t vnutour2023_db:v9 -f Dockerfile .
# docker run --name vnu_db -p 8080:3306 -d vnutour2023_db:v9
# docker start vnu_db

