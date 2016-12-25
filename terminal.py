# -*- coding: utf-8 -*-
# filename: terminal.py

import random
import string
from commands import commands
from connection import connection
import holdSevenBack
from holdSevenBack import hold_seven_back_game

def process(user, content):
    originalContent = content
    content = content.lower()
    if user in connection.user_list:
        if connection.user_list[user] == 'Started':
            if content == "human":
                connection.user_list[user] = 'Logged In'
                result1 = "Identifying...Success."
                result2 = "Welcome, " + connection.get_user_info(user)['nickname'] + "\nType [help] for help."
                result2 = result2.encode('utf-8')
                result_list = [result1, result2]
                return result_list
            elif content == "ai":
                connection.user_list.pop(user)
                result1 = "Authenticating..."
                result2 = ("Permission Denied: \nAI Unregistered with RAIRC.\n" +
                           "------------------\n" +
                           "Terminal shutting down.")
                result_list = [result1, result2]
                return result_list
            else:
                connection.user_list.pop(user)
                result1 = ("Permission Denied: \nInvalid response.\n" +
                           "------------------\n" +
                           "Terminal shutting down.")
                result_list = [result1]
                return result_list

        elif connection.user_list[user] == 'Logged In':
            if content == "shutdown":
                # print 3
                connection.user_list.pop(user)
                # print connection.activeUserSet
                result1 = "Logged out, " + connection.get_user_info(user)['nickname']
                result1 = result1.encode('utf-8')
                result2 = ("Shutting Down\n" +
                           "=============>100%\n" +
                           "Finished.")
                result_list = [result1, result2]
                return result_list
            elif content == 'users':
                result=''
                random_string1 = ''.join(random.sample(string.lowercase+string.digits ,7))
                random_string2 = ''.join(random.sample(string.lowercase+string.digits ,7))
                result = result + "AI : " + random_string1 + '\n'
                result = result + "AI : " + random_string2 + '\n'
                result = result + 'Dr.Ferrari\n'

                for user_id in connection.user_list.keys():
                    if connection.user_list[user_id] == 'Logged In':
                        result = result + connection.get_user_info(user_id)['nickname'].encode("utf-8") + '\n'

                result_list = [result]
                return result_list
            elif content == 'hold7back':
                nickname = connection.get_user_info(user)['nickname']
                new_player = holdSevenBack.Player(user, nickname.encode('utf-8'))
                hold_seven_back_game.add_player(new_player)
                connection.hold_seven_back_players[user] = new_player
                connection.user_list[user] = 'In Hold7back'
                return []

            elif 'xmasgiftme' in content:
                if user in connection.zbug_user:
                    return ["Don't want too much."]
                nickname = connection.get_user_info(user)['nickname']
                connection.gift_list.append(nickname + ": " + originalContent)
                connection.zbug_user.append(user)
                print connection.zbug_user
                print connection.gift_list
                result = "Done! Merry Xmas! " + nickname
                result_list = [result.encode("utf-8")]

                return result_list

            elif '!zbug!' in content:
                
                from reply import ReplyMessage
                result_list = []
                random.shuffle(connection.gift_list)
                for i, gift in enumerate(connection.gift_list):
                    reply_message = ReplyMessage(connection.zbug_user[i], connection.me, gift, 'text')
                    connection.send_message(reply_message.get_json().encode("utf-8"))
                    nickname = connection.get_user_info(connection.zbug_user[i])['nickname']
                    result_list.append(nickname.encode("utf-8"))

                random_index = random.randint(0, len(connection.zbug_user)-1)
                the_lucky_one = connection.zbug_user[random_index]
                reply_message = ReplyMessage(the_lucky_one, connection.me, 'You are the lucky one to have Dogi special gift!', 'text')

                connection.send_message(reply_message.get_json().encode("utf-8"))
                nickname = connection.get_user_info(the_lucky_one)['nickname']
                result_list.append("The Lucky One:" + nickname.encode("utf-8"))
                

                connection.zbug_user = []
                connection.gift_list = []

                    
                return result_list
            else:
                # print 4
                result_list = [commands.get(content)]
                return result_list
        elif connection.user_list[user] == 'In Hold7back':
            content = content.upper()
            player = connection.hold_seven_back_players[user]
            resultList = hold_seven_back_game.process(player, content)

            # Not so good
            if content == 'QUIT GAME':
                if hold_seven_back_game.is_player_waiting(player)
                    connection.hold_seven_back_players.pop(user)
                    connection.user_list[user] = 'Logged In'
                else:
                    table = hold_seven_back_game.get_player_table(player)
                    for player in table.players:
                        connection.hold_seven_back_players.pop(player.openid)
                        connection.user_list[player.openid] = 'Logged In'

                hold_seven_back_game.player_quit(player)


            
            if resultList == ['游戏已结束']:
                table = hold_seven_back_game.get_player_table(player)
                for player in table.players:
                    connection.hold_seven_back_players.pop(player.openid)
                    connection.user_list[player.openid] = 'Logged In'

                hold_seven_back_game.clean_table(table)

            return resultList

    else:
        if content == "dogi":
            connection.user_list[user] = 'Started'
            result1 = ("Dogi Instance #" + str(int(random.random() * 70 + 30)) + "\nVersion 1.0.2\n" +
                       "==============>100%\n" +
                       "Terminal Started.")
            result2 = "Are you human or AI? [human/AI]"
            result_list = [result1, result2]
            return result_list
        else:
            result_list = ["Enter 'Dogi' to activate its terminal."]
            return result_list
