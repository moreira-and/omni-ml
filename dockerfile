FROM python:3.10-slim

ENV POETRY_VERSION="poetry>=2.0.0,<3.0.0" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
RUN pip install "$POETRY_VERSION"

 
COPY pyproject.toml ./ 
COPY poetry.lock ./ 
COPY src ./
COPY README.md ./
COPY LICENSE ./

RUN poetry config virtualenvs.create false \
 && poetry install --without dev --no-interaction --no-ansi --no-root

EXPOSE 8000 5000

ENV MLFLOW_TRACKING_URI=http://127.0.0.1:5000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
