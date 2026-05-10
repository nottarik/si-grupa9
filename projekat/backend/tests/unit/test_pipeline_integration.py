"""
End-to-end test of run_pipeline() against the SQLite test DB.
Embedding and Qdrant are no longer part of the pipeline (moved to approval step).
"""
import pytest
from sqlalchemy import select

from app.db.models.user import Korisnik
from app.db.models.transcript import Transkript, Segment, TokenMapRecord, FormatTip, TranskStatusTip
from app.db.models.knowledge import UnosBazeZnanja


TRANSCRIPT_TEXT = (
    "Korisnik: Dobro jutro, zanimaju me uslovi za novi mobilni paket. Moj JMBG je 0101990012343.\n"
    "Agent: Dobar dan, hvala sto ste nas kontaktirali. Za novi mobilni paket mozete odabrati jednu od tri opcije koje nudimo.\n"
    "Korisnik: Koji dokumenti su potrebni za promjenu paketa? Moj broj je 061 123 456.\n"
    "Agent: Za promjenu paketa potrebna je samo vasa licna karta i popunjen zahtjev koji mozete preuzeti na nasoj web stranici ili u poslovnici."
)


@pytest.mark.asyncio
async def test_run_pipeline_creates_segments_and_qa(setup_test_db):
    from app.db.session import AsyncSessionLocal
    from app.services.preprocessing.pipeline import run_pipeline

    async with AsyncSessionLocal() as db:
        admin = (await db.execute(
            select(Korisnik).where(Korisnik.email == "admin@test.com")
        )).scalar_one()

        transkript = Transkript(
            naziv="test_pipeline.txt",
            format=FormatTip.tekst,
            raw_text=TRANSCRIPT_TEXT,
            status=TranskStatusTip.sirovi,
            id_korisnika_upload=admin.id,
        )
        db.add(transkript)
        await db.commit()
        await db.refresh(transkript)
        tid = transkript.id

        result = await run_pipeline(tid, TRANSCRIPT_TEXT, db)
        await db.commit()

        assert result.transcript_id == tid
        assert result.entity_count >= 2
        assert result.chunk_count >= 4
        assert result.qa_pair_count >= 2
        assert "0101990012343" not in result.masked_text
        assert "061 123 456" not in result.masked_text

        segs = (await db.execute(
            select(Segment).where(Segment.id_transkripta == tid)
        )).scalars().all()
        assert len(segs) == result.chunk_count

        qa_rows = (await db.execute(
            select(UnosBazeZnanja).where(UnosBazeZnanja.id_segmenta.isnot(None))
        )).scalars().all()
        assert len(qa_rows) == result.qa_pair_count
        for row in qa_rows:
            assert "0101990012343" not in row.pitanje

        tmr = (await db.execute(
            select(TokenMapRecord).where(TokenMapRecord.transkript_id == tid)
        )).scalar_one_or_none()
        assert tmr is not None
        assert "0101990012343" not in tmr.encrypted_blob
