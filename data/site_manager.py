import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_FILE = os.path.join(BASE_DIR, "data", "monitoring_sites.json")


DEFAULT_SITES = {
    "SHL-01": {
        "name": "Shillong Site 01",
        "city": "Shillong",
        "state": "Meghalaya",
        "latitude": 25.5788,
        "longitude": 91.8933,
        "status": "ONLINE"
    },
    "GUW-01": {
        "name": "Guwahati Site 01",
        "city": "Guwahati",
        "state": "Assam",
        "latitude": 26.1445,
        "longitude": 91.7362,
        "status": "ONLINE"
    },
    "AIZ-01": {
        "name": "Aizawl Site 01",
        "city": "Aizawl",
        "state": "Mizoram",
        "latitude": 23.7271,
        "longitude": 92.7176,
        "status": "ONLINE"
    },
    "KOH-01": {
        "name": "Kohima Site 01",
        "city": "Kohima",
        "state": "Nagaland",
        "latitude": 25.6751,
        "longitude": 94.1086,
        "status": "ONLINE"
    },
    "ITA-01": {
        "name": "Itanagar Site 01",
        "city": "Itanagar",
        "state": "Arunachal Pradesh",
        "latitude": 27.0844,
        "longitude": 93.6053,
        "status": "ONLINE"
    }
}


def load_sites():

    if not os.path.exists(SITE_FILE):

        save_sites(DEFAULT_SITES)

        return DEFAULT_SITES.copy()

    try:

        with open(
            SITE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            sites = json.load(file)

        return sites

    except Exception:

        save_sites(DEFAULT_SITES)

        return DEFAULT_SITES.copy()


def save_sites(sites):

    os.makedirs(
        os.path.dirname(SITE_FILE),
        exist_ok=True
    )

    with open(
        SITE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            sites,
            file,
            indent=4
        )


def add_site(
    site_id,
    name,
    city,
    state,
    latitude,
    longitude
):

    sites = load_sites()

    site_id = site_id.strip().upper()

    if site_id in sites:

        return False, "Site ID already exists."

    sites[site_id] = {
        "name": name.strip(),
        "city": city.strip(),
        "state": state.strip(),
        "latitude": float(latitude),
        "longitude": float(longitude),
        "status": "ONLINE"
    }

    save_sites(sites)

    return True, f"{site_id} added successfully."


def delete_site(site_id):

    sites = load_sites()

    if site_id not in sites:

        return False, "Site not found."

    del sites[site_id]

    save_sites(sites)

    return True, f"{site_id} deleted successfully."
