# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

home = Blueprint('home', __name__, url_prefix='')


@home.route('/')
def home_page():
    return render_template('index.html')
