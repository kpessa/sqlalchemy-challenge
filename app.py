from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.automap import automap_base
import sqlalchemy

from flask import Flask, jsonify, render_template
app = Flask(__name__)

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
Session = sessionmaker(bind=engine)
s = Session()


# Routes
@app.route("/")
def index():
  return render_template("index.html")


if __name__ == '__main__':
    app.run()
