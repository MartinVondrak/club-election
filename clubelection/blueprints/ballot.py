from flask import Blueprint, request

from clubelection.committee import Committee, CommitteeError
from clubelection.serialization import denormalizer, DenormalizerError
from clubelection.models import Ballot, Voter


def create_blueprint(committee: Committee) -> Blueprint:
    blueprint: Blueprint = Blueprint('ballot', __name__, url_prefix='/api')

    @blueprint.route('/ballot', methods=['POST'])
    def post_ballot():
        try:
            ballot: Ballot = denormalizer.denormalize(request.json, Ballot)
            voter: Voter = committee.get_voter(ballot.voter_id)
            committee.count_ballot(ballot, voter)
            print(f'{ballot.candidate_ids}')
        except DenormalizerError as error:
            return f'{error}', 400
        except CommitteeError as error:
            return f'{error}', 400

        return 'Created.', 201

    return blueprint
