"""Deterministic educational industrial energy indicators."""
from __future__ import annotations
import hashlib
import json
from pydantic import BaseModel, Field

class Factory(BaseModel):
    id: str
    name: str
    units_produced: int = Field(gt=0)
    energy_kwh: float = Field(ge=0)
    source_type: str = 'synthetic'

def intensity(factory: Factory) -> float:
    return factory.energy_kwh / factory.units_produced

def compare(factory: Factory, baseline: Factory) -> dict:
    if factory.units_produced != baseline.units_produced:
        raise ValueError('Production volumes must match for direct comparison')
    saved = baseline.energy_kwh - factory.energy_kwh
    pct = saved / baseline.energy_kwh * 100 if baseline.energy_kwh else None
    return {'factory': factory.name, 'energy_kwh': factory.energy_kwh,
            'units_produced': factory.units_produced,
            'kwh_per_unit': round(intensity(factory), 3),
            'energy_difference_kwh': round(saved, 3),
            'energy_difference_pct': None if pct is None else round(pct, 2)}

def sha256(data: object) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()
