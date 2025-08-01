# Maternal Health App Deployment Guide

## Overview

This project demonstrates a Dockerized Flask application deployed with Docker Compose, featuring two web service containers and a load balancer. The load balancer distributes traffic between the two web instances for high availability and scalability.

---

## Docker Hub Image

- **Repository:** [https://hub.docker.com/r/sandoo17/maternalapp](https://hub.docker.com/r/sandoo17/maternalapp)
- **Image Name:** `sandoo17/maternalapp`
- **Tags:** `latest`, `v2` (use `latest` for deployment)

---

## Build Instructions

To build the image locally (if you want to reproduce or modify):

```bash
# Clone the repository
git clone <your-repo-url>
cd Summative_playing_around_with_api

# Build the Docker image
docker build -t sandoo17/maternalapp:latest .
```

---

## Run Instructions

### Using Docker Compose

The provided `compose.yml` sets up:

- `web-01` on `172.20.0.11:8080`
- `web-02` on `172.20.0.12:8080`
- `lb-01` (load balancer) on `172.20.0.10:8082`

Start all services:

```bash
docker compose -f web_infra_lab/compose.yml up -d
```

### Manual Run (for individual containers)

```bash
# Run Web01
docker run -d --name web-01 -p 8080:8080 sandoo17/maternalapp:latest

# Run Web02
docker run -d --name web-02 -p 8081:8080 sandoo17/maternalapp:latest
```

---

## Load Balancer Configuration

Assuming you use HAProxy (adjust if using Nginx):

**Example HAProxy config (`lb/haproxy.cfg`):**
```
frontend http_front
    bind *:8080
    default_backend web_servers

backend web_servers
    balance roundrobin
    server web01 172.20.0.11:8080 check
    server web02 172.20.0.12:8080 check
```

**Reload HAProxy after changes:**
```bash
docker exec lb-01 service haproxy reload
```
or restart the container:
```bash
docker compose restart lb-01
```

---

## Testing Steps & Evidence

1. **Access the load balancer:**  
   Open [http://localhost:8082](http://localhost:8082) in your browser.

2. **Verify round-robin:**  
   - Refresh the page multiple times.
   - You should see responses alternating between Web01 and Web02 (add a hostname or container name to your Flask response for clarity).

3. **Direct access:**  
   - Test [http://localhost:8080](http://localhost:8080) for Web01.
   - Test [http://localhost:8081](http://localhost:8081) for Web02.

---

## Hardening: Handling Secrets

**Do not bake secrets (API keys, passwords) into your image.**  
Instead, use environment variables:

- In `compose.yml`:
  ```yaml
  environment:
    - API_KEY=${API_KEY}
  ```
- Pass secrets at runtime:
  ```bash
  docker run -e API_KEY=your_key_here ...
  ```

Update your Flask app to read secrets from `os.environ`.

---

## Acceptance Criteria Checklist

- [x] Application runs correctly in both containers (`web-01` & `web-02`)
- [x] HAProxy (`lb-01`) routes requests to both web instances
- [x] Docker image is publicly available and reproducible
- [x] README is precise and complete

---

## Troubleshooting

- If you see only one web instance responding, check HAProxy config and container health.
- Ensure Flask runs on `0.0.0.0:8080` inside the container.
- Use `docker compose logs` for debugging.

---

## Contact

For questions or issues, open an issue on the repository or contact the maintainer.
