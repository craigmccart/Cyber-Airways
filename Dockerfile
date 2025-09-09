# --- Stage 1: Build the application ---
FROM node:18-alpine AS builder
WORKDIR /app

# Look inside the 'frontend' subfolder for the package files
COPY frontend/package*.json ./
RUN npm install

# Look inside the 'frontend' subfolder for the rest of the app code
COPY frontend/. .

# --- Stage 2: Create the final, smaller image ---
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app .

EXPOSE 8080
CMD [ "npm", "start" ]
