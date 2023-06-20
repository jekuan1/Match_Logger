from . import db

# stores players and elo
# also need to store history of player matches


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True))
    loser_id = db.Column(db.Integer, db.ForeignKey("player.id"))
    winner_id = db.Column(db.Integer, db.ForeignKey("player.id"))
    loser = db.Column(db.String(150))
    winner = db.Column(db.String(150))
    # rating gained by winner
    gain = db.Column(db.Integer)
    # rating lost by loser
    loss = db.Column(db.Integer)


# stores players and their elo
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String(150), unique=True)
    elo = db.Column(db.Integer)
    matchesPlayed = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    dateCreated = db.Column(db.DateTime(timezone=True))
