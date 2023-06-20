from .models import Player, Match
from sqlalchemy import func


def EloCalc(winner_id, loser_id):
    winner_matches = Player.query.filter_by(id=winner_id).first().matchesPlayed
    loser_matches = Player.query.filter_by(id=loser_id).first().matchesPlayed
    winner_elo = Player.query.filter_by(id=winner_id).first().elo
    loser_elo = Player.query.filter_by(id=loser_id).first().elo

    if winner_elo > 2400:
        winner_k = 16
    elif winner_elo > 2100:
        winner_k = 24
    else:
        winner_k = 32

    if loser_elo > 2400:
        loser_k = 16
    elif loser_elo > 2100:
        loser_k = 24
    else:
        loser_k = 32

    winner_expected_score = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    elo_gained = int(winner_k * (1 - winner_expected_score))
    loser_expected_score = 1 / (1 + 10 ** ((winner_elo - loser_elo) / 400))
    elo_lost = int(loser_k * (0 + loser_expected_score))
    return elo_gained, elo_lost
