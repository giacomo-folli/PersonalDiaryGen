# Docker Guide for Monthly Reflection Diary

This document provides instructions for building, running, and updating the Docker image for the Monthly Reflection Diary application.

## Prerequisites

- [Docker](https://www.docker.com/) installed on your machine
- Basic knowledge of Docker commands
- Your OpenAI API key

## Building the Docker Image

To build the Docker image for the first time:

```bash
# Navigate to the project directory
cd path/to/monthly-reflection-diary

# Build the Docker image
docker build -t reflection-diary:latest .
```

This will create a Docker image named `reflection-diary` with the tag `latest`.

## Running the Application

### Using SQLite (Default)

To run the application with SQLite:

```bash
# Create a directory for persistent data if it doesn't exist
mkdir -p data/instance

# Run the container
docker run -d \
  --name reflection-diary \
  -p 5000:5000 \
  -v $(pwd)/data/instance:/app/instance \
  -e SECRET_KEY=your_secure_key \
  -e OPENAI_API_KEY=your_openai_api_key \
  reflection-diary:latest
```

### Using PostgreSQL

To run the application with PostgreSQL:

```bash
docker run -d \
  --name reflection-diary \
  -p 5000:5000 \
  -e SECRET_KEY=your_secure_key \
  -e DATABASE_URL=postgresql://username:password@host:port/database \
  -e OPENAI_API_KEY=your_openai_api_key \
  reflection-diary:latest
```

## Accessing the Application

After starting the container, you can access the application at:

```
http://localhost:5000
```

## Updating the Application

When you make changes to your application, follow these steps to update the Docker image and container:

1. **Stop and remove the existing container**:

   ```bash
   docker stop reflection-diary
   docker rm reflection-diary
   ```

2. **Build a new image with the updated code**:

   ```bash
   docker build -t reflection-diary:latest .
   ```

   Optionally, you can use versioned tags:

   ```bash
   docker build -t reflection-diary:v1.1 .
   ```

3. **Start a new container with the updated image**:

   ```bash
   docker run -d \
     --name reflection-diary \
     -p 5000:5000 \
     -v $(pwd)/data/instance:/app/instance \
     -e SECRET_KEY=your_secure_key \
     -e OPENAI_API_KEY=your_openai_api_key \
     reflection-diary:latest
   ```

## Docker Compose (Optional)

For a more streamlined setup, especially when using PostgreSQL, you can use Docker Compose:

1. Create a `docker-compose.yml` file:

```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data/instance:/app/instance
    environment:
      - SECRET_KEY=your_secure_key
      - OPENAI_API_KEY=your_openai_api_key
      # Uncomment for PostgreSQL:
      # - DATABASE_URL=postgresql://username:password@db:5432/diary_db
    depends_on:
      # Uncomment for PostgreSQL:
      # - db
    restart: unless-stopped
  
  # Uncomment for PostgreSQL:
  # db:
  #   image: postgres:14
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   environment:
  #     - POSTGRES_USER=username
  #     - POSTGRES_PASSWORD=password
  #     - POSTGRES_DB=diary_db
  #   restart: unless-stopped

# Uncomment for PostgreSQL:
# volumes:
#   postgres_data:
```

2. Start the application with Docker Compose:

```bash
docker-compose up -d
```

3. Update the application with Docker Compose:

```bash
docker-compose stop
docker-compose build
docker-compose up -d
```

## Environment Variables

The following environment variables can be configured:

- `SECRET_KEY`: Secret key for Flask sessions (required)
- `OPENAI_API_KEY`: Your OpenAI API key (required for AI features)
- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)
- `FLASK_ENV`: Set to 'production' for production mode (optional, defaults to 'development')
- `PORT`: Port to run the application on (optional, defaults to 5000)

## Troubleshooting

### Container won't start

Check the logs:

```bash
docker logs reflection-diary
```

### Database connection issues

If using PostgreSQL, ensure:
- The database server is running
- The connection URL is correct
- Network connectivity between containers if using Docker Compose

### Volume permissions

If you encounter permission issues with the SQLite database:

```bash
# Fix permissions on the host
sudo chown -R 1000:1000 ./data/instance
```

## Backup and Restore

### Backup the SQLite Database

```bash
docker cp reflection-diary:/app/instance/diary.db ./backup/diary.db
```

### Restore the SQLite Database

```bash
docker cp ./backup/diary.db reflection-diary:/app/instance/diary.db
```