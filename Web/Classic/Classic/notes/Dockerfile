FROM php:8.1-fpm

WORKDIR /var/www/html

COPY public/index.php /var/www/html/index.php

RUN chown -R root:root /var/www/html
RUN touch /var/log/fpm-php.www.log
RUN chmod 777 /var/log/fpm-php.www.log

COPY www.conf /usr/local/etc/php-fpm.d/www.conf

EXPOSE 9000
