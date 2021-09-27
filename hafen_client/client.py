from typing import Generic, List, TypeVar
from urllib.parse import urljoin

from aiohttp import ClientSession
from pydantic import parse_raw_as
from pydantic.generics import GenericModel

from hafen_client.models import Corpus
from hafen_client.commands import CreateCorpus, UpdateCorpus


DataT = TypeVar("DataT")


class Response(GenericModel, Generic[DataT]):
    data: DataT


class HafenClient:
    def __init__(self, base_uri=""):
        self._base_uri = base_uri
        self._session = ClientSession()

    async def close(self):
        await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, _exc_type, _exc_value, _exc_traceback):
        await self.close()

    def _get_url(self, path: str) -> str:
        return urljoin(self._base_uri, path)

    async def get_corpus(self, corpus_id: int) -> Corpus:
        async with self._session.get(self._get_url(f"corpora/{corpus_id}")) as resp:
            resp.raise_for_status()
            return parse_raw_as(Response[Corpus], await resp.text()).data

    async def list_corpora(self) -> List[Corpus]:
        async with self._session.get(self._get_url("corpora/")) as resp:
            resp.raise_for_status()
            return parse_raw_as(Response[List[Corpus]], await resp.text()).data

    async def create_corpus(self, data: CreateCorpus) -> Corpus:
        url = self._get_url(f"corpora/")
        async with self._session.post(url, data=data.json(exclude_unset=True)) as resp:
            resp.raise_for_status()
            return parse_raw_as(Response[Corpus], await resp.text()).data

    async def update_corpus(self, corpus_id: int, data: UpdateCorpus) -> Corpus:
        url = self._get_url(f"corpora/{corpus_id}")
        async with self._session.patch(url, data=data.json(exclude_unset=True)) as resp:
            resp.raise_for_status()
            return parse_raw_as(Response[Corpus], await resp.text()).data
