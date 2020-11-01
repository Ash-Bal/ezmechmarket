import functools
import praw
from ezmechmarket.db import get_db
from ezmechmarket.imgurinit import init_Imgur
from imgurpython import ImgurClient
import re
import requests
import os

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort



bp = Blueprint('market', __name__)

# initialize reddit class with ezmechmarket script(praw.ini)
print(os.getcwdb())
reddit = praw.Reddit("ezmechmarket")

# initialize imgur class
# imgurClient = 'd21478951409e78'
# imgurSecret = '378ebb7884ddeed5c0893aba349decb46af17224'
imgur = ImgurClient(init_Imgur()[0], init_Imgur()[1])



def get_posts(mechmarket):
    db = get_db()
    for submission in mechmarket:
        if db.execute(
            'select id from posts where title = ?', (submission.title,)
        ).fetchone() is None:
            db.execute(
                'insert into posts (title, url, body, created)'
                ' values (?, ?, ?, ?)',
                (submission.title, submission.url, submission.selftext, submission.created_utc)
            )
    db.commit()

def get_album_url(mechmarket):
    db = get_db()
    get_album_regex = "(https|http)://(i.|)imgur.com/(a/([a-zA-Z0-9]*)|gallery/([a-zA-Z0-9]*)|([a-zA-Z0-9]*).jpg|([a-zA-Z0-9]*))" 
    add_jpg_regex = "(https|http)://(i.|)imgur.com/([a-zA-Z0-9]*$)"
    jpg_regex = ".jpg$"
    for submission in mechmarket:
        # print("GET THE ALBUMS PLS")
        album_url = re.search(get_album_regex, submission.selftext)
        # print(album_url.group(0))
        if (album_url and re.search(add_jpg_regex, album_url.group(0))):
            url = album_url.group(0) + ".jpg"
            if db.execute(
                'select id from images where image_url = ?', (url,)
            ).fetchone() is None:
                db.execute(
                    'insert into images (title, image_url)'
                    ' values (?, ?)',
                    (submission.title, url)
                )
        elif (album_url and re.search(jpg_regex, album_url.group(0))):
            url = album_url.group(0)
            # print(url)
            if db.execute(
                'select id from images where image_url = ?', (url,)
            ).fetchone() is None:
                db.execute(
                    'insert into images (title, image_url)'
                    ' values (?, ?)',
                    (submission.title, url)
                )
        elif (album_url):
            url = album_url.group(0)
            # print(url)
            db.execute(
                'insert into album (title, album_url)'
                ' values (?, ?)',
                (submission.title, url)
            )
    db.commit()

def get_image_url(mechmarket):
    db = get_db()
    code_regex = "[a-zA-Z0-9]*.$"
    for submission in mechmarket:
        album_link = db.execute(
            'select album_url from album where title = ?',
            (submission.title,)
        ).fetchone()
        if (album_link):
            # print(album_link[0])
            album = re.search(code_regex, album_link[0])
            # print("checking")
            # check = imgur.get_album("QoKSKYp")
            # print(check)
            # print("Getting link...")
            # link = requests.head(imgur.get_album(album.group(0)))
            # print("Your link is: ")
            # print(album_link[0])
            try:
                imgur.get_album(album.group(0))
            except:
                continue
            # if (link.status_code == 200):
            unwrapped = imgur.get_album_images(album.group(0))
            #     print(album.group(0))
            # else:
            #     print(link.status_code, print(album.group(0)))
            #     continue
            for i in range(len(unwrapped)):
                if db.execute(
                    'select id from images where image_url = ?', (unwrapped[i].link,)
                ).fetchone() is None:
                    db.execute(
                        'insert into images (title, image_url)'
                        ' values (?, ?)',
                        (submission.title, unwrapped[i].link)
                    )
        else:
            continue
    db.commit()

@bp.route('/')
def index():
    db = get_db()
    mechmarket = reddit.subreddit("mechmarket").search('flair_name:"Selling"', sort='new', limit=10)
    get_posts(mechmarket)
    mechmarket = reddit.subreddit("mechmarket").search('flair_name:"Selling"', sort='new', limit=10)
    get_album_url(mechmarket)
    mechmarket = reddit.subreddit("mechmarket").search('flair_name:"Selling"', sort='new', limit=10)
    get_image_url(mechmarket)
    db.execute(
        'update images set image_url = replace(image_url, ".jpg",".png") where image_url like "%.jpg";'
    )

    titles = db.execute(
        'select distinct(i.title), p.url from images i join posts p on i.title = p.title order by p.created desc'
    ).fetchall()

    post_count = db.execute(
        'select count(title) from posts'
    ).fetchone()
    album_title = []
    album_images = []
    album_url = []
    for post in range(len(titles)):
        album_title.append(titles[post][0])
        album_url.append(titles[post][1])
        album_images.append(
            db.execute(
                'select distinct(i.image_url) from images i join posts p on i.title = p.title where p.title = ? order by p.created desc',
                (titles[post][0], )
            ).fetchall()
        )
    print(post_count[0])
    print(len(album_url))
    print(album_images[0])
    
    return render_template('index.html', titles = album_title, urls = album_url, images = album_images)
