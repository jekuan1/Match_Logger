from website import create_app

app = create_app()

# gunicorn -b 0.0.0.0:8000 -w 4 app:app
# $ nginx

# TODO host on github pages? or similar
# TODO scrolling leaderboard
# TODO add font awesome offline
# TODO add admin controls
# TODO add player info
# TODO add dark mode
# TODO refresh page every 5 mins
# TODO create a revamp system so I can export match history and then fuck aroudn with different models in the databse

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
