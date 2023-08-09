"""Represent models for near-Earth objects and their close approaches."""
import random
import os
import requests
from PIL import Image
from flask import Flask, render_template, abort, request

from model import MemeEngine, Ingestor, MemeGenerator

app = Flask(__name__)

meme = MemeEngine("./static")


def setup():
    """_summary_.

    Returns:
        _type_: _description_.
    """
    """Load all resources"""

    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]

    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    images = "./_data/photos/dog/"
    imgs = []
    for root, dirs, files in os.walk(images):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """_summary_.

    Returns:
        _type_: _description_.
    """
    """Generate a random meme"""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    print(quote)
    print(f"image path: {img}")

    try:
        path = f"{meme.folder}/{random.random()}.jpg"
        mew = MemeGenerator(Image.open(img), path)
        newImg = mew.insertText(quote)
        mew.saveImage(newImg)
        return render_template("meme.html", path=path)
    except requests.exceptions.ConnectionError:
        errorPath = "./static/error.png"
        return render_template("error.html", path=errorPath)


@app.route("/create", methods=["GET"])
def meme_form():
    """_summary_.

    Returns:
        _type_: _description_.
    """
    """User input for meme information"""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """_summary_.

    Returns:
        _type_: _description_.
    """
    """Create a user defined meme"""
    try:
        image_url = request.form.get("image_url")
        body = request.form.get("body")
        author = request.form.get("author")
        im = Image.open(requests.get(image_url, stream=True).raw)
        tmpPath = f"{meme.folder}/tmp.jpg"
        im.save(tmpPath, "JPEG", quality=80, optimize=True, progressive=True)

        path = meme.make_meme(tmpPath, body, author)

        return render_template("meme.html", path=path)
    except requests.exceptions.ConnectionError:
        errorPath = "./static/error.png"
        return render_template("error.html", path=errorPath)


if __name__ == "__main__":
    app.run()
