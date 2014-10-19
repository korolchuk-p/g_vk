
from flask import render_template, redirect
from app import app

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/static/images/404error.png")


@app.errorhandler(403)
def page_not_found(e):
    return redirect("/static/images/403error.png")
