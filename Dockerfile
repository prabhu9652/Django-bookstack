# =========================
# Stage 1: Builder
# =========================
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    # WeasyPrint build dependencies
    libpango1.0-dev \
    libcairo2-dev \
    libgdk-pixbuf2.0-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir -r requirements.txt -w /wheels


# =========================
# Stage 2: Runtime
# =========================
FROM python:3.12-slim

# Install base runtime dependencies and fonts
# Note: Playwright dependencies are installed via 'playwright install-deps' below
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    # WeasyPrint runtime dependencies for PDF generation (fallback)
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libfribidi0 \
    libgdk-pixbuf2.0-0 \
    libffi8 \
    libcairo2 \
    libcairo-gobject2 \
    shared-mime-info \
    # Fonts for PDF rendering
    fonts-liberation \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    fontconfig \
    && fc-cache -f -v \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only wheels
COPY --from=builder /wheels /wheels

RUN pip install --upgrade pip && \
    pip install --no-cache-dir /wheels/*.whl && \
    rm -rf /wheels

# Install Playwright Chromium and its system dependencies
# install-deps must run first to install correct packages for the distro
RUN playwright install-deps chromium && \
    playwright install chromium

# Copy application code
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "booksstore.wsgi:application", \
     "--bind=0.0.0.0:8000", \
     "--workers=9", \
     "--threads=2", \
     "--timeout=120"]
