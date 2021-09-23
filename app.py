from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, widgets, SubmitField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "887df81729beb44741c633ca2d802432"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///anime.db"

db = SQLAlchemy(app)

genres = []

with open("genres.txt", "r") as file:
    data = file.readlines()
    for x in data:
        x = x[:-1]
        genres.append(x.strip())
    
class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mal_id = db.Column(db.Integer)
    score = db.Column(db.String)
    tags = db.Column(db.String)
    sypnopsis = db.Column(db.String)
    popularity = db.Column(db.Integer)

class MultiCheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class TasteForm(FlaskForm):
    tag = MultiCheckBoxField(label="Select Tags", choices=[(x, x) for x in genres])
    submit = SubmitField(label="Generate")

def get_best_animes(animes, output):
    for x in range(0, 5):
        best_anime = animes[0]
        for anime in animes:
            if best_anime.popularity > anime.popularity:
                best_anime = anime
                animes.remove(anime)
        output.append(best_anime)


@app.route("/", methods=["GET", "POST"])
def home_page():
    best_recommendations = []
    form = TasteForm()
    recommendations = []

    if form.validate_on_submit():
        taste = form.tag.data
        all_animes = Anime.query.all()

        for anime in all_animes:
            genres = anime.tags.split(", ")
            for x in taste:
                if x in genres:
                    recommendations.append(anime)
                elif anime in recommendations:
                    recommendations.remove(anime)
                else:
                    continue

        best_recommendations = []
        if len(recommendations) <= 5:
            best_recommendations = recommendations

        if recommendations:
            get_best_animes(recommendations, best_recommendations)

        for x in best_recommendations:  
            print(x.name)
            print(x.popularity)
            print(x.tags)
            print(taste)

        else:
            print(None) 
        
        
        best_recommendations = list(set(best_recommendations))
    
    return render_template("home.html", recommendations=best_recommendations, form=form)

if __name__ == "__main__":
    app.run(debug=True)