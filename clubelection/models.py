from typing import Optional


class Voter:
    id: Optional[int] = None

    def __init__(self, access_code: str, has_voted: bool):
        self.access_code = access_code
        self.has_voted = has_voted


class Candidate:
    id: Optional[int] = None

    def __init__(self, first_name: str, last_name: str, biography: str):
        self.first_name = first_name
        self.last_name = last_name
        self.biography = biography


class Vote:
    id: Optional[int] = None

    def __init__(self, candidate: Candidate):
        self.candidate = candidate


class Ballot:
    def __init__(self, voter_id: int, candidate_ids: list):
        self.voter_id: int = voter_id
        self.candidate_ids: list = candidate_ids
