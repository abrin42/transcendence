FROM python:3.8
RUN mkdir -p /home/app
COPY ./ /home/app/ft_transcendence
WORKDIR /home/app/ft_transcendence
RUN apt-get update
RUN apt-get install -y --no-install-recommends postgresql-client
# RUN rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=pong.settings

#RUN pip install python-dotenv
RUN pip install pyotp
RUN pip install django-phonenumber-field[phonenumberslite]
RUN pip install phonenumbers
RUN pip install vonage


#a enlever pour rendu (enleve la mise en cache)
ENV PYTHONUNBUFFERED=1
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["sh", "-c", "python3 manage.py makemigrations --noinput && python3 manage.py migrate && daphne -b 0.0.0.0 -p 8000 pong.asgi:application -t 512"]
# CMD ["sh", "-c", "daphne -b 0.0.0.0 -p 8000 pong.asgi:application -t 512"]
