import subprocess
import sublime_plugin
import sublime

class JsBeautifierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Run JS Beautifer CLI scripts against current view"""
        # Load the contents of the view
        view = self.view
        content = view.substr(sublime.Region(0, view.size()))

        # TODO: Deteremine if the view is JS, CSS, or HTML
        # https://github.com/einars/js-beautify/blob/v1.4.2/index.html#L245-L269

        # Invoke `js-beautifier` CLI
        child = subprocess.Popen(['js-beautify', '--file', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        child.communicate(input=content)
        # child.terminate()
        # child.wait()
        print child.stdout
