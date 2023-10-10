# Backend-users-proyecto
## Create image users
1. Create image users: `docker build -t users_app .`
2. Create and run container: `docker run -d -p 3001:3001 -e DATABASE_URL=postgresql://postgres:admin@host.docker.internal:5432/postgres users_app`