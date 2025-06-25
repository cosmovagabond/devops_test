# file: backend-go/Dockerfile

# Stage 1: Build the Go binary
FROM golang:1.19-alpine AS builder

WORKDIR /app

# Copy go.mod and go.sum files
COPY go.mod ./

# Download dependencies
RUN go mod download

# Copy the source code
COPY . .

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux go build -o /go-api-server .

# Stage 2: Create a minimal final image
FROM alpine:latest

# Copy the binary from the builder stage
COPY --from=builder /go-api-server /go-api-server

# Expose the port the API will run on
EXPOSE 8080

# Command to run the executable
CMD ["/go-api-server"]