"""
End-to-end test of run_pipeline() against the SQLite test DB.
External dependencies (Qdrant, sentence-transformers) are mocked.
"""
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import select

from app.db.models.user import Korisnik
from app.db.models.transcript import Transkript, Segment, TokenMapRecord, FormatTip, TranskStatusTip
from app.db.models.knowledge import UnosBazeZnanja


TRANSCRIPT_TEXT = (
    "Korisnik: Dobro jutro. Moj JMBG je 0101990012343.\n"
    "Agent: Dobar dan, kako Vam mogu pomoci?\n"
    "Korisnik: Zanimaju me uslovi kredita. Moj broj je 061 123 456.\n"
    "Agent: Naravno, mogu Vam pomoci s tim."
)


@pytest.mark.asyncio
async def test_run_pipeline_creates_segments_and_qa(setup_test_db):
    from app.db.session import AsyncSessionLocal
    from app.services.preprocessing.pipeline import run_pipeline

    fake_vector = [0.0] * 384
    mock_embed = MagicMock(return_value=fake_vector)
    mock_index = MagicMock()

    async with AsyncSessionLocal() as db:
        # Use the admin user created in conftest
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

        with (
            patch("app.services.preprocessing.pipeline._embedder.embed", mock_embed),
            patch("app.services.preprocessing.pipeline._vector_store.index_item", mock_index),
        ):
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
            assert row.vector_id is not None
            assert "0101990012343" not in row.pitanje

        tmr = (await db.execute(
            select(TokenMapRecord).where(TokenMapRecord.transkript_id == tid)
        )).scalar_one_or_none()
        assert tmr is not None
        assert "0101990012343" not in tmr.encrypted_blob
