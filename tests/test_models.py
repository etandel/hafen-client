from datetime import datetime
from typing import Optional

import pytest

from hafen_client import Corpus, Text


class TestModels:
    def test__corpus(self, corpus: Corpus):
        assert (
            Corpus.parse_obj({"id": corpus.id, "reference": corpus.reference}) == corpus
        )

    @pytest.mark.parametrize("date", [None, datetime.now()])
    def test__text(self, text: Text, date: Optional[datetime]):
        text = text.copy(update={"date": date})
        assert (
            Text.parse_obj(
                {
                    "id": text.id,
                    "title": text.title,
                    "author": text.author,
                    "date": date and date.isoformat(),
                    "raw_text": text.raw_text,
                    "corpus": {
                        "id": text.corpus.id,
                        "reference": text.corpus.reference,
                    },
                }
            )
            == text
        )
