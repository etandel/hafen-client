import inspect

import pytest

from hafen_client import Corpus, Text


def pytest_collection_modifyitems(session, config, items):
    """
    This is a pytest hook that automatically marks all async test cases
    to be collected and run.
    """
    for item in items:
        if isinstance(item, pytest.Function) and inspect.iscoroutinefunction(
            item.function
        ):
            item.add_marker(pytest.mark.asyncio)


@pytest.fixture
def corpus() -> Corpus:
    return Corpus(id=23, reference="A Corpus")


@pytest.fixture
def text(corpus: Corpus) -> Text:
    return Text(
        id=27,
        title="A Text",
        author="Inigo Montoya",
        date=None,
        raw_text="this is the text",
        corpus=corpus,
    )
