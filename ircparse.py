#!/usr/bin/env python2
# Parse Texas Hold'em hand logs from the IRC poker database at:
# http://poker.cs.ualberta.ca/IRCdata/

import os, os.path
from pokerengine.pokergame import PokerGameServer

'''
Player data for a single hand, parsed from a line in the player's pdb file.

Sample lines with column labels:
player             #play prflop    turn         bankroll    winnings
          timestamp    pos   flop       river          action     cards
Marzon    766303976  8  1 Bc  bc    kc    kf      12653  300    0
spiney    766303976  8  2 Bc  cc    kc    f       10237  300    0
doublebag 766303976  8  3 cc  r     b     bc       7842  500    0 Jh Qh
neoncap   766303976  8  4 f   -     -     -        7857    0    0
maurer    766303976  8  5 f   -     -     -       12711    0    0
andrea    766303976  8  6 cc  c     c     f        7190  300    0
zorak     766303976  8  7 r   c     c     cc       4460  500    0 As Kc
justin    766303976  8  8 c   c     c     r        4304  500 2400 Ad Qs
'''
class IRCPlayer():
	def __init__(self, line):
		print 'Using player:', line
		tokens = line.split()
		self.name = line[0]
		self.pos = int(tokens[3])
		self.actions = dict()
		self.actions['pre-flop'] = tokens[4]
		self.actions['flop'] = tokens[5]
		self.actions['turn'] = tokens[6]
		self.actions['river'] = tokens[7]
		print 'Actions:', self.actions

	def __str__(self):
		return self.name + ': ' + str(self.actions)

def takeAction(game, state, serial, player):
	assert player.actions[state]
	action = player.actions[state][0]
	player.actions[state] = player.actions[state][1:]
	print action
	if action == '-':
		raise Exception('player is out of the game!')
	elif action == 'B':
		game.blind(serial)
	elif action == 'f':
		game.fold(serial)
	elif action == 'c':
		game.call(serial)
	elif action == 'r' or action == 'b': # FIXME: is this right? are bet and raise the same action in this simulator?
		game.callNraise(serial, 5000)
	elif action == 'k':
		game.check(serial)
	else:
		print 'Possible actions: ' + str(game.possibleActions(serial))
		raise Exception('unknown action "'+action+'"')

def playGame(timestamp, playerNames):
	players = dict()
	numPlayers = len(playerNames)
	for name in playerNames:
		f = open(os.path.join(basedir, 'pdb', 'pdb.'+name))
		player = None
		for line in f:
			if line.split()[1] == timestamp:
				player = IRCPlayer(line)
				break
		assert player
		players[player.pos] = player
	print players

	game = PokerGameServer("poker.%s.xml", ['/etc/poker-engine'])
	game.verbose = 1
	game.setVariant("holdem")
	game.setBettingStructure("10-20-pot-limit")

	# Each player sits at the table and buys in 1500.
	# The blinds are posted automatically, no action is required from
	# the player.
	for serial in range(1, 1+numPlayers):
		#serial = numPlayers - i
		game.addPlayer(serial)
		game.payBuyIn(serial, 1500*100)
		game.sit(serial)
		#game.autoBlindAnte(serial)

	game.setDealer(numPlayers-1)

	game.beginTurn(1)
	print 'current round:', game.current_round
	print 'dealer:', game.player_list[game.dealer]

	print 'next player:', game.getSerialInPosition()
	while game.state in ['blindAnte', 'pre-flop', 'flop', 'turn', 'river']:
		serial = game.getSerialInPosition()
		player = players[serial]
		print serial, game.canAct(serial)

		state = game.state
		if state == 'blindAnte': state = 'pre-flop'
		takeAction(game, state, serial, player)

	print "*" * 70
	for winner in game.winners:
		print "The winner is PLAYER%d with %s" % ( winner, game.readablePlayerBestHands(winner) )

        return game

if __name__ == '__main__':
	basedir = 'holdem/200109'
	hroster = open(os.path.join(basedir, 'hroster'), 'r')
	for i in range(10): hroster.readline()
	rosterLine = hroster.readline().split()
	print rosterLine
	assert len(rosterLine[2:]) == int(rosterLine[1])
        for i in range(5001):
            game = playGame(rosterLine[0], rosterLine[2:])
            print "BANK %d,%d" % (i, game.getPlayer(4).money)


