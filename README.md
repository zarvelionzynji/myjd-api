# myjd-api

This project provides a lightweight Docker image that exposes a simple REST API for sending download links to **MyJDownloader**.  
It is built using the Python library:  
https://github.com/mmarquezs/My.Jdownloader-API-Python-Library

I created this image to automate my personal download workflow using **n8n**, but it can be used with any automation tool that supports HTTP requests.

---

## Features
- Simple REST endpoint (`/add`) to send links directly to your JDownloader device.
- Supports optional `packageName`.
- Automatically connects to MyJDownloader on startup.
- Minimal Docker image based on Python + Waitress.

---

## Installation (Docker Compose)

```yaml
services:
  myjd-api:
    image: ghcr.io/zarvelionzynji/myjd-api:latest
    container_name: myjd-api
    ports:
      - 8069:5000
    environment:
      - JD_EMAIL=your@email
      - JD_PASSWORD=your_password
      - JD_DEVICE=your_device
    restart: unless-stopped
````

### Environment Variables

|Variable|Description|
|---|---|
|`JD_EMAIL`|Your MyJDownloader account email|
|`JD_PASSWORD`|Your account password|
|`JD_DEVICE`|Device name shown in JDownloader|

---

## Usage Example (HTTP Request)

Send a POST request to add a link:

### **cURL Example**
#### Add a link 

```bash
curl -X POST http://localhost:8069/add \
     -H "Content-Type: application/json" \
     -d '{
        "url": "https://example.com/file.zip"
     }'
````

#### Add a link (optional: with packageName)

```bash
curl -X POST http://localhost:8069/add \
     -H "Content-Type: application/json" \
     -d '{
        "url": "https://example.com/file.zip",
        "packageName": "My Package"
     }'
```

### Response Example

```json
{
  "success": true,
  "result": "Link added successfully"
}
```

---

## License

MIT — feel free to use and modify.

---

