from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

import glob
import os
import subprocess

class SublProjectsExtension(Extension):
    def __init__(self):
        super(SublProjectsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        sublime_path = os.path.expanduser(extension.preferences['sublime_projects_dir'])
        items = []
        for name in glob.glob(sublime_path + "/*.sublime-project"):
            project_name = name.split('/').pop().replace('.sublime-project', '').replace('-', ' ').title()
            item = ExtensionResultItem(
                icon = 'images/icon.png',
                name = project_name,
                description = 'Path: %s' % name,
                on_enter = ExtensionCustomAction(name)
            )
            items.append(item)

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        project_path = event.get_data()
        subl = extension.preferences['sublime_executable']
        subprocess.call([subl, "--project", project_path, "-n"])

if __name__ == '__main__':
    SublProjectsExtension().run()