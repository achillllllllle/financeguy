FROM node:16-slim

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install -D vite@4.5.0

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"] 