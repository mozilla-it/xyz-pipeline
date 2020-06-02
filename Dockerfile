FROM python:3

COPY pipeline /workspace/pipeline
COPY pyproject.toml /workspace/
WORKDIR /workspace

RUN pip install poetry
RUN poetry install
RUN poetry run tox