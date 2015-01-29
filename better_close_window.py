import sublime
import sublime_plugin

class BetterCloseWindow(sublime_plugin.WindowCommand):
    def run(self):
        # close all files
        self.window.run_command('close_all')
        # check if there are dirty views
        if any([v.is_dirty() for v in self.window.views()]):
            return
        # close the project
        self.window.run_command('close_project')
        # close the workspace
        self.window.run_command('close_workspace')
        # close the window
        self.window.run_command('close_window')