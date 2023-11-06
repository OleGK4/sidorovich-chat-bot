FROM python:3.11
# set work directory
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
# install dependencies
RUN pip install --user aiogram 3.1, peewee 3.1
# run app
CMD ["python", "bot.py"]

