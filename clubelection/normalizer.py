from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import cast

from clubelection.models import Candidate


class AbstractNormalizer(ABC):
    @abstractmethod
    def supports(self, to_normalize: object) -> bool:
        pass

    @abstractmethod
    def normalize(self, to_normalize: object) -> dict:
        pass


class CandidateNormalizer(AbstractNormalizer):

    def supports(self, to_normalize: object) -> bool:
        return type(to_normalize) is Candidate

    def normalize(self, to_normalize: object) -> dict:
        candidate: Candidate = cast(Candidate, to_normalize)
        return {
            'id': candidate.id,
            'first_name': candidate.first_name,
            'last_name': candidate.last_name,
            'biography': candidate.biography
        }


class Normalizer:
    def __init__(self, normalizers: list):
        self.normalizers = normalizers

    def normalize(self, to_normalize: object):
        for normalizer in self.normalizers:
            if normalizer.supports(to_normalize):
                return normalizer.normalize(to_normalize)
        if isinstance(to_normalize, Iterable):
            result: list = []
            for item in to_normalize:
                result.append(self.normalize(item))
            return result
        raise NormalizerError(f'Cannot normalize type: {type(to_normalize)}!')


class NormalizerError(Exception):
    pass


normalizer = Normalizer([CandidateNormalizer()])
