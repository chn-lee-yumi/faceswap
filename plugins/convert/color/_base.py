#!/usr/bin/env python3
""" Parent class for color Adjustments for faceswap.py converter """

import logging
import numpy as np

from plugins.convert._config import Config

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def get_config(plugin_name):
    """ Return the config for the requested model """
    return Config(plugin_name).config_dict


class Adjustment():
    """ Parent class for adjustments """
    def __init__(self):
        logger.debug("Initializing %s", self.__class__.__name__)
        self.config = get_config(".".join(self.__module__.split(".")[-2:]))
        logger.debug("config: %s", self.config)
        logger.debug("Initialized %s", self.__class__.__name__)

    def process(self, old_face, new_face, raw_mask):
        """ Override for specific color adjustment process """
        raise NotImplementedError

    def run(self, old_face, new_face, raw_mask):
        """ Perform selected adjustment on face """
        logger.trace("Performing color adjustment")
        # Remove Mask for processing
        reinsert_mask = False
        if new_face.shape[2] == 4:
            reinsert_mask = True
            final_mask = new_face[:, :, -1]
            new_face = new_face[:, :, :3]
        new_face = self.process(old_face, new_face, raw_mask)
        new_face = np.clip(new_face, 0.0, 1.0)
        if reinsert_mask and new_face.shape[2] != 4:
            # Reinsert Mask
            new_face = np.concatenate((new_face, np.expand_dims(final_mask, axis=-1)), -1)
        logger.trace("Performed color adjustment")
        return new_face
