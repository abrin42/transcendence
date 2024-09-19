FROM node:lts-alpine as build
RUN mkdir /app
COPY ./front /app/front
WORKDIR /app/front
RUN npm install
RUN npm install vue-i18n@9
RUN npm run build


FROM nginx:1.25.3
RUN rm -rf /var/www/html
RUN mkdir -p /etc/nginx/ssl
COPY --from=build /app/front/dist /var/www/html
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 8000

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