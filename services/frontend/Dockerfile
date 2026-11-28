# Stage 1: build the static site with Node. Nothing from this stage ships except /app/dist.
FROM node:22-alpine AS build
WORKDIR /app
# Copy only the dependency files first so this layer is cached until they change.
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: serve the built files with nginx. Final image has no Node, no source, no node_modules.
# "unprivileged" = runs as a non-root user and listens on 8080 (non-root cannot bind port 80).
FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
