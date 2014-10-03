__author__ = 'James Dozier'

import argparse
import configparser
import sqlite3
import random
import twitter
import json


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


def send_to_twitter(s, reply_id):
    """
    Send a sentence to post on Twitter.
    :param s: Sentence to post.
    :return: None
    """

    if reply_id:
        twit.statuses.update(status=s, in_reply_to_status_id=reply_id)
    else:
        twit.statuses.update(status=s)


def respond_to_users():
    """
    Respond to @mentions of Blabber_Bot.
    :return: None
    """

    with open('replied.json', 'r') as replied_file:
        replied = json.load(replied_file)['replied']

    time_line = twit.statuses.mentions_timeline(count=200)

    for tweet in time_line:
        tid = tweet['id']
        if tid in replied:
            continue
        replied.append(tid)

        user = tweet['user']['screen_name']
        s = generate_sentence()
        s = ' '.join(('@%s' % user, s))

        send_to_twitter(s, tid)

    with open('replied.json', 'w') as replied_file:
        json.dump({'replied': replied}, replied_file)

setup_config()
setup_conn()
generate_word_list()

twit = twitter.Twitter(
    auth=twitter.OAuth(
        config['Twitter']['token'],
        config['Twitter']['token_secret'],
        config['Twitter']['consumer'],
        config['Twitter']['consumer_secret']
    )
)

desc = 'A bot that speaks its mind. Which is a bunch of gobbledygook.'
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--speak', help='Speak to the world.', action='store_true')
parser.add_argument('-r', '--reply', help='Reply to the world.', action='store_true')

args = parser.parse_args()

if args.speak:
    send_to_twitter(generate_sentence(), None)

if args.reply:
    respond_to_users()
