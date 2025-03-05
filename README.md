# Backend - Technician Scheduler API

## Overview
The Technician Scheduler API allows users to book, check, and cancel technician appointments through a FastAPI-powered backend. It integrates with a database and provides authentication for secure access.

## Features
- User authentication (login/register)
- Book a technician
- Check existing bookings
- Cancel a booking
- AI-powered chatbot for natural language processing

## Installation & Setup
### Using Docker (Recommended)
1. Clone the repository:
   ```bash
   git clone <backend-repo-url>
   cd backend
   ```
2. Start the backend with Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:8000`

### Manual Setup
1. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Start the database (PostgreSQL required):
   ```bash
   docker-compose up db
   ```
3. Start the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/users/register/` | Register a new user |
| POST   | `/users/login/` | Authenticate and get a token |
| POST   | `/ai/bookings/` | AI-based technician booking |
| GET    | `/bookings/` | Get all user bookings |
| DELETE | `/bookings/{id}/` | Cancel a booking |

## Example Usage
### Booking a Technician
```json
{
  "user_input": "I want to book a plumber for tomorrow at 3PM"
}
```
Response:
```json
{
  "message": "Booking confirmed with John Doe (Plumber) on Wednesday at 3:00 PM",
  "booking_id": 123
}
```

## Running Backend & Frontend Together
1. Clone both repositories:
   ```bash
   git clone <backend-repo-url>
   git clone <frontend-repo-url>
   ```
2. Navigate to the frontend and install dependencies:
   ```bash
   cd frontend
   npm install
   ```
3. Start both applications using `concurrently`:
   ```bash
   npm run start:both
   ```
   This runs both the backend and frontend at once.
