FROM node:lts-alpine as build
RUN mkdir /app
COPY ./front /app/front
WORKDIR /app/front
RUN npm install
RUN npm install vue-i18n@10
RUN npm run build
RUN sleep 3


FROM nginx:1.25.3
RUN rm -rf /var/www/html
RUN mkdir -p /etc/nginx/ssl
COPY --from=build /app/front/dist /var/www/html
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /etc/nginx/ssl
COPY certificat/certificate.crt /etc/nginx/ssl/certificate.crt
COPY certificat/privatekey.pem /etc/nginx/ssl/privatekey.pem
WORKDIR /etc/nginx/ssl
RUN chmod 644 certificate.crt
RUN chmod 644 privatekey.pem
EXPOSE 8000
EXPOSE 8443

# COPY --from=build /app/front/dist /var/www/html

# COPY static/ /usr/share/nginx/html/static/
# COPY media/ /usr/share/nginx/html/media/
# WORKDIR /var/www/html





# FROM nginx:1.25.3
# RUN rm -rf /var/www/html
# RUN mkdir -p /etc/nginx/ssl

# RUN mkdir /app
# COPY ./front /app/www/html
# # COPY --from=build /app/frontend/dist /var/www/html
# COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
# # COPY static/ /usr/share/nginx/html/static/
# # COPY media/ /usr/share/nginx/html/media/
# EXPOSE 8000