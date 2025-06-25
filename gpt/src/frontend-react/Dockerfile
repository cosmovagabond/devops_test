# file: frontend-react/Dockerfile

# Stage 1: Build the React application
FROM node:16-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . ./

# Build the application for production
RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:stable-alpine

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built files from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for Nginx
EXPOSE 80

# When the container starts, Nginx will be started automatically
CMD ["nginx", "-g", "daemon off;"]