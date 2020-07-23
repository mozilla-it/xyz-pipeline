FROM python:3

COPY pipeline /workspace/pipeline
COPY pyproject.toml .coveragerc /workspace/
WORKDIR /workspace


RUN pip install . && \
    pip install tox && \
    tox
