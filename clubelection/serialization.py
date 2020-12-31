from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import cast, List, Type

from clubelection.models import Candidate, Ballot


class AbstractNormalizer(ABC):
    @abstractmethod
    def supports(self, data: object) -> bool:
        pass

    @abstractmethod
    def normalize(self, data: object) -> dict:
        pass


class CandidateNormalizer(AbstractNormalizer):

    def supports(self, data: object) -> bool:
        return type(data) is Candidate

    def normalize(self, data: object) -> dict:
        candidate: Candidate = cast(Candidate, data)
        return {
            'id': candidate.id,
            'first_name': candidate.first_name,
            'last_name': candidate.last_name,
            'biography': candidate.biography
        }


class Normalizer:
    def __init__(self, normalizers: List[AbstractNormalizer]):
        self.normalizers: List[AbstractNormalizer] = normalizers

    def normalize(self, data: object):
        for normalizer in self.normalizers:
            if normalizer.supports(data):
                return normalizer.normalize(data)
        if isinstance(data, Iterable):
            result: list = []
            for item in data:
                result.append(self.normalize(item))
            return result
        raise NormalizerError(f'Cannot normalize type "{type(data)}"!')


class NormalizerError(Exception):
    pass


class AbstractDenormalizer(ABC):
    @abstractmethod
    def supports(self, data: dict, to_class: Type) -> bool:
        pass

    @abstractmethod
    def denormalize(self, data: dict) -> object:
        pass


class BallotDenormalizer(AbstractDenormalizer):
    def supports(self, data: dict, to_class: Type) -> bool:
        return to_class is Ballot

    def denormalize(self, data: dict) -> Ballot:
        try:
            return Ballot(data['voter_id'], data['candidate_ids'])
        except Exception as error:
            raise DenormalizerError(error)


class Denormalizer:
    def __init__(self, denormalizers: List[AbstractDenormalizer]):
        self.denormalizers: List[AbstractDenormalizer] = denormalizers

    def denormalize(self, data: dict, to_class: Type):
        for denormalizer in self.denormalizers:
            if denormalizer.supports(data, to_class):
                return denormalizer.denormalize(data)
        raise DenormalizerError(f'Cannot denormalize type "{type(data)}" to "{to_class}"!')


class DenormalizerError(Exception):
    pass


normalizer: Normalizer = Normalizer([CandidateNormalizer()])
denormalizer: Denormalizer = Denormalizer([BallotDenormalizer()])
