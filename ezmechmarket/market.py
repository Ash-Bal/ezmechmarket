import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from ezmechmarket.db import get_db

bp = Blueprint('market', __name__)

# @bp.route('/')
# def index():
#     db = 