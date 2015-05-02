from datetime import datetime
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall


def my_pygame_loop_interior():
	print "hi"


lc = LoopingCall(my_pygame_loop_interior)
lc.start(1)
reactor.run()
