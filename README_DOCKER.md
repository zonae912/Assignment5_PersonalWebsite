# Docker Setup Guide for Flask Personal Website

This guide will help you containerize and run your Flask personal website using Docker.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your system
- Basic understanding of Docker concepts

## What is Docker?

Docker allows you to package your application with all its dependencies into a standardized unit called a container. This ensures your app runs consistently across different environments.

## Files Added for Docker

1. **Dockerfile** - Instructions for building your Docker image
2. **.dockerignore** - Files to exclude from the Docker image
3. **docker-compose.yml** - Simplified Docker container management

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and start the container:**
   ```powershell
   docker-compose up --build
   ```

2. **Access your website:**
   Open your browser and go to `http://localhost:5000`

3. **Stop the container:**
   Press `Ctrl+C` in the terminal, then run:
   ```powershell
   docker-compose down
   ```

### Option 2: Using Docker Commands

1. **Build the Docker image:**
   ```powershell
   docker build -t flask-website .
   ```

2. **Run the container:**
   ```powershell
   docker run -d -p 5000:5000 --name my-website flask-website
   ```

3. **Access your website:**
   Open your browser and go to `http://localhost:5000`

4. **Stop the container:**
   ```powershell
   docker stop my-website
   ```

5. **Remove the container:**
   ```powershell
   docker rm my-website
   ```

## Useful Docker Commands

### View running containers:
```powershell
docker ps
```

### View all containers (including stopped):
```powershell
docker ps -a
```

### View container logs:
```powershell
docker logs my-website
# Or with docker-compose:
docker-compose logs
```

### Access container shell:
```powershell
docker exec -it my-website /bin/bash
# Or with docker-compose:
docker-compose exec web /bin/bash
```

### Rebuild after code changes:
```powershell
docker-compose up --build
```

## How It Works

1. **Dockerfile** - Defines the container environment:
   - Starts with Python 3.11 base image
   - Installs dependencies from `requirements.txt`
   - Copies your application files
   - Exposes port 5000
   - Runs your Flask app

2. **docker-compose.yml** - Simplifies running the container:
   - Automatically builds the image
   - Maps port 5000 to your local machine
   - Mounts the database file for data persistence
   - Sets environment variables

3. **app.py** - Modified to listen on `0.0.0.0` so it's accessible from outside the container

## Database Persistence

The `projects.db` file is mounted as a volume, which means:
- Your project data persists even when containers are stopped/removed
- You can modify the database and changes are immediately reflected

## Troubleshooting

### Port already in use:
If port 5000 is already in use, modify the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8000:5000"  # Access via localhost:8000
```

### Changes not reflected:
Rebuild the container after code changes:
```powershell
docker-compose up --build
```

### View detailed logs:
```powershell
docker-compose logs -f
```

## Production Considerations

For production deployment:
1. Change the `app.secret_key` in `app.py` to a secure random value
2. Consider using a production WSGI server like Gunicorn instead of Flask's built-in server
3. Use environment variables for sensitive configuration
4. Set up proper logging and monitoring

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Desktop Tutorial](https://docs.docker.com/get-started/workshop/)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/latest/deploying/)
