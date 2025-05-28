from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import requests

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# Homepage shows top listings
@app.route("/")
def home():
    URL_source = "https://mlb25.theshow.com/apis/listings.json"
    response = requests.get(URL_source)
    data = response.json()["listings"]
    page = int(request.args.get("page", 1))
    if page > 1:
        url_source = f"https://mlb25.theshow.com/apis/listings.json?page={page}"
        response = requests.get(url_source)
        data = response.json()["listings"]
        return  render_template('home.html', players=data, page=page)

    return render_template("home.html", players=data, page=page)

# List individual player
@app.route("/listing/<player_id>")
def listing(player_id):
    player_data_url = f'https://mlb25.theshow.com/apis/item.json?uuid={player_id}'
    market_data_url = f'https://mlb25.theshow.com/apis/listing.json?uuid={player_id}'

    if player_id:
        player_response = requests.get(player_data_url)
        market_response = requests.get(market_data_url)
        player_data = player_response.json()
        market_data = market_response.json()
        market_history = market_data.get("price_history", [])

    return render_template("listing.html", player=player_data, market=market_data, history=market_history)

# Search for player
@app.route("/search", methods=["GET", "POST"])
def search_player():
    players = []
    if request.method == "GET":
        search_term = request.args.get("search")
        search_url = f'https://mlb25.theshow.com/apis/listings.json?name={search_term}'
        response = requests.get(search_url)
        data = response.json()["listings"]

        for listing in data:
            player = {
                "player_id": listing["item"]["uuid"],
                "player_name": listing["listing_name"],
                "team": listing["item"]["team"],
                "position": listing["item"]["display_position"],
            }
            players.append(player)

    return render_template("search.html", players=players)

if __name__ == '__main__':
    app.run(debug=True)
