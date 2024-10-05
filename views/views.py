from flask import Flask, render_template, request, redirect, url_for, flash

from app import *
from models.utils import *


@app.route('/')
def home():
    return render_template('home.html')
