#!python3
# coding: utf-8

"""
The 'CommandsParser' class is used to parse messages the bot receives.
It defines the character (or characters) at the start of a message that define a bot command ('!' in this case) and
parses the whole message for arguments.
When instantiated it first reads all the classes inside the Commands class in Commands.py, which are the actual bot
commands. Then parses the arguments available in each message with respect to the detected command.
Outputs error messages defined on each command class as well as the actual output of the command.
If no command is detected or an inexistent command is given, message is ignored.
"""

from .Commands import Commands


class CommandsParser:
    def __init__(self, command_identifier='!'):
        # Character at the start of a message that identifies it as a bot command
        self.command_identifier = command_identifier

        # Get all attributes (classes) from Commands and keep only those that do not start with '_'
        commands = filter(lambda attribute: not attribute[0].startswith('_'), Commands.__dict__.items())

        # Dictionary with command string associated with the correct command class
        self.commands_dict = {command.name: command() for _, command in commands}

    def parse_args(self, raw_string):
        """
        Parse commands given to bot

        :param raw_string: str
            message received by discord.Client (message.content)
        """
        if raw_string.startswith(self.command_identifier) and len(raw_string) > len(self.command_identifier):
            raw_command, *arguments = raw_string[len(self.command_identifier):].split()

            if raw_command in self.commands_dict:
                command_class = self.commands_dict[raw_command]
                n_args = command_class.n_args
                args_type = command_class.args_type

                if n_args == 0:
                    if len(arguments) == 0:
                        return command_class.command()
                    else:
                        return command_class.message_on_fail
                else:
                    try:
                        converted_args = [args_type(arg) for arg in arguments] if args_type != str else arguments
                    except ValueError:
                        return command_class.message_on_fail
                    else:
                        if n_args is None:
                            if len(arguments) > 0:
                                return command_class.command(*converted_args)
                            else:
                                return command_class.message_on_fail
                        elif n_args > 0:
                            if len(arguments) == n_args:
                                return command_class.command(*converted_args)
                            else:
                                return command_class.message_on_fail
