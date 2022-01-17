FROM mysql:8

ENV MYSQL_DATABASE igralci
ENV MYSQL_USER test
ENV MYSQL_PASSWORD test
ENV MYSQL_ROOT_PASSWORD test

COPY ./init.sql /docker-entrypoint-initdb.d
