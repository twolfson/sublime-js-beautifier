import subprocess
import sublime_plugin
import sublime

class JsBeautifierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Run JS Beautifer CLI scripts against current view"""
        # Load the contents of the view
        view = self.view
        content = view.substr(sublime.Region(0, view.size()))
        print content

        # TODO: Deteremine if the view is JS, CSS, or HTML

        # Invoke `js-beautifier` CLI
