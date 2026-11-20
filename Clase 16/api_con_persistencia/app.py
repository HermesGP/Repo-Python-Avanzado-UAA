from flask import Flask
from routes.routes import routes
from database.config import Base, engine

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    app.run(debug=True)