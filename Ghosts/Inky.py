import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Path import navigate
from Ghosts.Ghost import Ghost

class Inky(Ghost):
	pass
	# def __init__(self):
	# 	Ghost.__init__(self)

	# def decideMove():
	# 	pass

if __name__=="__main__":
	i=Inky()
	print(i.getPosition())