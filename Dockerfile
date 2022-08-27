# FIXME use multi-stage build
# ARG BASEIMAGE=
# ARG BASEIMAGE_USECASE=

# FIXME --platform=x86_64 ${BASEIMAGE}
FROM docker.io/library/python:3.8-slim as baseimage

LABEL site="https://qte77.github.io"
LABEL author="qte77"

# don't generate .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# no buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN set -xe \
  && python -m ensurepip --upgrade \
  && pip install --no-cache-dir --upgrade setuptools wheel
RUN rm -rf /var/cache/apt/* /tmp/* \
  /usr/lib/python*/ensurepip

# TODO --platform=x86_64 ${BASEIMAGE_USECASE}
FROM baseimage as usecase

# EXPOSE 8080

ARG USER="user"
ARG HOME="/home/${USER}"
ARG FILES_IN="./app"
ARG FILES_OUT="${HOME}/app"
ARG FILES_CONF="${FILES_OUT}/config"
ARG APP="${FILES_OUT}/app.py"
ARG WANDB_KEYFILE=".wandb/wandb.key"
# ARG WANDB_KEY="<token>"

RUN useradd -m -d ${HOME} ${USER}
USER ${USER}
WORKDIR ${HOME}

ENV PATH="${FILES_OUT}:/home/user/.local/bin:${PATH}"
# ENV WANDB_KEY=${WANDB_KEY}

COPY --chown=${USER}:${USER} ${WANDB_KEYFILE} \
  "${HOME}/${WANDB_KEYFILE}"
COPY --chown=${USER}:${USER} ${FILES_IN} ${FILES_OUT}

RUN set -xe \
  && pip install --no-cache-dir --user \
    -r "${FILES_OUT}/requirements.txt"

RUN chmod +x ${APP}
ENTRYPOINT ${APP}

# TODO FastAPI etc.
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "app.py:app"]
