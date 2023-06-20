from flask import Blueprint, render_template, request, flash, redirect, url_for
import datetime as dt

from .models import Player, Match
from .elo_calculator import EloCalc
from . import db

DEFAULTELO = 1000

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return redirect(url_for("views.leaderboards"))


@views.route("/leaderboards")
def leaderboards():
    players = Player.query.order_by(Player.elo.desc(), Player.playerName)
    return render_template("leaderboards.html", players=players)


@views.route("/add-player", methods=["GET", "POST"])
def add_player():
    if request.method == "POST":
        player = request.form.get("player")
        player = player.title()

        if len(player) < 1:
            flash("Player name too short!", category="error")
        elif Player.query.filter_by(playerName=player).first():
            flash("Player already exists", category="error")
        else:
            new_player = Player(
                playerName=player, elo=DEFAULTELO, wins=0, losses=0, matchesPlayed=0
            )
            db.session.add(new_player)
            db.session.commit()
            flash("Player Added!", category="success")
            return redirect(url_for("views.add_player"))

    return render_template("add_player.html")


@views.route("/add-match", methods=["GET", "POST"])
def add_match():
    if request.method == "POST":
        winner = request.form.get("winner")
        loser = request.form.get("loser")
        winner = winner.title()
        loser = loser.title()

        if len(loser) == 0 or len(winner) == 0:
            flash("Did not input a name.", category="error")
        elif loser == winner:
            flash("You cannot play against yourself", category="error")
        # TODO tell me which player could not be found
        elif (
            Player.query.filter_by(playerName=winner).first()
            and Player.query.filter_by(playerName=loser).first()
        ):
            winner_id = Player.query.filter_by(playerName=winner).first().id
            loser_id = Player.query.filter_by(playerName=loser).first().id
            gain, loss = EloCalc(winner_id=winner_id, loser_id=loser_id)
            new_match = Match(
                winner_id=winner_id,
                loser_id=loser_id,
                gain=gain,
                loss=loss,
                winner=winner,
                loser=loser,
                date=dt.datetime.now(),
            )
            Player.query.filter_by(playerName=winner).first().elo += gain
            Player.query.filter_by(playerName=loser).first().elo -= loss
            Player.query.filter_by(playerName=winner).first().matchesPlayed += 1
            Player.query.filter_by(playerName=winner).first().wins += 1
            Player.query.filter_by(playerName=loser).first().matchesPlayed += 1
            Player.query.filter_by(playerName=loser).first().losses += 1
            db.session.add(new_match)
            db.session.commit()
            flash("Match successfully added")
            return redirect(url_for("views.add_match"))
        else:
            flash("Could not find player(s).", category="error")
    players = Player.query.order_by(Player.playerName)
    names = []
    for player in players:
        names.append(player.playerName)
    return render_template("add_match.html", names=names)


@views.route("/match-history")
def match_history():
    matches = Match.query.order_by(Match.id.desc())
    return render_template("match_history.html", matches=matches, Player=Player)


@views.route("/admin", methods=["GET", "POST"])
def admin():
    players = Player.query.order_by(Player.id)

    if request.method == "POST":
        player = request.form.get("player")
        rating = request.form.get("rating")
        player = player.title()
        rating = rating.title()
        # TODO check why this change rating functionality not working
        if Player.query.filter_by(playerName=player).first():
            Player.query.filter_by(playerName=player).first().elo = rating
            db.session.commit()
            flash("Rating successfully changed")
            return redirect(url_for("views.admin"))
        else:
            flash("Could not find player.", category="error")

    return render_template("admin.html", players=players)


@views.route("/player_delete/<pid>", methods=["GET"])
def player_delete(pid):
    Player.query.filter_by(id=pid).delete()
    db.session.commit()
    flash("Player successfully deleted", category="success")
    return redirect(url_for("views.admin"))


@views.route("/version-history")
def version_history():
    f = open("website/version_history.txt", "r")
    return render_template("version_history.html", vh=f.read())
