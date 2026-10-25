# Flock Energy API Wrapper

A REST API wrapper around the legacy Urja Meter Ops portal. This project exposes meter search, geographic coordinates, energy readings, and transformer data through a documented FastAPI interface.

## Features

- Meter listing and search with pagination
- Meter geographic data
- Meter energy readings
- Transformer listing with pagination
- Interactive API documentation through Swagger UI
- Automated tests using mocked HTTP responses
- Environment-based configuration for credentials

## Technology Stack

- Python
- FastAPI
- HTTPX
- Pydantic Settings
- Pytest
- RESPX

## Project Structure

```text
flock-energy-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── client.py
│   └── config.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.13 or a compatible Python version
- Access to the Urja Meter Ops portal
- The credentials supplied for the assignment

## Setup

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Set the following values in `.env`:

```text
URJA_BASE_URL=https://urja-ops.flockenergy.tech
URJA_USERNAME=your-assignment-email
URJA_PASSWORD=your-assignment-password
```

Use the actual credentials provided for the assignment. Never commit `.env` or publish credentials.

## Run the API

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8765
```

Open the interactive API documentation at:

`http://127.0.0.1:8765/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Health check |
| GET | `/api/meters` | List and search meters |
| GET | `/api/meters/{meter_id}/geo` | Retrieve meter coordinates |
| GET | `/api/meters/{meter_id}/energy` | Retrieve meter energy readings |
| GET | `/api/transformers` | List transformers |

### Query parameters

`GET /api/meters`

- `q` — optional meter search query
- `page` — page number, defaults to `1`

`GET /api/transformers`

- `page` — page number, defaults to `1`

## Run Tests

With the virtual environment activated:

```powershell
python -m pytest -v
```

The tests mock the legacy portal's HTTP responses, allowing API behavior to be tested without depending on live portal data.

## Error Handling

The API returns a `502 Bad Gateway` response when a legacy portal request fails. Error details are logged to the application terminal, while clients receive a generic error message.

## Security

- Credentials are loaded from environment variables.
- `.env` is excluded from version control.
- The API is intended for local development and assignment evaluation.
- The wrapper currently exposes read-only operations.

## Limitations and Future Improvements

- Add validation for meter identifiers.
- Improve handling of expired sessions and authentication failures.
- Add structured logging and more specific error responses.
- Add automated tests for upstream failures and invalid requests.
- Review dependency compatibility and pin production dependencies deliberately.

## License

Created as a take-home engineering assignment for evaluation.