FROM python:3
LABEL maintainer="Jorge Spiropulo jspiropulo@mozilla.com"
COPY pipeline /workspace/pipeline
COPY setup.py /workspace/
WORKDIR /workspace
RUN pip3 install --upgrade --no-cache-dir .
RUN behave pipeline/tests/bdd