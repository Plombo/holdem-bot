#
# Copyright (C) 2006 - 2010 Loic Dachary <loic@dachary.org>
# Copyright (C) 2004, 2005, 2006 Mekensleep
#
# Mekensleep
# 26 rue des rosiers
# 75004 Paris
#       licensing@mekensleep.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Authors:
#  Loic Dachary <loic@dachary.org>
#

#
# poker-engine
#

import sys, os
sys.path.insert(0, "..")

from pokerengine.pokergame import PokerGameServer

#
# Instantiate a poker engine for a hold'em game with a 10/15 pot limit
# betting structure. The variant and betting structure descriptions
# will be read from the conf/poker.holdem.xml and conf/poker.10-15-pot-limit.xml
# files.
#
game = PokerGameServer("poker.%s.xml", ['conf', '../conf', '/etc/poker-engine'])
game.verbose = 1
game.setVariant("holdem")
game.setBettingStructure("10-15-pot-limit")

#
# The serial numbers of the four players
#
PLAYER1 = 1
PLAYER2 = 2
PLAYER3 = 3
PLAYER4 = 4

#
# Each player sits at the table and buys in 1500.
# The blinds are posted automatically, no action is required from
# the player.
#
for serial in xrange(PLAYER1, PLAYER4 + 1):
    game.addPlayer(serial)
    game.payBuyIn(serial, 1500*100)
    game.sit(serial)
    game.autoBlindAnte(serial)

#
# Post the blinds and deal the pocket cards. PLAYER1
# is the dealer, PLAYER2 pays the small blind, PLAYER3
# pays the big blind.
#
game.beginTurn(1)
#game.botPlayer(PLAYER1)
game.botPlayer(PLAYER2)
game.botPlayer(PLAYER3)
game.botPlayer(PLAYER4)

import random
while game.possibleActions(PLAYER1):
	actions = game.possibleActions(PLAYER1)
	assert len(actions)
	rnd = random.randint(0, len(actions)-1)
	action = actions[rnd]
	if action == 'fold':
		game.fold(PLAYER1)
	elif action == 'check':
		game.check(PLAYER1)
	elif action == 'call':
		game.call(PLAYER1)
	elif action == 'raise':
		game.callNraise(PLAYER1, 0)
	else:
		raise Exception('unknown action' + action)

'''
#
# PLAYER4 calls under the gun
#
game.call(PLAYER4)
#
# The dealer and small blind fold
#
game.fold(PLAYER1)
game.fold(PLAYER2)
#
# The big blind checks
#
game.check(PLAYER3)
#
# PLAYER3 and PLAYER4 check the flop
#
game.check(PLAYER3)
game.check(PLAYER4)
#
# PLAYER3 and PLAYER4 check the turn
#
game.check(PLAYER3)
game.check(PLAYER4)
#
# PLAYER3 and PLAYER4 check the river
#
game.check(PLAYER3)
game.check(PLAYER4)
'''
#
# Print the winner(s)
#
print "*" * 70
for winner in game.winners:
    print "The winner is PLAYER%d with %s" % ( winner, game.readablePlayerBestHands(winner) )
