FROM node:lts-alpine as build
RUN mkdir /app
COPY ./front /app/front
WORKDIR /app/front
RUN npm install
RUN npm install vue-i18n@10
RUN npm run build

FROM nginx:1.25.3
RUN rm -rf /var/www/html
RUN mkdir -p /etc/nginx/ssl
COPY --from=build /app/front/dist /var/www/html
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /etc/nginx/ssl
COPY certificates/server.crt /etc/nginx/ssl/server.crt
COPY certificates/server.key /etc/nginx/ssl/server.key
WORKDIR /etc/nginx/ssl
RUN chmod 644 server.crt
RUN chmod 600 server.key
EXPOSE 8000
EXPOSE 8443