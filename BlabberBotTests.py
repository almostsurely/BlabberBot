__author__ = 'James Dozier'

import unittest
import os
import configparser


class BlabberBotTests(unittest.TestCase):
    """
    Tests for BlabberBot.
    """

    def test_connections(self):
        """
        Test necessary connections in BlabberBot.
        :return:
        """

        #Test that our config file exists.
        self.assertTrue(os.path.isfile(r'./blabberbot.cfg'))

        config = configparser.ConfigParser()
        config.read(r'./blabberbot.cfg')

        #Test that necessary headers exist.
        self.assertTrue('Twitter' in config.keys())
        self.assertTrue('Neo4j' in config.keys())
        self.assertTrue('Dictionary' in config.keys())