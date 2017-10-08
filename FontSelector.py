# This package is greatly inspired from https://packagecontrol.io/packages/FontCycler
import sublime
import sublime_plugin
import os
from random import random

class FontSelectorCommand(sublime_plugin.WindowCommand):
    def run(self, action):
        self.font_stack = self.load_fonts()

        if action == 'select':
            self.window.show_quick_panel(self.font_stack, self.on_done, on_highlight=self.on_highlighted)
        elif action == 'random':
            font = self.random_font()
            self.on_done(font)
        elif action == 'next':
            self.dir_font()
        elif action == 'prev':
            self.dir_font(False)

    def dir_font(self, direction = True):
        index = self.font_stack.index(self.get_font())
        if direction == True:
            index = self.normalize_indices(index + 1)
        else:
            index = self.normalize_indices(index - 1)

        self.on_done(index)

    def normalize_indices(self, index):
        count = len(self.font_stack) - 1
        if index > count:
            index =  0
        elif index < 0:
            index =  count

        return index

    def on_done(self, index):
        font = self.font_stack[index]
        self.set_font(font)
        self.save_settings(font)

    def on_highlighted(self, index):
        self.set_font(self.font_stack[index])

    def random_font(self):
        return int(random() * len(self.font_stack))

    def load_fonts(self):
        return self.get_font_settings().get("monospace_fonts", [])

    def set_font(self, font_name):
        self.get_pref_settings().set('font_face', font_name)

    def get_font(self):
        return self.get_pref_settings().get('font_face')

    def save_settings(self, font_name):
        sublime.save_settings('Preferences.sublime-settings')
        sublime.status_message('SetFont: ' + font_name)
        print('')
        print('[SetFont] ' +  font_name)
        print('')

    def get_font_settings(self):
        return sublime.load_settings('FontSelector.sublime-settings')

    def get_pref_settings(self):
        return sublime.load_settings('Preferences.sublime-settings')

