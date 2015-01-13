#!/usr/bin/env python2

import tempfile, subprocess, shutil
from xmlinterface import JobPraser

class Editor(object):

    @staticmethod
    def edit_commands(filepath):
        job = JobPraser(filepath)

        #List with files objects
        tempfiles = []
        #List with files names for vim
        templist = []

        for command in job.get_shell_commands():
            temp = tempfile.NamedTemporaryFile(prefix=filepath,suffix='.job')
            open(temp.name, 'w').write(command)
            tempfiles.append(temp)
            templist.append(temp.name)

        subprocess.call(['vim', '-o'] + templist)

        newcommands = []

        for temp in tempfiles:
            newcommands.append(open(temp.name,'r').read())
            temp.close() 

        job.replace_shell_commands(newcommands)
        job.update_file()
