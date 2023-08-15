FROM node:14.16.1
#FROM node:15.5.0-buster

WORKDIR /app

#COPY frontend/package.json /app
#RUN yarn install

COPY frontend/package*.json /app/
RUN npm install

#CMD ["bash", "-c", "yarn install && yarn run dev"]
ENTRYPOINT ["npm", "run", "dev"]