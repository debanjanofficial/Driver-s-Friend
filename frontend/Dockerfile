# ---------- Stage 1: Build React App ----------
    FROM node:23.5.0 AS builder

    # Create app directory
    WORKDIR /app
    
    # Copy package files and install dependencies
    COPY package*.json /app/
    RUN npm install
    
    # Copy the rest of the app source
    COPY . /app
    
    # Build the application (production mode)
    RUN npm run build
    
    # ---------- Stage 2: Serve with Nginx ----------
    FROM nginx:alpine
    
    # Copy build artifacts from the previous stage
    COPY --from=builder /app/build /usr/share/nginx/html
    
    # Expose port 80 for serving HTTP traffic
    EXPOSE 80
    
    # Start Nginx in the foreground
    CMD ["nginx", "-g", "daemon off;"]
    