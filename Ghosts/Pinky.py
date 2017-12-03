import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Path import navigate
from Ghosts.Ghost import Ghost

class Pinky(Ghost):

	def __init__(self):
		Ghost.__init__(self)

	def decideMove():
		pass