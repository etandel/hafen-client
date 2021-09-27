from typing import AsyncGenerator
from urllib.parse import urljoin

import pytest
from aiohttp import ClientSession
from aioresponses.core import aioresponses, RequestCall
from yarl import URL

from hafen_client import Corpus, HafenClient
from hafen_client.client import Response
from hafen_client.commands import CreateCorpus, UpdateCorpus


@pytest.fixture
def mockresponse():
    with aioresponses() as m:
        yield m


class TestClient:
    @pytest.fixture
    async def client(self) -> AsyncGenerator[HafenClient, None]:
        async with HafenClient() as c:
            yield c

    async def test__init(self):
        c = HafenClient()
        assert c._base_uri == ""
        assert isinstance(c._session, ClientSession)

        c = HafenClient("foo")
        assert c._base_uri == "foo"
        assert isinstance(c._session, ClientSession)

    class TestContextManager:
        async def test__context_manager(self, client: HafenClient):
            async with client:
                assert client._session.closed is False

            assert client._session.closed is True

        async def test__close__ok(self, client: HafenClient):
            assert client._session.closed is False

            await client.close()
            assert client._session.closed is True

        async def test__close__already_closed(self, client: HafenClient):
            await client.close()
            assert client._session.closed is True

            await client.close()
            assert client._session.closed is True

    class TestGetUrl:
        async def test__ok(self):
            c = HafenClient("/base/")
            assert c._get_url("foo") == "/base/foo"

    class TestCorpusCrud:
        BASE_URI = "corpora/"

        def get_url(self, path):
            return urljoin(self.BASE_URI, path)

        async def test__create(self, client: HafenClient, mockresponse, corpus: Corpus):
            url = self.get_url("")
            mockresponse.post(url, body=Response(data=corpus).json())

            data = CreateCorpus(reference=corpus.reference)
            assert (await client.create_corpus(data)) == corpus

            assert mockresponse.requests == {
                ("POST", URL(url)): [
                    RequestCall(args=(), kwargs={"data": data.json(exclude_unset=True)})
                ]
            }

        async def test__update(self, client: HafenClient, mockresponse, corpus: Corpus):
            url = self.get_url(f"{corpus.id}")

            expected_calls = []
            for field, value in corpus:
                mockresponse.patch(url, body=Response(data=corpus).json())

                data = UpdateCorpus(**{field: value})
                assert (await client.update_corpus(corpus.id, data)) == corpus

                expected_calls.append(
                    RequestCall(args=(), kwargs={"data": data.json(exclude_unset=True)})
                )

            assert mockresponse.requests == {("PATCH", URL(url)): expected_calls}

        async def test__get(self, client: HafenClient, mockresponse, corpus: Corpus):
            response = Response(data=corpus).json()
            mockresponse.get(self.get_url(f"{corpus.id}"), body=response)
            assert (await client.get_corpus(corpus.id)) == corpus

        async def test__list(self, client: HafenClient, mockresponse, corpus: Corpus):
            expected = [
                corpus.dict(),
                corpus.copy(update=dict(id=corpus.id + 1)).dict(),
            ]
            mockresponse.get(self.get_url(""), payload={"data": expected})
            assert (await client.list_corpora()) == expected
