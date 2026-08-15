# Teaching image: Python 3 + R (no Bioconductor yet — keep the first build fast).
# Pin the tag in an audit; bump deliberately.
FROM python:3.12-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends r-base \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/lab
COPY summarize.py summarize.R /opt/lab/
# data/ is bind-mounted at runtime
