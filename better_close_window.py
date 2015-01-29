import sublime
import sublime_plugin
import json
import re
import os


def project_file_name(window):
    """
    by titoBouzout, author of SideBarEnhancements
    https://github.com/titoBouzout/SideBarEnhancements
    """
    if int(sublime.version()) > 3000:
        return window.project_file_name()

    # for sublime text 2, try to guess it from sublime_session
    if not window.folders():
        return None

    session = os.path.normpath(os.path.join(sublime.packages_path(), '..',
                               'Settings', 'Session.sublime_session'))
    auto_session = os.path.join(sublime.packages_path(), '..',
                                'Settings', 'Auto Save Session.sublime_session')
    data = open(session, 'r').read()
    data = data.replace('\t', ' ')
    data = json.loads(data, strict=False)
    projects = data['workspaces']['recent_workspaces']

    if os.path.lexists(auto_session):
        data = open(auto_session, 'r').read()
        data = data.replace('\t', ' ')
        data = json.loads(data, strict=False)
        if hasattr(data, 'workspaces') and hasattr(data['workspaces'], 'recent_workspaces') \
                and data['workspaces']['recent_workspaces']:
            projects += data['workspaces']['recent_workspaces']
        projects = list(set(projects))
    for project_file in projects:
        project_file = re.sub(r'^/([^/])/', '\\1:/', project_file)
        if os.path.lexists(project_file):
            project_json = json.loads(open(project_file, 'r').read(), strict=False)
            if 'folders' in project_json:
                folders = project_json['folders']
                for directory in window.folders():
                    for folder in folders:
                        folder_path = re.sub(r'^/([^/])/', '\\1:/', folder['path'])
                        if folder_path == directory.replace('\\', '/'):
                            return project_file
    return None


class BetterCloseWindow(sublime_plugin.WindowCommand):
    def run(self):
        # if it is a project, close the project
        if project_file_name(self.window):
            if int(sublime.version()) >= 3000:
                self.window.run_command('close_workspace')
            else:
                self.window.run_command('close_project')

        self.window.run_command('close_all')
        # exit if there are dirty views
        if any([v.is_dirty() for v in self.window.views()]):
            return

        # close the sidebar
        if int(sublime.version()) >= 3000:
            self.window.run_command('close_project')
        else:
            self.window.run_command('close_folder_list')

        # close the window
        self.window.run_command('close_window')
