FROM node:19

WORKDIR /app

COPY src/app .
COPY src/flag.txt /199ab15c-fe1a-4ef1-9529-522588e1e505/flag.txt

RUN npm install

EXPOSE 80
CMD [ "node", "app.js" ]
