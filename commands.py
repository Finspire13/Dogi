#TODO deal with the mass
class Command:
        def __init__(self):
                self.commands = {
                        "help": ("These commands are defined internally:\n\n" +
                                 "info [subject]\n" +
                                 "<Get information about the subject.>\n\n" +
                                 "list [option]\n" +
                                 "<Get file list. Specify maximum files to show on screen. Latest ones will be shown. '-a' for all files.>\n\n" +
                                 "open [filename]\n" +
                                 "<Open file>\n\n" +
                                 "shutdown\n" +
                                 "<Shut down the terminal.>"),

                        "list": ("0x0089AB readme 20161211\n" +
                                 "0x01000D File Missing\n" +
                                 "0x00C000 File Missing\n" +
                                 "0x0F9090 File Missing\n" +
                                 "0x011115 File Missing\n" +
                                 "0x0843C4 File Missing\n"),

                        "list -a": ("0x0089AB readme 20161211\n" +
                                    "0x01000D File Missing\n" +
                                    "0x00C000 File Missing\n" +
                                    "0x0F9090 File Missing\n" +
                                    "0x011115 File Missing\n" +
                                    "0x0843C4 File Missing\n"),

                        "info Dogi": ("Dogi series is an advanced AI system in development.\n\n" +
                                      "Dogi with its full ability will promise human a brave new world.\n\n" +
                                      "The main contributor to Dogi is Dr.Ferrari. Dogi is supported by Ginne Inc."),

                        "info Mr.Dog": "A great man",

                        "info Dr.Ferrari": ("Donald Ferrari is an American computer scientist." +
                                            " He is the author of the multi-volume work Principles of Intelligent Agent." +
                                            " He contributed to the development of highly-reliable AI system.\n" +
                                            "Personal website: 123.206.179.29/ferrari"),

                        "info Ginne": (
                        "Ginne is an multinational technology company with the vision of reducing the 'risk of human extinction' " +
                        "and conducting space exploration."),

                        "info Ginne Inc.": (
                        "Ginne is an multinational technology company with the vision of reducing the 'risk of human extinction' " +
                        "and conducting space exploration."),

                        "info RAIRC": ("Robots and Artificial Intelligence Regulatory Commission (RAIRC) " +
                                       "is an international agency tasked with protecting public safety against misuse of AI and robots." +
                                       "RAIRC was established in 2015 as a result of Shanghai Protocol."),

                        "info Shanghai Protocol": "Missing",

                        "open readme": ("Something dangerous is hidden in this system and you must find it.\n\n" +
                                        "Dogi terminals are synced with Dogi Cloud Server. You need to check Dogi for every update.\n\n" +
                                        "Good Luck.\n\n" +
                                        "EOF")
                }
        def get(self, command):
                return self.commands.get(command, "Command Not Found")

commands = Command()
