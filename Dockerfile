FROM python:3

COPY pipeline pyproject.toml .coveragerc /workspace/pipeline
WORKDIR /workspace


RUN pip install . && \
    pip install tox && \
    tox
