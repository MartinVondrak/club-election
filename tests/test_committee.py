import pytest
from flexmock import flexmock
from sqlalchemy.orm import Session

from clubelection.committee import Committee, CommitteeError
from clubelection.models import Voter, Ballot, Candidate, Vote


def test_should_not_count_ballot_and_raise_error_if_voter_has_already_voted():
    voter: Voter = Voter('code', True)
    voter.id = 1
    ballot: Ballot = Ballot(voter.id, [1, 2, 3])
    committee: Committee = Committee(flexmock(Session()))
    with pytest.raises(CommitteeError):
        committee.count_ballot(ballot, voter)


def test_should_generate_vote():
    candidate: Candidate = Candidate('name', 'last_name', 'bio')
    candidate.id = 10
    query_mock = flexmock()
    query_mock.should_receive('get').with_args(10).and_return(candidate).once()
    session_mock = flexmock(Session())
    session_mock.should_receive('query').with_args(Candidate).and_return(query_mock).once()
    committee: Committee = Committee(session_mock)
    actual_vote: Vote = committee.generate_vote(10)
    assert actual_vote.id is None
    assert actual_vote.candidate is candidate


def test_should_not_generate_vote_and_raise_error_if_candidate_not_found():
    query_mock = flexmock()
    query_mock.should_receive('get').with_args(10).and_return(None).once()
    session_mock = flexmock(Session())
    session_mock.should_receive('query').with_args(Candidate).and_return(query_mock).once()
    committee: Committee = Committee(session_mock)
    with pytest.raises(CommitteeError):
        committee.generate_vote(10)


def test_should_get_voter():
    expected_voter: Voter = Voter('a', False)
    expected_voter.id = 1
    query_mock = flexmock()
    query_mock.should_receive('get').with_args(1).and_return(expected_voter).once()
    session_mock = flexmock(Session())
    session_mock.should_receive('query').with_args(Voter).and_return(query_mock).once()
    committee: Committee = Committee(session_mock)
    actual_voter = committee.get_voter(1)
    assert expected_voter is actual_voter


def test_should_raise_error_if_voter_does_not_exist():
    query_mock = flexmock()
    query_mock.should_receive('get').with_args(2).and_return(None).once()
    session_mock = flexmock(Session())
    session_mock.should_receive('query').with_args(Voter).and_return(query_mock).once()
    committee: Committee = Committee(session_mock)
    with pytest.raises(CommitteeError):
        committee.get_voter(2)
