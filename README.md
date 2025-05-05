# REST API Example Project

A simple REST API example project with Docker and PostgreSQL.

## Prerequisites

- Docker (with Docker Compose)
- Git

## Getting Started

Follow these steps to set up and run the project:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pushinik/rest_example
   cd rest_example
   ```

2. **Prepare the environment**:
   ```bash
   mkdir -p .docker/pg_data
   cp .env.example .env
   ```

3. **Configure environment variables**:
   Edit the `.env` file to set your preferred configuration:
   ```bash
   nano .env
   ```

4. **Build and start containers**:
   ```bash
   docker compose up -d --build
   ```

## Project Structure

- `.docker/pg_data` - PostgreSQL data directory (persistent storage)
- `.env.example` - Example environment configuration
- `src/` - Application source code
- `compose.yml` - Docker Compose configuration

## Environment Variables

Key variables to configure in `.env`:

- `POSTGRES_*` - PostgreSQL database configuration
- `MAIL_*` - Mail configuration

## Common Commands

- Start containers: `docker compose up -d`
- Stop containers: `docker compose down`
- View logs: `docker compose logs -f`
- Rebuild containers: `docker compose up -d --build`

## Accessing the API

After startup, the API will be available at:
`http://localhost:8000/`
