FROM python:3.11-bookworm

# Install Node.js 20.x from NodeSource
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy uv from official image
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for Docker layer caching
COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json ./frontend/
COPY backend/pyproject.toml backend/uv.lock ./backend/

# Install all dependencies (Node + Python)
RUN npm ci \
    && npm ci --prefix frontend \
    && cd backend && uv sync --frozen

# Copy source code
COPY . .

# Set build-time env vars for Vite
ARG VITE_API_BASE_URL=http://localhost:5001
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# Build frontend with Vite
RUN cd frontend && npm run build

# Railway assigns PORT dynamically; frontend=3000, backend=5001
ENV PORT=3000
ENV HOST=0.0.0.0
EXPOSE 3000 5001

# Start both frontend and backend concurrently
CMD ["npm", "run", "dev"]
