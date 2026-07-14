import requests


BASE_URL = "https://www.sumo-api.com/api"


def get_bouts(
    basho_id: str,
    division: str,
    day: int,
) -> dict:
    """Download the bouts for one division and tournament day."""

    url = (
        f"{BASE_URL}/basho/{basho_id}"
        f"/torikumi/{division}/{day}"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    return response.json()