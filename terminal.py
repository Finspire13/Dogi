import random
import string
from commands import commands
from connection import connection

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
            elif 'xmasgiftme' in content:
                name = connection.get_user_info(user)['nickname']
                connection.gift_list[name] = name + ": " + originalContent
                print connection.gift_list
                result = "Recorded: " + name + ": " + originalContent
                result_list = [result.encode("utf-8")]
                if user not in connection.zbug:
                    connection.zbug.append(user)
                    print len(connection.zbug)
                return result_list
            elif '!zbug!' in content:
                 result_list = []
                 random.shuffle(connection.zbug)
                 for i, user in enumerate(connection.gift_list.keys()):
                     from reply import ReplyMessage
                     reply_message = ReplyMessage(connection.zbug[i], connection.me, connection.gift_list[user], 'text')
                     try:
                         connection.send_message(reply_message.get_json().encode("utf-8"))
                         result_list.append(user.encode("utf-8"))
                     except Exception as e:
                         print str(e)
                 connection.zbug = []
                 connection.gift_list = dict()
                 return result_list
            else:
                # print 4
                result_list = [commands.get(content)]
                return result_list
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
