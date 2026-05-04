FROM python:3.13-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1
ENV DJANGO_SETTINGS_MODULE=dio_website.settings.dev


WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv export --frozen --format requirements-txt --no-hashes --output-file requirements.txt
RUN uv pip install --system --requirements requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
