import sublime
import sublime_plugin

class BetterCloseWindow(sublime_plugin.WindowCommand):
    def run(self):
        # if it is a project, close the project
        if self.window.project_file_name():
            # close the workspace
            self.window.run_command('close_workspace')
        else:
            self.window.run_command('close_all')
            # check if there are dirty views
            if any([v.is_dirty() for v in self.window.views()]):
                return
            # close the sidebar
            self.window.run_command('close_project')
        # close the window
        self.window.run_command('close_window')