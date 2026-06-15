FROM python:3.13-slim

EXPOSE 8080

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1


WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --format requirements-txt --no-hashes --output-file requirements.txt
RUN uv pip install --system --requirements requirements.txt

COPY . .

CMD ["gunicorn", "dio_website.wsgi:application", "--bind", "0.0.0.0:8080"]
