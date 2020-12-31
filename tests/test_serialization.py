import pytest

from clubelection.models import Candidate, Ballot
from clubelection.serialization import normalizer, NormalizerError, denormalizer, DenormalizerError


def test_should_normalize_candidate():
    candidate: Candidate = Candidate('Name', 'Surname', 'I am Name Surname!')
    normalized: dict = normalizer.normalize(candidate)
    assert normalized['id'] is None
    assert normalized['first_name'] == 'Name'
    assert normalized['last_name'] == 'Surname'
    assert normalized['biography'] == 'I am Name Surname!'


def test_should_normalize_candidate_list():
    candidate1: Candidate = Candidate('Name', 'Surname', 'I am Name Surname!')
    candidate1.id = 1
    candidate2: Candidate = Candidate('A', 'B', 'I am A B!')
    candidate2.id = 2
    normalized: list = normalizer.normalize([candidate1, candidate2])
    assert len(normalized) == 2
    assert normalized[0]['id'] == 1
    assert normalized[1]['id'] == 2


def test_should_raise_error_if_normalizing_unsupported_object_():
    with pytest.raises(NormalizerError):
        normalizer.normalize(object())


def test_should_denormalize_ballot():
    normalized_ballot: dict = {'voter_id': 1, 'candidate_ids': [1, 2, 3]}
    ballot: Ballot = denormalizer.denormalize(normalized_ballot, Ballot)
    assert ballot.voter_id == 1
    assert len(ballot.candidate_ids) == 3
    assert ballot.candidate_ids == [1, 2, 3]


def test_should_raise_error_if_denormalizing_invalid_ballot():
    with pytest.raises(DenormalizerError):
        normalized_ballot: dict = {'voter': 1, 'candidates': [1, 2, 3]}
        denormalizer.denormalize(normalized_ballot, Ballot)


def test_should_raise_error_if_denormalizing_unsupported_object():
    with pytest.raises(DenormalizerError):
        denormalizer.denormalize({}, object)
