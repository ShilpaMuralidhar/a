import os

import pandas as pd
import numpy as np
from scipy import stats

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
# import VaxRegression

app = Flask(__name__)


#################################################
# Database Setup
#################################################

postgresURI = "postgres://trszpzmvozxxfa:4837915234eabffbb990eda4721662850ebcf9e07fc119c3fe994db385f04f6f@ec2-54-83-33-14.compute-1.amazonaws.com:5432/dcnno5op1g262"

app.config["SQLALCHEMY_DATABASE_URI"] = postgresURI
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table #
Vaccines = Base.classes.wuenic
Life = Base.classes.infexpmort

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("indexTrend.html")


@app.route("/vaccine_names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Vaccines).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    vaccines = df["Vaccine"].unique()
    # Return a list of the vaccine names
    return jsonify(list(vaccines))

@app.route("/vaxdata/<vaccine>")
def vaccine_vaxdata(vaccine):
    """Return the MetaData for a given vaccine."""
    print(vaccine)
    # print(country)
    selVax = [
        Vaccines.Vaccine,
        Vaccines.Country,
        Vaccines.Year,
        Vaccines.Coverage
    ]

    resultsVax = db.session.query(*selVax).filter(Vaccines.Vaccine == vaccine).filter(Vaccines.Year == 2017).all()
    
    # print(results)

    # Create alist of dictionaries for each row of metadata information
    vaxItems = []
    
    for result in resultsVax:
        vaccine_metadata = {}
        vaccine_metadata["Vaccine"] = result[0]
        vaccine_metadata["Country"] = result[1]
        vaccine_metadata["Year"] = result[2]
        vaccine_metadata["Coverage"] = result[3]
        vaxItems.append(vaccine_metadata)

    return jsonify(vaxItems)


if __name__ == "__main__":
    #when you upload to heroku, take out debug
    app.run(debug = True, port = 5044)
    # app.run()
