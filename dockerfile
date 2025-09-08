# --- Stage 1: Build the application ---
    FROM node:18-alpine AS builder
    WORKDIR /app
    COPY package*.json ./
    RUN npm install
    COPY . .
    # If you have a build step, you would run it here
    # RUN npm run build
    
    # --- Stage 2: Create the final, smaller image ---
    FROM node:18-alpine
    WORKDIR /app
    # Copy only the necessary files from the builder stage
    COPY --from=builder /app/node_modules ./node_modules
    COPY --from=builder /app/package*.json ./
    COPY --from=builder /app .
    
    EXPOSE 8080
    CMD [ "node", "index.js" ]