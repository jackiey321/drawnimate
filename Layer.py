#################################################
# Layer.py
# Layer class used in modes with drawings
#
# Your name: Jackie Yang     Section: J
# Your andrew id: jaclyny
#
#################################################

from Drawnimate import *

class Layer(object):
    def __init__(self, visible = True):
        self.strokes = []  # stores all brush strokes on layer
        self.visible = visible 