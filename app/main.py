
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query

from app.client import UrjaClient
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = UrjaClient(
        base_url=settings.urja_base_url,
        email=settings.urja_username,
        password=settings.urja_password,
    )
    app.state.urja_client = client
    yield
    await client.close()


app = FastAPI(
    title="Flock Energy API",
    description="A REST API wrapper for the legacy Urja Meter Ops portal",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Flock Energy API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/meters")
async def list_meters(
    q: str = Query(default="", description="Search meters"),
    page: int = Query(default=1, ge=1, description="Page number"),
):
    try:
        return await app.state.urja_client.get_meters(query=q, page=page)
    except Exception as exc:
        print(f"Legacy portal error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve meter data from the legacy portal.",
        ) from exc


@app.get("/api/meters/{meter_id}/geo")
async def get_meter_geo(meter_id: str):
    try:
        return await app.state.urja_client.get_meter_geo(meter_id)
    except Exception as exc:
        print(f"Legacy portal error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve meter geographic data.",
        ) from exc


@app.get("/api/meters/{meter_id}/energy")
async def get_meter_energy(meter_id: str):
    try:
        return await app.state.urja_client.get_meter_energy(meter_id)
    except Exception as exc:
        print(f"Legacy portal error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve meter energy data.",
        ) from exc
async def get_transformers(self, page: int = 1) -> dict:
    """Fetch a page of transformers from the legacy portal."""
    if not self.authenticated:
        await self.login()

    response = await self.session.get(
        "/portal/dts",
        params={"page": page},
    )
    response.raise_for_status()
    return response.json()
@app.get("/api/transformers")
async def list_transformers(
    page: int = Query(default=1, ge=1, description="Page number"),
):
    try:
        return await app.state.urja_client.get_transformers(page=page)
    except Exception as exc:
        print(f"Legacy portal error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve transformer data from the legacy portal.",
        ) from exc