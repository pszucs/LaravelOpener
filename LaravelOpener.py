import sublime
import sublime_plugin
import os
import json
import re
from os import path
from pprint import pprint

SETTINGS_FILE = 'LaravelOpener.sublime-settings'
file_to_be_opened = ''

class LaravelOpenerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # read settings
        self.global_settings = sublime.load_settings(SETTINGS_FILE)
        self.views_folder = self.global_settings.get('views_folder')
        self.extension = self.global_settings.get('extension')
        self.project_data = sublime.active_window().project_data()
        
        if 'laravel_opener_project_root' not in self.project_data:
            sublime.message_dialog("Please add the 'laravel_opener_project_root' property to your project's config file.")
            return

        view_file = ""
        view = self.view
        window = view.window()
        fn_name = view.substr(view.sel()[0]) # selected text

        # text was selected
        if fn_name:
            fn_regions = view.find_by_selector('meta.function - meta.function.inline')
            if fn_regions:
                for fn_region in reversed(fn_regions):
                    fn_def = view.substr(view.line(fn_region.a))
                    if "function " + fn_name in fn_def:
                        fn_block = view.substr(fn_region)
                        match_obj = re.search(r'(view|make)\([\'\"]([a-zA-z0-9_\.\/]*)[\'\"]', fn_block)
                        if match_obj:
                            view_file = match_obj.group(2).replace(".", "/")
                            break
        # no selection
        else:
            # check to see if there's a view file in the current line
            line_contents = Contents.get_current_line(self.view)
            match_obj = re.search(r'(view|make|\@include)\([\'\"]([a-zA-z0-9_\.\/]*)[\'\"]', line_contents)
            if match_obj:
                view_file = match_obj.group(2).replace(".", "/")

        for folder in sublime.active_window().project_data()['folders']:
            project_folder = folder['path'].replace('\\\\', '\\')
            dirs = project_folder.split(os.sep)
            last = dirs[-1]
            
            if last == self.project_data['laravel_opener_project_root']:
                if len(view_file):
                    file_to_open = os.path.normpath(os.path.join(project_folder, self.views_folder, view_file + self.extension))
                    if os.path.isfile(file_to_open):
                        window.open_file(file_to_open)
                    else:
                        self.check_directory(os.path.normpath(os.path.join(project_folder, self.views_folder, view_file)))
                        create_view_file = sublime.ok_cancel_dialog("Create view file?", "Yes")
                        if create_view_file:
                            window.open_file(file_to_open)
                        else:
                            window.new_file()
                    return

                # was the plugin invoked from the routes file?
                route = self.parse_controller_method(Contents.get_current_line(self.view))

                if route is not False:
                    filename = os.path.normpath(os.path.join(project_folder, "app/Http/Controllers", route["controller"] + ".php"))
                    look_for = "function " + route["method"]                        
                    line = self.find_method_position(filename, look_for)
                    global file_to_be_opened
                    file_to_be_opened = filename
                    window.open_file("{0}:{1}".format(filename, line), sublime.ENCODED_POSITION)
                break

    def laravel_routes_file(self, project_folder):
        """
        Returns the path of the routes file based on the laravel/lumen version from composer.json
        """
        with open(project_folder + '/composer.json') as data_file:
            data = json.load(data_file)

        if "laravel/lumen-framework" in data["require"]:
            version = data["require"]["laravel/lumen-framework"][:3]

        if "laravel/framework" in data["require"]:
            version = data["require"]["laravel/framework"][:3]

        if version == "5.2":
            return project_folder + "/app/Http/routes.php"
        else:
            return project_folder + "/routes/web.php"

    def find_method_position(self, filename, look_for):
        """
        Return which row the method was found in
        """
        with open(filename) as myFile:
            for num, line in enumerate(myFile, 1):
                if look_for in line:
                    return num

    def parse_controller_method(self, line_contents):
        """
        Gets the controller and method name from the line
        """
        match_obj = re.search(r'\'([\d\w]*)\@([\d\w]*)\'', line_contents)
        if match_obj:
            return {
                "controller": match_obj.group(1),
                "method": match_obj.group(2)
            }
        return False

    def find_in_routes_file(self, laravel_routes_file, route_name):
        """
        Find route_name in laravel_routes_file - not in use, to be added later
        """
        for line in open(laravel_routes_file):
            line = line.replace(" ", "")
            route_name1 = "'as'=>'" + route_name + "'"
            route_name2 = '"as"=>"' + route_name + '"'
            route_name3 = '->name("' + route_name
            route_name4 = "->name('" + route_name
            if route_name1 in line or route_name2 in line or route_name3 in line or route_name4 in line:
                return line

        return False

    def check_directory(self, new_path):
        """
        Create the directory if it doesn't exist
        """
        directory = path.dirname(new_path)
        if not path.exists(directory):
            os.makedirs(directory)

class Contents():
    def get_current_line(view):
        """
        Returns the contents of the line where the cursor is
        """
        region = view.sel()[0].begin()
        line = view.line(region)
        return view.substr(line)

class LaravelOpenerEventListener(sublime_plugin.EventListener):
    def on_load_async(self, view):
        """
        Listen to the event when a file opening is complete.
        Select the method name so that the plugin can be executed again.
        """

        # if this is not the file that was intented to be opened by the plugin, exit early
        if view.file_name() != file_to_be_opened:
            return

        line_contents = Contents.get_current_line(view)

        region = view.sel()[0].begin()  # sel() returns Selection (reference to the selection)
        line = view.line(region)

        pos1 = line.a + line_contents.find("function") + 9
        pos2 = line.a +line_contents.find("(")

        view.sel().clear()
        view.sel().add(sublime.Region(pos1, pos2))
        view.show(pos1)