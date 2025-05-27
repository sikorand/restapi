
from library import create_app

app = create_app()

@app.route("/")
def hello():
    return "API is working!"

if __name__ == '__main__':
    app.run(debug=True)
