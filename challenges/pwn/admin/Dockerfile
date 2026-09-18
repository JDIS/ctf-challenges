FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/challenge
COPY vuln ./vuln
RUN chmod +x ./vuln

EXPOSE 1337
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./vuln,stderr"]
