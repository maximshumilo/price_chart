FROM node:16-alpine as build
COPY . /src
WORKDIR /src
RUN npm install -g npm@8.7.0
RUN npm ci --silent
RUN npm run build

FROM nginx:alpine
RUN rm -rf /usr/share/nginx/html/*
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY --from=build /src/build /usr/share/nginx/html
