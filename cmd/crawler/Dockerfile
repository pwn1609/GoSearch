from golang:1.25 AS builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY cmd/ ./cmd/
COPY internal/ ./internal/

RUN CGO_ENABLED=0 GOOS=linux go build -o crawler ./cmd/crawler

FROM debian:bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/crawler .

cmd ["./crawler"]