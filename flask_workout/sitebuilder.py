import sys

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True

# Conf FlatPages
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'exercises'

# Init Freezer
FREEZER_BASE_URL = '/exercises'

# Init Flask
app = Flask(__name__)
app.config.from_object(__name__)
exercises = FlatPages(app)
freezer = Freezer(app)
available_tags = []

for recipe in exercises:
    tags = recipe.meta.get('tags', [])
    if tags:
        available_tags = available_tags + tags
available_tags = list(set(available_tags))

@app.route('/')
def index():
    return render_template('index.html', all_exercises=exercises, all_tags=available_tags, exercises=exercises)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [r for r in exercises if tag in r.meta.get('tags', [])]
    return render_template('tag.html', all_exercises=exercises, all_tags=available_tags, exercises=tagged, tag=tag)

@app.route('/exercises/<path:path>/')
def exercise(path):
    data = exercises.get_or_404(path)
    return render_template('exercise.html', all_exercises=exercises, all_tags=available_tags, exercise=data)

@app.route('/workouts/<path:path>/')
def workout(path):
    data = workouts.get_or_404(path)
    return render_template('workout.html', all_exercises=exercises, all_tags=available_tags, workout=data)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)