# -*- coding: utf-8 -*-
# filename: hold7back.py

import random
import string

values = {
	'A':1,
	'2':2,
	'3':3,
	'4':4,
	'5':5,
	'6':6,
	'7':7,
	'8':8,
	'9':9,
	'10':10,
	'J':11,
	'Q':12,
	'K':13
}

colors = ['@','#','*','+']

values_num = 13
turns_num = 52
players_num = 4 

class Card:
	def __init__(self, color, value):     #str, str
		self.color = color
		self.value = value

	def get_text(self):
		return self.color + self.value


class Player:
	def __init__(self, openid, nickname):
		self.openid = openid
		self.nickname = nickname
		self.hand = []
		self.penalty = []

	def draw_card(self, card):
		self.hand.append(card)

	def throw_card(self, card):
		if card in self.hand:
			self.hand.remove(card)
			return True
		else:
			return False

	def keep_card(self, card):
		if card in self.hand:
			self.hand.remove(card)
			self.penalty.append(card)
			return True
		else:
			return False

	def get_score(self):
		score = 0
		for card in self.penalty:
			score += values[card.value]
		return score

	def clear(self):
		del self.hand[:]
		del self.penalty[:]
		self.hand = []
		self.penalty = []

	def get_hand_text(self):
		text = ''
		for card in self.hand:
			text += card.get_text() + ' '
		return text

	def get_penalty_text(self):
		text = ''
		for card in self.penalty:
			text += card.get_text() + ' '
		return text




class Table:
	def __init__(self, players):
		self.players = players
		random.shuffle(players)

		self.cards_on_desk = { '@': [False] * values_num, 
						       '#': [False] * values_num, 
						       '*': [False] * values_num, 
						       '+': [False] * values_num}

		self.turn_count = 0

	def shuffle(self):
		card_stack = []
		for value in values.keys():
			for color in colors:
				card = Card(color, value)
				card_stack.append(card)

		random.shuffle(card_stack)
		return card_stack

	def draw_cards(self):
		card_stack = self.shuffle()

		for player in self.players:
			player.clear()

		while card_stack:
			for player in self.players:
				card = card_stack.pop()
				player.draw_card(card)
				print player.nickname + card.get_text()

	def next_turn(self, player ,card, action):
		if self.turn_count >= turns_num:
			return "游戏已结束"

		current_player = self.players[self.turn_count % players_num]

		if current_player != player:
			return "还没到你的回合"

		if action == 'Keep':
			if self.__have_card_to_throw():
				return '你有能出的牌'
			if current_player.keep_card(card):
				self.turn_count += 1
				if self.turn_count >= turns_num:
					return "游戏已结束"
				return 'OK'
			else:
				return '你没有这张牌'
		elif action == "Throw":
			if not self.__can_throw_card(card):
				return '你不能出这张牌'
			if current_player.throw_card(card):
				index = values[card.value]-1
				self.cards_on_desk[card.color][index] = True
				self.turn_count += 1
				if self.turn_count >= turns_num:
					return "游戏已结束"
				return 'OK'
			else:
				return '你没有这张牌' 
		else:
			return '无效操作'

	def __have_card_to_throw(self):
		current_player = self.players[self.turn_count % players_num]

		for card in current_player.hand:
			if self.__can_throw_card(card):
				return True

		return False

	def __can_throw_card(self, card):
		index = values[card.value]-1
		left_index = values[card.value]-2
		right_index = values[card.value]
		if self.cards_on_desk[card.color][index] == False:
			if left_index < 0:
				if self.cards_on_desk[card.color][right_index] == True:
					return True
			if right_index >= len(self.cards_on_desk[card.color]):
				if self.cards_on_desk[card.color][left_index] == True:
					return True
			if self.cards_on_desk[card.color][left_index] != self.cards_on_desk[card.color][right_index]:
				return True

		return False

	def get_current_player(self):
		return self.players[self.turn_count % players_num]


class HoldSevenBackGame():
	def __init__(self):
		self.players_in_waiting = []
		self.players_at_table = {}

	def add_player(self, player):
		if player in self.players_in_waiting:
			return
		if player.openid in self.players_at_table.keys():
			return 

		self.players_in_waiting.append(player)
		if len(self.players_in_waiting) == players_num:
			new_table = Table(self.players_in_waiting)
			for player in self.players_in_waiting:
				self.players_at_table[player.openid] = new_table
			new_table.draw_cards()

			print "游戏开始\n"
			for player in self.players_in_waiting:
				print player.openid + '\n'
			print new_table.get_current_player().nickname + "出牌\n"
			print '手牌\n' + new_table.get_current_player().get_hand_text()

			self.players_in_waiting = []

	def __player_quit(self, player):
		if player.openid in self.players_at_table.keys():
			table = self.players_at_table[player.openid]
			self.__clean_table(table)
			print '玩家退出，游戏结束\n'
		else:
			self.players_in_waiting.remove(player)

	def __clean_table(self, table):
		for temp in table.players:
			self.players_at_table.pop(temp.openid)

	def process(self, player, command):
		if player.openid in self.players_at_table.keys():
			if command == 'QUIT GAME':
				self.__player_quit(player)
				return []
			elif command == 'HAND':
				return ['手牌\n' + player.get_hand_text()]
			elif command == 'PENALTY':
				return ['扣牌\n' + player.get_hand_text()]
			elif command.startswith('SAY'):
				print player.nickname + command + '\n'
			elif command.startswith('KEEP') or command.startswith('THROW'):
				split_command = command.split(' ')
				if len(split_command) != 2 or len(split_command[1]) < 2:
					return ['指令格式错误']

				value = split_command[1][1:]
				color = split_command[1][0]

				if not color in colors:
					return ['指令格式错误']
				if not value in values.keys:
					return ['指令格式错误']

				card = Card(color,value)
				table = self.players_at_table[player.openid]

				if command.startswith('KEEP'):
					response = table.next_turn(player, card, 'Keep')
					if response == "游戏已结束":
						self.__clean_table(table)
						game_result = '游戏结束! 得分如下：\n'
						for temp in table.players:
							game_result += temp.nickname + ': ' + temp.get_score() + '\n'
						print game_result
						return []
					return [response]
				else:
					response = table.next_turn(player, card, 'THROW')
					if response == "游戏已结束":
						self.__clean_table(table)
						game_result = '游戏结束! 得分如下：\n'
						for temp in table.players:
							game_result += temp.nickname + ': ' + temp.get_score() + '\n'
						print game_result
						return []
					return [response]

			else:
				return ['Command Not Found']
		elif player in self.players_in_waiting:
			if command == 'QUIT GAME':
				self.__player_quit(player)
				return ['已经退出游戏']
			else:
				return ['正在寻找玩家...']
		else:
			return []

hold_seven_back_game = HoldSevenBackGame()

#FFFFFFFTTTTFFFFF
#FTTTTTTTTTTTTTTF
#import hold7back
#import hold_7_back_game from hold7back


