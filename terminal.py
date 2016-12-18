import random
from commands import commands
from connection import connection

def process(user, content):
    if user in connection.user_list:
        if connection.user_list[user] == 'Started':
            if content == "human":
                connection.user_list[user] = 'Logged In'
                result1 = "Identifying...Success."
                result2 = "Welcome, " + connection.get_user_info(user)['nickname'] + "\nType [help] for help."
                result2 = result2.encode('utf-8')
                result_list = [result1, result2]
                return result_list
            elif content == "AI":
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
            # to improve
            elif 'XMASGIFTME' in content:
                if len(connection.gift_list) == 0:
                    connection.gift_list[1] = connection.get_user_info(user)['nickname'] + " wants " + content
                else:
                    exchange = random.randint(1, len(connection.gift_list)+1)
                    gift = connection.gift_list[exchange]
                    connection.gift_list[len(connection.gift_list)+1] = gift
                    connection.gift_list[exchange] = connection.get_user_info(user)['nickname'] + " wants " + content
            elif 'ZBUG!OPERATIONAL!' in content:
                 result_list = []
                 for i in range(0, len(connection.gift_list)):
                     from reply import ReplyMessage
                     reply_message = ReplyMessage(connection.zbug[i], connection.me, connection.gift_list[i], 'text')
                     connection.send_message(reply_message)
                     result_list.append(connection.gift_list[i])
                 return result_list
            else:
                # print 4
                result_list = [commands.get(content)]
                return result_list
    else:
        if content == "Dogi":
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
