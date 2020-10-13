import praw
from imgurpython import ImgurClient
import re
# from flask import Flask

# initialize reddit class with ezmechmarket script
reddit = praw.Reddit("ezmechmarket")

imgurClient = 'd21478951409e78'
imgurSecret = 'a7724f093cdff224c45e5f990055c6e93ac1b69d'
imgur = ImgurClient(imgurClient, imgurSecret)

# get all new posts with a "Selling" flair
mechmarket = reddit.subreddit("mechmarket").search('flair_name:"Selling"', sort='new', limit=50)

def link_scraper(submission_text):
    regex = "(https|http)://(i.|)imgur.com/(a|gallery|((?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{,7})|((?=.*?[A-Z])(?=.*?[a-z]).{0,7}))/(.jpg|((?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{,7})|((?=.*?[A-Z])(?=.*?[a-z]).{0,7}))" 
    images = re.search(regex, submission_text)
    if(images):
        return images.group(0)
    else:
        return None

def unwrap_images(album_link):
    regex = "(((?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{,7})|((?=.*?[A-Z])(?=.*?[a-z]).{0,7}))$"
    album = re.search(regex, album_link)
    unwrapped = imgur.get_album_images(album.group(0))
    image_path = []
    for i in range(len(unwrapped)):
        image_path.append(unwrapped[i].link)
    return image_path

def main():
    # containers for parts of each post we need to store
    post_titles = [] # holds post titles
    post_text = [] # holds post text
    post_url = [] # holds url to reddit post
    album_links = [] # holds url to imgur post
    image_links = [] # holds urls to each image in an imgur post
    
    # populate post containers
    for submission in mechmarket:
        post_titles.append(submission.title)
        post_text.append(submission.selftext)
        post_url.append(submission.url)
    
    # scrape imgur link from post
    # populates album_link
    for post in range(len(post_titles)):
        album_links.append(link_scraper(post_text[post]))
    
    #populate image_link
    for post in range(len(album_links)):
        if(album_links[post] is not None):
            #print(album_links[post])
            image_links.append(unwrap_images(album_links[post]))
        else:
            #print(album_links[post])
            image_links.append(None)
    
    print(post_titles[0])
    print(post_url[0])
    print(image_links[0])

main()    




