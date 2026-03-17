import urllib.request
import os

os.makedirs("static/posters", exist_ok=True)

posters = {
    "dune.jpg":         "https://m.media-amazon.com/images/M/MV5BN2QyZGU4ZDctOWMzMy00NTc5LThlOGQtODhmNDI1NmY5YzAwXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_FMjpg_UX800_.jpg",
    "oppenheimer.jpg":  "https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjUtN2M1MS00MTQ2LTk2ODgtNzc2M2QyZGE5NTVjXkEyXkFqcGdeQXVyNzAwMjU2MTY@._V1_FMjpg_UX800_.jpg",
    "inception.jpg":    "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_FMjpg_UX800_.jpg",
    "interstellar.jpg": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX800_.jpg",
    "insideout2.jpg":   "https://m.media-amazon.com/images/M/MV5BYmU1ZGYzZGQtZjIxNS00ZmZlLWJhNTMtZTE4ZmZiMzNmMzZhXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_FMjpg_UX800_.jpg",
    "darkknight.jpg":   "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_FMjpg_UX800_.jpg",
    "endgame.jpg":      "https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_FMjpg_UX800_.jpg",
    "godfather.jpg":    "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX800_.jpg",
    "joker.jpg":        "https://m.media-amazon.com/images/M/MV5BNGVjNWI4ZGUtNzE0MS00YTJmLWE0ZDctN2ZiYTk2YmI3NTYyXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_FMjpg_UX800_.jpg",
    "spiderman.jpg":    "https://m.media-amazon.com/images/M/MV5BZWMyYzFjYTYtNTRjYi00OGExLWE2YzgtOGRmYjAxZTU3NzAyXkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_FMjpg_UX800_.jpg",
    "lionking.jpg":     "https://m.media-amazon.com/images/M/MV5BMjIwMjE1Nzc4NV5BMl5BanBnXkFtZTgwNDg4OTA1NzM@._V1_FMjpg_UX800_.jpg",
    "topgun.jpg":       "https://m.media-amazon.com/images/M/MV5BZWYzOGEwNUs2OGpkFC00NjA5LTk2ZTItOGRlMGE3YzI2OWM2XkEyXkFqcGdeQXVyMjkwOTAyMDU@._V1_FMjpg_UX800_.jpg",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print("Downloading posters...")
for filename, url in posters.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(f"static/posters/{filename}", 'wb') as f:
                f.write(response.read())
        print(f"✅ {filename}")
    except Exception as e:
        print(f"❌ {filename} — {e}")

print("\nDone! Ab cinebook command chalao.")
