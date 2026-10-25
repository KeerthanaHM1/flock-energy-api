
import httpx


class UrjaClient:
    """HTTP client for the legacy Urja Meter Ops portal."""

    def __init__(
        self,
        base_url: str,
        email: str,
        password: str,
    ):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.password = password
        self.authenticated = False

        self.session = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            follow_redirects=True,
        )

    async def login(self) -> None:
        """Authenticate and retain the session cookie."""
        response = await self.session.post(
            "/login",
            data={
                "email": self.email,
                "password": self.password,
            },
            headers={
                "Accept": "application/json",
                "Origin": self.base_url,
                "Referer": f"{self.base_url}/login",
                "x-sveltekit-action": "true",
            },
        )
        response.raise_for_status()
        self.authenticated = True

    async def get_meters(
        self,
        query: str = "",
        page: int = 1,
    ) -> dict:
        """Fetch a page of meters from the legacy portal."""
        if not self.authenticated:
            await self.login()

        response = await self.session.get(
            "/portal/meters/search",
            params={"q": query, "page": page},
        )
        response.raise_for_status()
        return response.json()

    async def get_meter_geo(self, meter_id: str) -> dict:
        """Fetch geographic coordinates for a meter."""
        if not self.authenticated:
            await self.login()

        response = await self.session.get(
            f"/portal/meters/{meter_id}/geo"
        )
        response.raise_for_status()
        return response.json()

    async def get_meter_energy(self, meter_id: str) -> dict:
        """Fetch energy readings for a meter."""
        if not self.authenticated:
            await self.login()

        response = await self.session.get(
            f"/portal/meters/{meter_id}/energy"
        )
        response.raise_for_status()
        return response.json()

    async def get_transformers(
        self,
        page: int = 1,
    ) -> dict:
        """Fetch a page of transformers from the legacy portal."""
        if not self.authenticated:
            await self.login()

        response = await self.session.get(
            "/portal/dts",
            params={"page": page},
        )
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        """Close the HTTP session."""
        await self.session.aclose()
