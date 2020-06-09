FROM python:3

COPY pipeline /workspace/pipeline
COPY pyproject.toml /workspace/
WORKDIR /workspace


RUN pip install .
RUN pip install tox
RUN tox