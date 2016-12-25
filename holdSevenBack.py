# -*- coding: utf-8 -*-
# filename: holdSevenback.py

import random
import string
from connection import connection
from reply import ReplyMessage

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
		for handcard in self.hand:
			if card.color == handcard.color and card.value == handcard.value:
				self.hand.remove(handcard)
				return True

		return False

	def keep_card(self, card):
		for handcard in self.hand:
			if card.color == handcard.color and card.value == handcard.value:
				self.hand.remove(handcard)
				self.penalty.append(handcard)
				return True

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
		text_array = []
		for card in self.hand:
			text_array.append(card.get_text())
		text_array.sort()
		text = ''
		for card_text in text_array:
			text += card_text + ' '
		return text

	def get_penalty_text(self):
		text_array = []
		for card in self.penalty:
			text_array.append(card.get_text())
		text_array.sort()
		text = ''
		for card_text in text_array:
			text += card_text + ' '
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
				#print player.nickname + card.get_text()

	def next_turn(self, player ,card, action):
		if self.turn_count >= turns_num:
			return "游戏已结束"

		current_player = self.players[self.turn_count % players_num]

		if current_player != player:
			return "还没到你的回合"

		if action == 'KEEP':
			if self.__have_card_to_throw():
				return '你有能出的牌'
			if current_player.keep_card(card):
				self.turn_count += 1
				if self.turn_count >= turns_num:
					return "游戏已结束"
				return 'OK'
			else:
				return '你没有这张牌'
		elif action == "THROW":
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
		if values[card.value] == 7:
			return True

		index = values[card.value]-1
		left_index = values[card.value]-2
		right_index = values[card.value]
		if self.cards_on_desk[card.color][index] == False:
			if left_index < 0:
				if self.cards_on_desk[card.color][right_index] == True:
					return True
				else:
					return False
			if right_index >= len(self.cards_on_desk[card.color]):
				if self.cards_on_desk[card.color][left_index] == True:
					return True
				else:
					return False
			if self.cards_on_desk[card.color][left_index] != self.cards_on_desk[card.color][right_index]:
				return True

		return False

	def get_current_player(self):
		return self.players[self.turn_count % players_num]

	def get_desk_cards_text(self):
		result = ''
		for color in colors:
			result = result + color + ' '
			for i, boo in enumerate(self.cards_on_desk[color]):
				if boo == True:
					value_text = values.keys()[values.values().index(i+1)]
					result += value_text
				else:
					result += '-'
			result += '\n'

		return result



class HoldSevenBackGame():
	def __init__(self):
		self.players_in_waiting = []
		self.players_at_table = {}

	def __messages_before_turn(self, table):
		#----Message----
		# print 'Send to all: 轮到' + table.get_current_player().nickname + "出牌\n"
		# print '桌面\n' + table.get_desk_cards_text()
		# print 'Send to ' + table.get_current_player().nickname + ':手牌\n' + table.get_current_player().get_hand_text()

		text1 = '轮到' + table.get_current_player().nickname + "出牌"
		text2 = '桌面:\n' + table.get_desk_cards_text()

		for player in table.players:
			message1 = ReplyMessage(player.openid, connection.me, text1, 'text')
			message2 = ReplyMessage(player.openid, connection.me, text2, 'text')
			connection.send_message(message1.get_json())
			connection.send_message(message2.get_json())

		text3 = '手牌:\n' + table.get_current_player().get_hand_text()
		message3 = ReplyMessage(table.get_current_player().openid, connection.me, text3, 'text')
		connection.send_message(message3.get_json())
		#---------------

	def __messages_after_turn(self, table, player, card, action):
		#----Message----
		if action == 'KEEP':
			# print 'Send to all:' + player.nickname + '扣了一张牌'
			text = player.nickname + '扣了一张牌'
			for player in table.players:
				message = ReplyMessage(player.openid, connection.me, text, 'text')
				connection.send_message(message.get_json())
		elif action == 'THROW':
			# print 'Send to all:' + player.nickname + '出了一张牌' + card.get_text()
			text = player.nickname + '出了一张牌' + card.get_text()
			for player in table.players:
				message = ReplyMessage(player.openid, connection.me, text, 'text')
				connection.send_message(message.get_json())
		else:
			return
		#print 'Send to all: 回合结束'
		text = '---回合结束---'
		for player in table.players:
			message = ReplyMessage(player.openid, connection.me, text, 'text')
			connection.send_message(message.get_json())
		#---------------

	def __messages_game_start(self, table):
		#----Message----
		# print "Send to all: 游戏开始，玩家：\n"
		# for player in table.players:
		# 		print player.nickname + '\n'
		# print "Send to all: 正在发牌...\n"
		text1 = '游戏开始，玩家：\n'
		for player in table.players:
			text1 += player.nickname + '\n'		
		text2 = '正在发牌...'

		for player in table.players:
			message1 = ReplyMessage(player.openid, connection.me, text1, 'text')
			message2 = ReplyMessage(player.openid, connection.me, text2, 'text')
			connection.send_message(message1.get_json())
			connection.send_message(message2.get_json())

		self.__messages_before_turn(table)
		#---------------

	def __messages_game_over(self, table):
		#----Message----
		text1 = '游戏结束! 得分如下：\n'
		for player in table.players:
			text1 += player.nickname + ': ' + str(player.get_score()) + '\n'
		text2 = '已经退出游戏'
		for player in table.players:
			message1 = ReplyMessage(player.openid, connection.me, text1, 'text')
			message2 = ReplyMessage(player.openid, connection.me, text2, 'text')
			connection.send_message(message1.get_json())
			connection.send_message(message2.get_json())		
		# print "Send to all:" + text1
		# print "Send to all: 已经退出游戏"
		#---------------

	def __messages_player_quit(self, table):
		#----Message----
		#print 'Send to all: 玩家退出，游戏结束'
		text = '玩家退出，游戏结束'
		for player in table.players:
			message = ReplyMessage(player.openid, connection.me, text, 'text')
			connection.send_message(message.get_json())
		#---------------

	def __messages_broadcast(self, table, player, content):
		#----Message----
		#print 'Send to all:' + player.nickname + content + '\n'
		text = player.nickname + content
		for player in table.players:
			message = ReplyMessage(player.openid, connection.me, text, 'text')
			connection.send_message(message.get_json())
		#---------------

	def __messages_help(self, player):
		#----Message----
		#print 'Send to ' + player.nickname + 'HELPSOMETHING'
		text = ('游戏说明:\n\n'+
			    '四种花色用 @ # * + 表示\n'+
			    '数值用A2345678910JQK表示\n\n'+
			    '-输入DESK查看桌面上的牌\n'+
			    '-输入HAND查看手牌\n'+
			    '-输入PENALTY查看已扣的牌\n\n'+
			    '-输入KEEP [card] 进行扣牌\n'+
			    '   例：KEEP @K\n'+
			    '-输入THROW [card] 进行出牌\n'+
			    '   例：THROW #A\n\n'+
			    '-输入SAY [Something]说话\n'+
			    '   例：SAY love you\n\n'+
			    '-输入QUIT GAME退出游戏\n'+
			    '-输入HELP查看帮助')
		message = ReplyMessage(player.openid, connection.me, text, 'text')
		connection.send_message(message.get_json())
		#---------------

	def __messages_add_player(self, player):
		#----Message----
		#print 'Send to ' + player.nickname + '正在寻找玩家...'
		text = '正在寻找玩家...'
		message = ReplyMessage(player.openid, connection.me, text, 'text')
		connection.send_message(message.get_json())
		#---------------


	def add_player(self, player):
		if player in self.players_in_waiting:
			return
		if player.openid in self.players_at_table.keys():
			return 

		self.players_in_waiting.append(player)
		print "Players in waiting:"
		print self.players_in_waiting

		#----Message----
		self.__messages_help(player)
		self.__messages_add_player(player)
		#---------------


		if len(self.players_in_waiting) == players_num:
			new_table = Table(self.players_in_waiting)
			for player in self.players_in_waiting:
				self.players_at_table[player.openid] = new_table
			new_table.draw_cards()

			#----Message----
			self.__messages_game_start(new_table)
			#---------------

			self.players_in_waiting = []

	def player_quit(self, player):
		if player.openid in self.players_at_table.keys():
			table = self.players_at_table[player.openid]
			#----Message----
			self.__messages_player_quit(table)
			#---------------
			self.clean_table(table)
		else:
			self.players_in_waiting.remove(player)

	def clean_table(self, table):
		for temp in table.players:
			self.players_at_table.pop(temp.openid)

	def is_player_waiting(self, player):
		return player in self.players_in_waiting

	def get_player_table(self, player):
		if player.openid in self.players_at_table.keys():
			return self.players_at_table[player.openid]
		else:
			return


	def process(self, player, command):
		if player.openid in self.players_at_table.keys():
			table = self.players_at_table[player.openid]

			if command == 'QUIT GAME':
				#self.player_quit(player)
				return ['已经退出游戏']
			elif command =='HELP':
				self.__messages_help(player)
				return []
			elif command == 'DESK':
				return ['桌面\n' + table.get_desk_cards_text()]
			elif command == 'HAND':
				return ['手牌\n' + player.get_hand_text()]
			elif command == 'PENALTY':
				return ['扣牌\n' + player.get_penalty_text()]
			elif command.startswith('SAY'):
				#----Message----
				self.__messages_broadcast(table, player, command.upper())
				return []
				#---------------
			elif command.startswith('KEEP') or command.startswith('THROW'):
				split_command = command.split(' ')
				if len(split_command) != 2 or len(split_command[1]) < 2:
					return ['指令格式错误']

				value = split_command[1][1:]
				color = split_command[1][0]

				if color not in colors:
					return ['指令格式错误']
				if value not in values.keys():
					return ['指令格式错误']

				card = Card(color,value)
				
				if command.startswith('KEEP'):
					response = table.next_turn(player, card, 'KEEP')
					if response == "游戏已结束":
						#----Message----
						self.__messages_after_turn(table, player, card, 'KEEP')
						self.__messages_game_over(table)
						#---------------
						#self.clean_table(table)
					elif response == "OK":
						#----Message----
						self.__messages_after_turn(table, player, card, 'KEEP')
						self.__messages_before_turn(table)
						#---------------
					return [response]
				else:
					response = table.next_turn(player, card, 'THROW')
					if response == "游戏已结束":
						#----Message----
						self.__messages_after_turn(table, player, card, 'THROW')
						self.__messages_game_over(table)
						#---------------
						#self.clean_table(table)
					elif response == "OK":
						#----Message----
						self.__messages_after_turn(table, player, card, 'THROW')
						self.__messages_before_turn(table)
						#---------------
					return [response]

			else:
				return ['游戏中无该指令']
		elif player in self.players_in_waiting:
			if command == 'QUIT GAME':
				#self.player_quit(player)
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


