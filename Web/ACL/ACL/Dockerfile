FROM node:18-alpine

RUN apk add --no-cache openssl tini

RUN adduser -D -u 1001 web

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

RUN FLAG_NAME=$(openssl rand -hex 10) && \
    echo "flag{test)}" > /flag_$FLAG_NAME && \
    chmod 644 /flag_$FLAG_NAME && \
    chown root:root /flag_$FLAG_NAME

EXPOSE 3000

USER web

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "app.js"]
