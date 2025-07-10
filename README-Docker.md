# Task Management Backend - Docker Setup

This guide will help you set up the Task Management backend using Docker for easy development and deployment.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### 1. Build and Run with Docker Compose

```bash
# Navigate to the backend directory
cd task_management

# Build and start all services
docker-compose up --build

### 2. Access the Application

- **Backend API**: http://localhost:9000
- **API Documentation**: http://localhost:9000/api/schema/swagger-ui/
- **Redis**: localhost:6379

### 3. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: This will delete data)
docker-compose down -v
```
