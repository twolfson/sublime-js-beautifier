import re
import subprocess
import sublime_plugin
import sublime

class JsBeautifierCommand(sublime_plugin.TextCommand):
    @classmethod
    def looks_likes_html(cls, source):
        """Determine if a code block looks like HTML

        https://github.com/einars/js-beautify/blob/v1.4.2/index.html#L262-L269
            <foo> - looks like html
            <!--\nalert('foo!');\n--> - doesn't look like html
        """
        # In JS, we only replace the first item (not a global regexp)
        trimmed = re.sub(r'^[ \t\n\r]+', '', source, count=1)
        comment_mark = '<' + '!-' + '-'
        return (trimmed and (trimmed[:1] == '<' and trimmed[:4] != comment_mark))

    def run(self, edit):
        """Run JS Beautifer CLI scripts against current view"""
        # Load the contents of the view
        view = self.view
        all_text = sublime.Region(0, view.size())
        content = view.substr(all_text)

        # Deteremine if the view is JS, CSS, or HTML
        # TODO: Leverage syntax
        # Otherwise, use sniffing from JS Beautifier source
        # https://github.com/einars/js-beautify/blob/v1.4.2/index.html#L245-L269
        content_type = 'html' if self.looks_likes_html(content) else 'js'

        # Invoke `js-beautifier` CLI
        child = subprocess.Popen(['js-beautify', '--type', content_type, '--file', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # TODO: Figure out better solution to encoding since Linux !== Windows
        # http://stackoverflow.com/questions/3810302/python-unicode-popen-or-popen-error-reading-unicode
        child.stdin.write(content.encode('cp437'))
        child.stdin.close()
        child.wait()
        beautified_content = child.stdout.read()

        # Overwrite the current content
        view.replace(edit, all_text, beautified_content)
        view.end_edit(edit)
