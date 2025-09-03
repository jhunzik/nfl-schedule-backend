"""
Data models for the application.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Location:
    venue: str
    city: str


@dataclass
class Game:
    id: str
    homeTeam: str
    awayTeam: str
    startTime: datetime
    location: Location
    type: str
