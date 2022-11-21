# Build frontend
FROM node:lts-bullseye AS build
WORKDIR /frontend
COPY ./src/frontend ./
RUN npm install && npm run build

# Prepare backend
FROM python:3.10-slim-bullseye
WORKDIR /app
RUN pip3 install --upgrade pip
COPY ./src/app/requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir --upgrade
COPY ./src/app ./app

# Add frontend build to app
COPY --from=build /frontend/dist ./app/dist

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]