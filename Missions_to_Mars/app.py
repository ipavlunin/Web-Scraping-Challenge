# Impoert Libraries
from flask import Flask, render_template, redirect
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
# Create database
db = client.mars_db
# Clear database if that exists
client.mars_db.mission.drop()

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mission = client.mars_db.mission.find_one()

    # Return template and data
    return render_template("index.html", mission = mission)
    
    
    
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    # Create collection
    mission = client.mars_db.mission
    # Run the scrape function
    mars_web_dict = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mission.update({}, mars_web_dict, upsert=True)

    # Redirect back to home page (returns code 302)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)