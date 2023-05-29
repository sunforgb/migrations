FROM django:4.1.5-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG PROJ_DIR=/backend

RUN mkdir -p ${PROJ_DIR}
COPY ./backend ${PROJ_DIR}

WORKDIR ${PROJ_DIR}

COPY ./compose/backend/entry.sh /entry.sh
RUN chmod +x /entry.sh
ENTRYPOINT [ "/entry.sh" ]