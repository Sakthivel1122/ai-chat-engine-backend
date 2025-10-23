# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Set Work Directory ----------
WORKDIR /app

# ---------- Install system dependencies ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ---------- Install Python dependencies ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy Django Project ----------
COPY . .

# ---------- Expose Port ----------
EXPOSE 8000

# ---------- Run Migrations & Start Server ----------
CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn your_django_app.wsgi:application --bind 0.0.0.0:8000"]
