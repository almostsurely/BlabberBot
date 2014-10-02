__author__ = 'James Dozier'

import configparser
import sqlite3
import random
import twitter


def setup_config():
    """
    Setups global config to read our configuration file, blabberbot.cfg
    :return: None
    """
    global config

    config = configparser.ConfigParser()
    config.read('blabberbot.cfg')


def setup_conn():
    """
    Established our global Sqlite connection and cursor
    :return: None
    """
    global conn

    conn = sqlite3.connect('WordNet3.1Sqlite.db')

    global cur

    cur = conn.cursor()


def generate_word_list():
    """
    Generates a dictionary of Parts of Speech and a list of words.
    :return:
    """
    global word_list

    word_list = {}

    with open('wordpos.sql') as sql:
        cur.execute(sql.read())

    for item in cur.fetchall():
        pos = item[2]
        word = item[1]
        if pos not in word_list.keys():
            word_list[pos] = []

        word_list[pos].append(word)


def generate_sentence():
    """
    Generate a random sentence.

    n = Noun
    v = Verb
    a = Adjective
    r = Adverb

    :return: String of sentence generated.
    """
    sentence = ['The']

    sentence.append(random.choice(word_list['a']))
    sentence.append(random.choice(word_list['n']))
    sentence.append(random.choice(word_list['v']))
    sentence.append(random.choice(word_list['r']))

    return ' '.join(sentence) + '.'


def send_to_twitter(s):
    """
    Send a sentence to post on Twitter.
    :param s: Sentence to post.
    :return: None
    """

    twit = twitter.Twitter(
        auth=twitter.OAuth(
            config['Twitter']['token'],
            config['Twitter']['token_secret'],
            config['Twitter']['consumer'],
            config['Twitter']['consumer_secret']
        )
    )

    twit.statuses.update(status=s)


setup_config()
setup_conn()
generate_word_list()

send_to_twitter(generate_sentence())