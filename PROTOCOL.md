# Legacy Portal Protocol Notes

## 1. Overview

The Flock Energy API wrapper communicates with the legacy Urja Meter Ops portal at:

`https://urja-ops.flockenergy.tech`

The wrapper exposes selected read-only portal operations through a REST API built with FastAPI. HTTPX is used to make asynchronous requests to the legacy service.

## 2. Authentication

### Login request

- **Method:** POST
- **Path:** `/login`
- **Content type:** `application/x-www-form-urlencoded`
- **Form fields:**
  - `email`
  - `password`

The login request includes the following headers:

- `Accept: application/json`
- `Origin: https://urja-ops.flockenergy.tech`
- `Referer: https://urja-ops.flockenergy.tech/login`
- `x-sveltekit-action: true`

The HTTPX client retains cookies across requests using a persistent asynchronous session.

Authentication is initiated lazily when a protected operation is called for the first time.

## 3. Discovered Legacy Endpoints

### 3.1 Meter search

- **Method:** GET
- **Path:** `/portal/meters/search`
- **Query parameters:**
  - `q` — optional search query
  - `page` — page number

The response contains a `data` array and pagination metadata, including `total`, `page`, and `pageSize`.

Observed meter fields include:

- `meterId`
- `serialNo`
- `make`
- `phaseType`
- `installStatus`
- `dtCode`

### 3.2 Meter geographic data

- **Method:** GET
- **Path:** `/portal/meters/{meter_id}/geo`

The response contains a `data` object with `latitude` and `longitude` fields.

### 3.3 Meter energy readings

- **Method:** GET
- **Path:** `/portal/meters/{meter_id}/energy`

The response contains a `data` array of energy readings. Observed fields include:

- `timestamp`
- `kwh`
- `kvah`
- `voltR`

The observed timestamp format is `DD/MM/YYYY HH:mm`. The portal's timezone has not been independently verified.

### 3.4 Transformer listing

- **Method:** GET
- **Path:** `/portal/dts`
- **Query parameters:**
  - `page` — page number

The response contains a `data` array and pagination metadata. Observed transformer fields include:

- `code`
- `name`
- `feederCode`
- `capacityKva`

## 4. Wrapper API Mapping

| Wrapper endpoint | Legacy endpoint |
|---|---|
| `GET /api/meters` | `GET /portal/meters/search` |
| `GET /api/meters/{meter_id}/geo` | `GET /portal/meters/{meter_id}/geo` |
| `GET /api/meters/{meter_id}/energy` | `GET /portal/meters/{meter_id}/energy` |
| `GET /api/transformers` | `GET /portal/dts` |

The wrapper forwards the relevant query parameters and returns the legacy JSON response.

## 5. Error Handling

Successful upstream responses are passed through as JSON.

The wrapper currently converts exceptions raised during upstream operations into a `502 Bad Gateway` response with a generic client-facing message. The underlying exception type and message are printed to the application terminal for debugging.

Further improvements could distinguish authentication failures, missing resources, rate limiting, and upstream availability issues.

## 6. Session and Security Considerations

- Credentials are loaded from environment variables.
- The HTTPX session retains cookies for subsequent requests.
- The wrapper is designed for read-only operations.
- Credentials and session cookies must not be committed to source control or included in logs.
- The current implementation does not yet automatically re-authenticate after an expired session.
- The current implementation does not independently verify that the login response represents a successful application-level login.

## 7. Investigation Method

The endpoint paths, HTTP methods, request parameters, response structures, and login requirements were identified by inspecting the portal's browser network requests and checking the resulting responses.

The wrapper endpoints were then exercised through the local FastAPI Swagger interface. Automated tests use mocked HTTP responses to verify wrapper behavior without depending on the live portal.

## 8. Known Limitations

- Portal behavior may change independently of this wrapper.
- Upstream response schemas are passed through rather than normalized into dedicated response models.
- Authentication expiry and retries need more robust handling.
- Additional validation and tests for upstream failures would improve reliability.
