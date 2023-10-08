FROM node:lts-alpine AS build

RUN apk update && apk add python3
RUN apk add py3-pip

RUN apk add make

RUN npm install -g node-gyp

RUN apk add build-base

COPY ./website/ .
RUN npm i
RUN npm run build

# FROM nginx:alpine AS runtime
# COPY --from=build /dist /usr/share/nginx/html

# FROM lipanski/docker-static-website:latest AS runtime
# COPY --from=build /dist .
# CMD ["busybox", "httpd", "-f", "-v", "-p", "80", "-c", "httpd.conf"]

FROM busybox:latest AS runtime
COPY --from=build /dist .
CMD ["busybox", "httpd", "-f", "-v", "-p", "80"]