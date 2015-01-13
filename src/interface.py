#!/usr/bin/env python3

import curses
import os
from editor import Editor
import fcntl
from utils import *

(consolewidth, consoleheight) = getTerminalSize()

class JobsMenu(object):

    J_NUM = 119
    T_HEIGHT = 65

    def __init__(self, items, stdscreen):
        self.window = curses.newpad(121, int(consolewidth)-2)
        self.window.refresh(0, 0, 5, 1, int(consoleheight)-2,
                            int(consolewidth)-2)
        self.position = 0
        self.items = items

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        self.window.clear()
        self.window.box()

        while True:
            self.refresh_menu()
            self.menu_key_manage()
            self.menu_display_manage()

        self.window.clear()
        curses.doupdate()

    def refresh_menu(self):
        if (self.position in range(self.T_HEIGHT, self.J_NUM) or
           self.position in range(self.J_NUM+self.T_HEIGHT, 2*self.J_NUM) or
           self.position in range(2*self.J_NUM+self.T_HEIGHT, 3*self.J_NUM) or
           self.position in range(3*self.J_NUM+self.T_HEIGHT, 4*self.J_NUM)):
            self.window.refresh(54, 0, 5, 1, 119-2,
                                int(consolewidth)-2)
        else:
            self.window.refresh(0, 0, 5, 1, int(consoleheight)-2,
                                int(consolewidth)-2)

        curses.doupdate()

    def menu_display_manage(self):
        for index, item in enumerate(self.items):
            if index == self.position:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            msg = '%s' % (item[0])
            if index < self.J_NUM:
                self.window.addstr(1+index, 1, msg, mode)
            elif index < 2*self.J_NUM:
                self.window.addstr(1+index-self.J_NUM, 50, msg, mode)
            elif index < 3*self.J_NUM:
                self.window.addstr(1+index-2*self.J_NUM, 100, msg, mode)
            elif index < 4*self.J_NUM:
                self.window.addstr(1+index-3*self.J_NUM, 150, msg, mode)

    def menu_key_manage(self):
        key = self.window.getch()

        if key in [curses.KEY_ENTER, ord('\n')]:
            if self.position == len(self.items)-1:
                return False
            else:
                Editor.edit_commands(str(self.items[self.position][1]))
                self.window.clear()
                self.window.box()
                return False
        elif key == 65:
            self.navigate(-1)
        elif key == 66:
            self.navigate(1)
        elif key == 67:
            self.navigate(self.J_NUM)
        elif key == 68:
            self.navigate(-self.J_NUM)

        return True


class JenkinsConf(object):

    def __init__(self, stdscreen, jenkinsdir):
        self.screen = stdscreen
        curses.curs_set(0)

        os.chdir(jenkinsdir + "/jobs")
        jobs = os.listdir(jenkinsdir + "/jobs")
        print(consolewidth)

        win = stdscreen.subwin(3, int(consolewidth) - 2, 2, 1)
        win.box()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_GREEN)
        win.addstr(1, 2, 'TUPU jenkins commands configs')
        win.refresh()

        job_items = []

        for job in jobs:
            job_items.append((job,
                              "%s/jobs/%s/config.xml" %
                              (jenkinsdir, job)))

        while True:
            jobs_menu = JobsMenu(job_items, self.screen)
            jobs_menu.display()

if __name__ == '__main__':
    try:
        curses.wrapper(JenkinsConf, '/home/paweber/.jenkins')
    except KeyboardInterrupt:
        print('Quit')
