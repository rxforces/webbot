from nginx:1.9.1

# Download packages
RUN apt-get update
RUN apt-get install -y curl \
                       git  \
                       build-essential

# install our code
copy content /usr/share/nginx/html/

# Installation
RUN curl -sL https://deb.nodesource.com/setup | bash -
RUN apt-get install -y nodejs
RUN apt-get clean

WORKDIR /usr/share/nginx/html

RUN npm install npm -g
RUN npm install -g bower
RUN npm install -g grunt-cli
RUN npm cache clean
RUN npm install
RUN bower --allow-root install -g

