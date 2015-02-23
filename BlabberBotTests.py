__author__ = 'James Dozier'

import unittest
import os
import configparser
import twitter
import urllib
import urllib.request
import py2neo


class BlabberBotTests(unittest.TestCase):
    """
    Tests for BlabberBot.
    """

    def test_connections(self):
        """
        Test necessary connections in BlabberBot.
        Connections to:
        Twitter API
        GraphStory
        Merriam Webster API
        :return:
        """

        # Test that our config file exists.
        self.assertTrue(os.path.isfile(r'./blabberbot.cfg'))

        config = configparser.ConfigParser()
        config.read(r'./blabberbot.cfg')

        # Test that necessary headers exist.
        self.assertIn('Twitter', config.keys())
        self.assertIn('Neo4j', config.keys())
        self.assertIn('Dictionary', config.keys())

        # Test that necessary values under headers exist.
        # Twitter
        self.assertIn('token', config['Twitter'])
        self.assertIn('token_secret', config['Twitter'])
        self.assertIn('consumer', config['Twitter'])
        self.assertIn('consumer_secret', config['Twitter'])

        # Neo4j
        self.assertIn('user', config['Neo4j'])
        self.assertIn('password', config['Neo4j'])
        self.assertIn('host', config['Neo4j'])

        # Dictionary
        self.assertIn('dict_key', config['Dictionary'])
        self.assertIn('thes_key', config['Dictionary'])

        #Test Twitter Connection
        auth = twitter.OAuth(
            config['Twitter']['token'],
            config['Twitter']['token_secret'],
            config['Twitter']['consumer'],
            config['Twitter']['consumer_secret']
        )
        twit = twitter.Twitter(auth=auth)

        self.assertIsInstance(twit, twitter.Twitter)

        try:
            us_woe_id = 23424977
            _ = twit.trends.place(_id=us_woe_id)
        except Exception as e:
            self.fail(e)

        # Test GraphStory Connection
        uri = 'https://{user}:{password}@{host}/db/data'.format(**config['Neo4j'])
        graph_db = py2neo.Graph(uri)

        try:
            _ = graph_db.node_labels
        except Exception as e:
            self.fail(e)

        # Test Merriam Webster Connection
        url = 'http://www.dictionaryapi.com/api/v1/references/{product}/xml/test?key={key}'

        resp = urllib.request.urlopen(url.format(
            product='collegiate', key=config['Dictionary']['dict_key']
        )).read()

        self.assertNotEqual(resp, b'Invalid API key or reference name provided.')

        resp = urllib.request.urlopen(url.format(
            product='thesaurus', key=config['Dictionary']['thes_key']
        )).read()

        self.assertNotEqual(resp, b'Invalid API key or reference name provided.')