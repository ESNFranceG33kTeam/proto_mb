FROM ubuntu:22.04

# Var for labels
ARG GITHUB_ACTOR
ARG GITHUB_REPOSITORY
ARG GITHUB_REF

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

ENV PROJECT_NAME="Module bénévole"

LABEL org.opencontainers.image.title="${PROJECT_NAME}" \
      org.opencontainers.image.authors=${GITHUB_ACTOR} \
      org.opencontainers.image.vendor=${GITHUB_REPOSITORY} \
      org.opencontainers.image.source="https://github.com/${GITHUB_ACTOR}/web_mb" \
      org.opencontainers.image.url="https://github.com/${GITHUB_ACTOR}/web_mb/tags" \
      org.opencontainers.image.description="Module benevole" \
      org.opencontainers.image.os="Ubuntu" \
      org.opencontainers.image.version=${GITHUB_REF}

RUN apt-get update -yq
RUN pip install streamlit

ADD mb/ /opt/mb/

ADD start.sh .

EXPOSE 8501

CMD ./start.sh
