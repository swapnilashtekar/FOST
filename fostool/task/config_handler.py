# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# coding:utf-8
from __future__ import absolute_import, division, print_function

import yaml
import os
from addict import Dict
import logging
logger = logging.getLogger('ConfigHandler')
logger.setLevel(logging.INFO)

class YamlHandler:
    """handle yaml file
    """
    def __init__(self, file_path):
        """ YamlHandler init

        Parameters
        ----------
        file_path : String
            yaml file path of config
        """
        if not os.path.exists(file_path):
            return FileExistsError(OSError)
        self.file_path = file_path
        logger.info('yaml handler load path: {}'.format(self.file_path))

    def read_yaml(self, encoding='utf-8'):
        """ read yaml file and convert to easydict

        Parameters
        ----------
        encoding : String
            encoding method uses utf-8 by default

        Returns
        -------
        Dict(addict)
            The usage of Dict is the same as dict
        """
        with open(self.file_path, encoding=encoding) as f:
            return Dict(yaml.load(f.read(), Loader=yaml.FullLoader))

    def write_yaml(self, data, encoding='utf-8'):
        """ write dict or easydict to yaml file(auto write to self.file_path)

        Parameters
        ----------
        data : 'dict' or 'Dict(addict)'
            dict containing the contents of the yaml file
        """
        with open(self.file_path, encoding=encoding, mode='w') as f:
            return yaml.dump(addict2dict(data) if isinstance(data, Dict) else data, stream=f, allow_unicode=True)

def addict2dict(addict_obj):
    '''convert addict to dict

    Parameters
    ----------
    addict_obj : Dict
        the addict obj that you want to convert to dict

    Returns
    -------
    dict
        convert result
    '''
    dict_obj = {}
    for key, vals in addict_obj.items():
        dict_obj[key] = addict2dict(vals) if isinstance(vals, Dict) else vals
    return dict_obj
