import requests
import os
from urllib.parse import quote_plus


def _base_url():
    """Return API base URL from env or a sensible default (root, no path).

    Ensure this does not include `/clients` so endpoints are built correctly.
    """
    return (os.getenv("API_URL") or "http://127.0.0.1:5000").rstrip("/")


def get_clients(timeout: float = 5.0):
    # If DATABASE_URL is set, prefer direct DB access
    if os.getenv('DATABASE_URL'):
        try:
            from db_client import get_clients as db_get_clients
            return db_get_clients()
        except Exception:
            # fall back to HTTP if DB client fails
            pass
    url = f"{_base_url()}/clients?format=json"
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_person(fio: str, timeout: float = 5.0):
    if os.getenv('DATABASE_URL'):
        try:
            from db_client import get_person as db_get_person
            return db_get_person(fio)
        except Exception:
            pass
    url = f"{_base_url()}/clients/{quote_plus(fio)}?format=json"
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_orders(fio: str, timeout: float = 5.0):
    if os.getenv('DATABASE_URL'):
        try:
            from db_client import get_orders as db_get_orders
            return {'orders': db_get_orders(fio)}
        except Exception:
            pass
    url = f"{_base_url()}/clients/{quote_plus(fio)}/orders?format=json"
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def update_person(fio: str, data: dict, timeout: float = 5.0):
    """Send JSON PUT to update a person via API."""
    # Server supports form POST for edit; use that endpoint
    url = f"{_base_url()}/clients/{quote_plus(fio)}/edit"
    resp = requests.post(url, data=data, timeout=timeout)
    resp.raise_for_status()
    # return server response text (HTML or message)
    return resp.text


def delete_person(fio: str, timeout: float = 5.0):
    url = f"{_base_url()}/clients/{quote_plus(fio)}/delete"
    resp = requests.post(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def add_client(name, phone, timeout: float = 5.0):
    payload = {"fio": name, "phone": phone}
    url = f"{_base_url()}/clients/create"
    resp = requests.post(url, data=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.text
