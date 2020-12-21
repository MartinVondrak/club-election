class Voter:
    def __init__(self, access_code: str, has_voted: bool):
        self.access_code = access_code
        self.has_voted = has_voted


class Candidate:
    def __init__(self, first_name: str, last_name: str, biography: str):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.biography = biography


class Vote:
    def __init__(self, candidate: Candidate):
        self.candidate = candidate
