from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class EscalationInfo(BaseModel):
    escalation_id: int
    status: str
    queue_position: int
    trigger_tip: str


class EscalationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sesija_id: int
    korisnik_id: str
    dodjeljeni_agent_id: Optional[str] = None
    prioritet: str
    status: str
    trigger_tip: Optional[str] = None
    tema: Optional[str] = None
    razgovor: Optional[List[dict]] = None
    datum_kreiranja: datetime
    datum_rjesavanja: Optional[datetime] = None
    napomena_rjesavanja: Optional[str] = None
    queue_position: Optional[int] = None


class EscalationResolve(BaseModel):
    napomena: str = ""
    submit_to_kb: bool = False
    odgovor_agenta: Optional[str] = None
    pitanje_korisnika: Optional[str] = None


class AgentStatusUpdate(BaseModel):
    status: str
