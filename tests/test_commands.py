import json

from hafen_client.commands import UpdateCorpus, Empty


class TestEmpty:
    def test__is_empty(self):
        class SubS(Empty):
            pass

        assert Empty.is_empty(Empty)
        assert Empty.is_empty(Empty())
        assert Empty.is_empty(SubS)
        assert Empty.is_empty(SubS())

        assert not Empty.is_empty(None)
        assert not Empty.is_empty(type(None))
        assert not Empty.is_empty(0)


class TestUpdateCorpus:
    def test__json_excludes_emptys(self):
        assert UpdateCorpus().json(exclude_unset=True) == json.dumps({})
        assert UpdateCorpus(reference="foo").json(exclude_unset=True) == json.dumps(
            {"reference": "foo"}
        )
