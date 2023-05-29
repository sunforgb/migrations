FROM node:18-alpine

ARG PROJ_DIR=/frontend

RUN  mkdir -p ${PROJ_DIR}
COPY ./frontend ${PROJ_DIR}

WORKDIR ${PROJ_DIR}
RUN yarn install

ENV PATH="/node_modules/.bin:$PATH"

CMD ["yarn", "serve"]