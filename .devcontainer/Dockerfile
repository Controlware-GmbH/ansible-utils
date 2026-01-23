FROM mcr.microsoft.com/devcontainers/python:3.13-trixie

ARG DEBIAN_FRONTEND=noninteractive

ENV PIP_NO_CACHE_DIR 1
ENV PIP_ROOT_USER_ACTION ignore

###
### Install OS basics & helpers
###
RUN apt-get update
RUN apt-get install -y bash-completion && apt-get clean all

USER vscode
# Install Python packages which are not or outdated in OS repo
RUN --mount=type=bind,source=requirements-dev.txt,target=/tmp/requirements.txt \
    pip install --upgrade -r /tmp/requirements.txt
