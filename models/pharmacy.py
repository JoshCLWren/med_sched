"""Model for a pharmacy."""

from dataclasses import dataclass

from models.time import TimeOfDay


@dataclass
class Pharmacy:
    """Model for a pharmacy."""

    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone_number: str
    fax_number: str
    email: str
    website: str
    is_default: bool
    created_at: str
    updated_at: str
    id: int
