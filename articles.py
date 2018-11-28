import json
import os
from uuid import uuid1

ARTICLES_DIR_PATH = "articles/"


def save_article(userid, header, signature, body):
    """
    Creates new article using given parameters and saves it with unique ID
    """
    article_info = {
        "userid": userid,
        "header": header,
        "signature": signature,
        "body": body,
    }
    article_id = uuid1().hex
    article_filepath = os.path.join(
        ARTICLES_DIR_PATH, "{}.json".format(article_id)
    )
    if not os.path.exists(ARTICLES_DIR_PATH):
        os.mkdir(ARTICLES_DIR_PATH)
    with open(article_filepath, "tw") as article_file:
        json.dump(article_info, article_file)

    return article_id


def load_article(article_id):
    article_filepath = os.path.join(
        ARTICLES_DIR_PATH, "{}.json".format(article_id)
    )
    if not os.path.exists(article_filepath):
        return None

    with open(article_filepath) as article_file:
        article = json.load(article_file)
        article["id"] = article_id
        return article


def update_article(article_id, header=None, signature=None, body=None):
    """
    Updates article information using given parameters
    """
    article = load_article(article_id)
    if article is None:
        return False

    if header is not None:
        article["header"] = header
    if signature is not None:
        article["signature"] = signature
    if body is not None:
        article["body"] = body

    article_filepath = os.path.join(
        ARTICLES_DIR_PATH, "{}.json".format(article_id)
    )
    with open(article_filepath, "tw") as article_file:
        json.dump(article, article_file)

    return True


def load_all_articles():
    if not os.path.exists(ARTICLES_DIR_PATH):
        return []
        
    articles = [
        load_article(os.path.splitext(entry.name)[0])
        for entry in os.scandir(ARTICLES_DIR_PATH)
        if entry.is_file()
    ]
    return articles
