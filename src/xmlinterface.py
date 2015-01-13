import xml.etree.ElementTree as ElementTree
from xml.dom.minidom import parse


class JobPraser(object):
    """JobPraser
    JobParser creates an object of selected jenkins job and allows modifications
    included in the interface.
    """

    def __init__(self, filepath):
        self.name = filepath
        self.tree = ElementTree.parse(filepath)
        self.root = self.tree.getroot()
        #self.domek = parse(open('lol.xml'))

    def get_shell_command(self, number):
        """get_shell_command: returns the indicated command

        :param number: (int) command number in file

        :return: (str) command string
        """
        return self.root.findall('./builders/hudson.tasks.Shell/command')[number].text

    def get_shell_commands(self):
        """get_shell_commands: returns list with command's strings

        :return: (list) return list of command's strings
        """
        commands = []

        for command in self.root.findall('./builders/hudson.tasks.Shell/command'):
            commands.append(command.text)

        return commands

    def replace_shell_command(self, number, newcommand):
        """replace_shell_command: replaces the selected command with the new value from
        newcommand variable

        :param number: command number in file
        :param newcommand: value of new command
        """
        self.root.findall('./builders/hudson.tasks.Shell/command')[number].text = newcommand

    def replace_shell_commands(self, newcommands):
        """replace_shell_commands: updates all commands in config file

        :param newcommands: (list) is the list of commands strings
        """
        commands = self.root.findall('./builders/hudson.tasks.Shell/command')

        for command, newcommand in zip(commands, newcommands):
            command.text = newcommand

    def update_file(self):
        """update_file: save all changes in xml file and update it"""
        self.tree.write(self.name)
