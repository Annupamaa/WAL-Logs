# WAL Log Dashboard (Flask + PostgreSQL)

## Tech Used
- Python + Flask
- PostgreSQL
- Docker + Docker Compose
- Basic HTML/JS

## Setup Instructions
1. Clone the repo or copy files
2. Run: `docker-compose up --build`
3. Access:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000

## API Usage
### GET /logs
Headers: Authorization: Bearer secret-token

### POST /simulate-replay
Body:
{
  "start": "2024-01-01T00:00:00",
  "end": "2024-12-31T23:59:59"
}
# WAL-Logs
