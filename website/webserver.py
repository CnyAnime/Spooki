import quart

app = quart.Quart(__name__)


@app.route("/")
async def index():
    return await quart.render_template("index.html")


@app.route("/home")
async def home():
    return await quart.render_template("index.html")


@app.errorhandler(404)
async def error_handler(error):
    if error.code == 404:
        return await quart.render_template("404.html")

    return f"{error.code}: {error.description}"


if __name__ == "__main__":
    app.run()
