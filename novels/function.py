#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import os
import random

from novels.config import Config


"""
    Get a random user agent string.
    :return: Random user agent string.
"""
def get_random_user_agent():
    return random.choice(_get_data('user_agents.txt', Config.USER_AGENT))


def _get_data(filename, default=''):
    """
        Get data from a file
        :param filename: filename
        :param default: default value
        :return: data
        """
    root_folder = os.path.dirname(os.path.dirname(__file__))
    user_agents_file = os.path.join(
        os.path.join(root_folder, 'data'), filename)
    try:
            with open(user_agents_file, mode='r') as f:
                data = [_.strip() for _ in f.readlines()]
    except:
        data = [default]
    return data

if __name__ == '__main__':
    print(get_random_user_agent())