# =============================================================================
# Multi-Stage Dockerfile for Django + Playwright PDF Generation
# Optimized for minimal image size
# =============================================================================

# =============================================================================
# Stage 1: Builder - Compile Python wheels
# =============================================================================
FROM python:3.12-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir -r requirements.txt -w /wheels


# =============================================================================
# Stage 2: Playwright - Download Chromium browser
# =============================================================================
FROM python:3.12-slim-bookworm AS playwright-builder

RUN pip install --no-cache-dir playwright && \
    playwright install chromium


# =============================================================================
# Stage 3: Runtime - Minimal production image
# =============================================================================
FROM python:3.12-slim-bookworm AS runtime

# Runtime dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    libffi8 \
    fonts-liberation \
    fonts-dejavu-core \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/playwright

# Install Python packages
COPY --from=builder /wheels /tmp/wheels
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /tmp/wheels/*.whl && \
    rm -rf /tmp/wheels

# Copy Playwright browser from builder
COPY --from=playwright-builder /root/.cache/ms-playwright /opt/playwright

# Install Chromium system dependencies (auto-detects distro)
RUN playwright install-deps chromium && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Rebuild font cache
RUN fc-cache -f -v

# Copy application
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Cleanup to reduce size
RUN find /app -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /app -type f -name "*.pyc" -delete 2>/dev/null || true && \
    rm -rf /app/.git /app/venv /app/env /app/.hypothesis /app/.vscode /app/.kiro 2>/dev/null || true

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "booksstore.wsgi:application", \
     "--bind=0.0.0.0:8000", \
     "--workers=4", \
     "--threads=2", \
     "--timeout=120"]
