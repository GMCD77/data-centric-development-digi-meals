import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'digi_meals'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

base_url="https://8080-dfc71269-2884-4135-a69f-b94bfa184173.ws-eu0.gitpod.io"
def _redirect(path):
    return redirect (base_url + path)

@app.route('/')
def get_recipes():
    return render_template("home.html", recipes=mongo.db.recipe.find(), utensils=mongo.db.utensils.find())

@app.route('/test')
def test():
   return _redirect("/")
#    return redirect(url_for('/'))

@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html", categories=mongo.db.categories.find())

@app.route('/utensils')
def get_utensils():
    return render_template("utensils.html", recipes=mongo.db.recipe.find(), utensils=mongo.db.utensils.find())

@app.route('/recipecard')
def recipecard():
    utensils=mongo.db.utensils.find()
    return render_template("recipecard.html", utensils=utensils)

@app.route('/add_utensils')
def add_utensils():
    return render_template("addutensils.html", categories=mongo.db.categories.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipe = mongo.db.recipe
    recipe.insert_one(request.form.to_dict())
    return _redirect('/')

@app.route('/insert_utensils', methods=['POST'])
def insert_utensils():
    utensils = mongo.db.utensils
    utensils.insert_one(request.form.to_dict())
    return redirect(url_for('/utensils'))

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe, categories=all_categories)

@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    the_recipe =  mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('recipecard.html', recipe=the_recipe, categories=all_categories)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipe = mongo.db.recipe
    recipe.update( {"_id": ObjectId(recipe_id)},
    {
        'recipe_name': request.form.get('recipe_name'),
        'image_link':request.form.get('image_link'),
        'cuisine' : request.form.get('cuisine'),
        'serves' : request.form.get('serves'),
        'preparation_time' : request.form.get('preparation_time'),
        'cooking_time' : request.form.get('cooking_time'),
        'description' : request.form.get('description'),
        'ingredients' : request.form.get('ingredients'),
        'instructions' : request.form.get('instructions')
    })
    return redirect(url_for(''))

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipe.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '127.0.0.1'),
            port=int(os.environ.get('PORT', '8080')),
            debug=True)