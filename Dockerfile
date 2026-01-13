# =========================
# Stage 1: Builder (compile dependencies)
# =========================
FROM python:3.12-slim-bookworm AS builder

# Install only build-time dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy and build wheels
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir -r requirements.txt -w /wheels


# =========================
# Stage 2: Playwright (browser installation)
# =========================
FROM python:3.12-slim-bookworm AS playwright-stage

# Install playwright and download browser
RUN pip install --no-cache-dir playwright && \
    playwright install chromium

# Browser is stored in /root/.cache/ms-playwright


# =========================
# Stage 3: Runtime (minimal final image)
# =========================
FROM python:3.12-slim-bookworm AS runtime

# Install minimal runtime dependencies
# Playwright install-deps handles Chromium libs automatically
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core runtime libs
    libjpeg62-turbo \
    zlib1g \
    libffi8 \
    # Fonts for PDF rendering
    fonts-liberation \
    fonts-dejavu-core \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/playwright

# Install Python packages from wheels
COPY --from=builder /wheels /tmp/wheels
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /tmp/wheels/*.whl && \
    rm -rf /tmp/wheels

# Copy pre-installed Playwright browser
COPY --from=playwright-stage /root/.cache/ms-playwright /opt/playwright

# Install Playwright Chromium system dependencies
# This command auto-detects the distro and installs correct packages
RUN playwright install-deps chromium && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Rebuild font cache
RUN fc-cache -f -v

# Copy application code
COPY . .

# Setup entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Cleanup unnecessary files to reduce size
RUN find /app -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /app -type f -name "*.pyc" -delete 2>/dev/null || true && \
    rm -rf /app/.git /app/venv /app/env /app/.hypothesis 2>/dev/null || true

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "booksstore.wsgi:application", \
     "--bind=0.0.0.0:8000", \
     "--workers=4", \
     "--threads=2", \
     "--timeout=120"]
