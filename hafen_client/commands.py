from typing import TypeVar, Union

from pydantic import BaseModel


class _EmptyIter:
    def __next__(self):
        raise StopIteration()

    def __iter__(self):
        return self


class Empty:
    @classmethod
    def is_empty(cls, cls_or_obj):
        return isinstance(cls_or_obj, Empty) or (
            isinstance(cls_or_obj, type) and issubclass(cls_or_obj, Empty)
        )

    @classmethod
    def __get_validators__(cls):
        yield from _EmptyIter()


T = TypeVar("T")
EmptyT = Union[Empty, T]


class CreateCorpus(BaseModel):
    reference: str


class UpdateCorpus(BaseModel):
    reference: EmptyT[str] = Empty()
