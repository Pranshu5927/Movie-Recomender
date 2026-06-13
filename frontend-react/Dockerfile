# Stage 1: Build React application
FROM node:18-slim as builder

WORKDIR /app

# Copy package.json and package-lock.json
COPY frontend-react/package*.json .

# Install dependencies
RUN npm ci --prefer-offline --no-audit

# Copy source code
COPY frontend-react/ .

# Build the React app
RUN npm run build

# Stage 2: Serve the built app with nginx
FROM nginx:alpine

# Copy built app from builder stage to nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY frontend-react/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (nginx default)
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1/ || exit 1

# Run nginx
CMD ["nginx", "-g", "daemon off;"]
