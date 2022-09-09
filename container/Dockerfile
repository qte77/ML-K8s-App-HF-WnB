FROM docker.io/library/python:3.9-slim as baseimage

LABEL site="https://qte77.github.io"
LABEL author="qte77"

ARG USER="user"
ARG APP="./app"
ARG APP_EP="${APP_FILES}/app.py"
ARG REQS="./reqs"
ARG WANDB_KEYFILE=".wandb/wandb.key"
# ARG WANDB_KEY="<token>"

EXPOSE 8080
RUN useradd -m ${USER}
USER ${USER}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="${APP}:/home/user/.local/bin:${PATH}"
# ENV WANDB_KEY=${WANDB_KEY}

COPY --chown=${USER}:${USER} ${REQS} ${REQS}
COPY --chown=${USER}:${USER} ${APP} ${APP}
# COPY --chown=${USER}:${USER} ${WANDB_KEYFILE} \
#   "${HOME}/${WANDB_KEYFILE}"

RUN set -xe && \
    pip install --no-cache-dir --user \
        -r "${REQS}/app-reqs.txt"
RUN set -xe && \
    pip install --no-cache-dir --user \
        -r "${REQS}/mlds-reqs.txt"
RUN set -xe && \
    pip install --no-cache-dir --user \
        -r "${REQS}/hf-reqs.txt"
RUN set -xe && \
    pip install --no-cache-dir --user \
        -r "${REQS}/torch-reqs.txt"

ENTRYPOINT [ "/bin/sh" ]

# RUN chmod +x ${APP_EP}
# ENTRYPOINT ["${APP_EP}"]

# TODO FastAPI etc.
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "app.py:app"]
