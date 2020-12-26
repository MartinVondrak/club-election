import pytest

from clubelection.models import Candidate
from clubelection.normalizer import normalizer, NormalizerError


def test_candidate():
    candidate: Candidate = Candidate('Name', 'Surname', 'I am Name Surname!')
    normalized: dict = normalizer.normalize(candidate)
    assert normalized['id'] is None
    assert normalized['first_name'] == 'Name'
    assert normalized['last_name'] == 'Surname'
    assert normalized['biography'] == 'I am Name Surname!'


def test_candidate_list():
    candidate1: Candidate = Candidate('Name', 'Surname', 'I am Name Surname!')
    candidate1.id = 1
    candidate2: Candidate = Candidate('A', 'B', 'I am A B!')
    candidate2.id = 2
    normalized: list = normalizer.normalize([candidate1, candidate2])
    assert len(normalized) == 2
    assert normalized[0]['id'] == 1
    assert normalized[1]['id'] == 2


def test_fail():
    with pytest.raises(NormalizerError):
        normalizer.normalize(object())
