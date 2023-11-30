# Stage 1: Playwright image for installation
FROM mcr.microsoft.com/playwright:focal as playwright

# Stage 2: Python image
FROM python:3.10

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy required files from Playwright image to Python image
COPY --from=playwright /usr/bin/microsoft-edge-dev /usr/bin/microsoft-edge-dev
COPY --from=playwright /usr/lib/microsoft-edge-dev /usr/lib/microsoft-edge-dev

COPY . /app

CMD ["python", "app.py"]
