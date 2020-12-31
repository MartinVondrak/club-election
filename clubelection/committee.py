from sqlalchemy.orm import Session

from clubelection.models import Ballot, Voter, Vote, Candidate


class Committee:
    def __init__(self, session: Session):
        self.session: Session = session

    def count_ballot(self, ballot: Ballot, voter: Voter) -> None:
        if voter.has_voted is True:
            raise CommitteeError(f'Voter ID "{voter.id}" has already voted.')
        for candidate_id in ballot.candidate_ids:
            vote: Vote = self.generate_vote(candidate_id)
            self.session.add(vote)
        voter.has_voted = True
        self.session.commit()

    def get_voter(self, voter_id: int) -> Voter:
        voter: Voter = self.session.query(Voter).get(voter_id)
        if voter is None:
            raise CommitteeError(f'Voter ID "{voter_id}" not found.')
        return voter

    def generate_vote(self, candidate_id: int) -> Vote:
        candidate: Candidate = self.session.query(Candidate).get(candidate_id)
        if candidate is None:
            raise CommitteeError(f'Candidate ID "{candidate_id}" not found.')
        return Vote(candidate)


class CommitteeError(Exception):
    pass
