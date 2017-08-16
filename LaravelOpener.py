import sublime
import sublime_plugin
import os
import json
import re
from os import path
from pprint import pprint

"""
Add "laravel_opener_project_root": "bikes" to project settings (sublime)
"""

class LaravelOpenerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        window = view.window()
        folders = window.folders()
        region = view.sel()[0].begin()
        line = view.line(region)
        line_contents = view.substr(line)

        # read settings
        global_settings = sublime.load_settings('LaravelOpener.sublime-settings')
        views_folder = global_settings.get('views_folder')
        extension = global_settings.get('extension')

        view_file = self.get_view_file(line_contents)
        project_data = sublime.active_window().project_data()

        if 'laravel_opener_project_root' not in project_data:
            sublime.message_dialog("Please add the 'laravel_opener_project_root' property to your project's config file.")
            return

        project_root = project_data['laravel_opener_project_root']
        
        file_to_open = None
        named_route_found = False

        for folder in sublime.active_window().project_data()['folders']:
            project_folder = folder['path']
            dirs = project_folder.split('/')
            last = dirs[-1]
            
            if last == project_root:
                file_to_open = project_folder + "/" + views_folder + "/" + view_file + extension
                
                # is it a route name?
                laravel_routes_file = self.laravel_routes_file(project_folder)
                route_line = self.find_in_routes_file(laravel_routes_file, view_file)

                if route_line is not False:
                    choice = sublime.ok_cancel_dialog("Named route found.", "Go to definition")
                    
                    if choice is True:
                        named_route_found = True

                break

        if named_route_found is True:
            route = self.get_controller_and_method(route_line)
            filename = project_folder + "/app/Http/Controllers/" + route["controller"] + ".php"
            look_for = "function " + route["method"]
            
            line = self.find_method_position(filename, look_for)
            window.open_file("{0}:{1}:{2}".format(filename, line, 0), sublime.ENCODED_POSITION)

        else:
            if file_to_open is None:
                sublime.message_dialog("Make sure the project root is set in the config file!")
                return

            if os.path.isfile(file_to_open):
                window.open_file(file_to_open)
            else:
                self.check_directory(project_folder + "/" + views_folder + "/" + view_file)
                create_view_file = sublime.ok_cancel_dialog("Create view file?", "Yes")
                if create_view_file:
                    window.open_file(file_to_open)
                else:
                    window.new_file()
    
    def get_view_file(self, line_contents):
        """
        Return the relative path and the basename of the file intented to open
        """
        view_file = self.find_between(line_contents, "('", "')-")
        if view_file == "":
            view_file = self.find_between(line_contents, '("', '")-')
        if view_file == "":
            view_file = self.find_between(line_contents, "('", "',")
        if view_file == "":
            view_file = self.find_between(line_contents, '("', '",')
        if view_file == "":
            view_file = self.find_between(line_contents, "('", "')")
        if view_file == "":
            view_file = self.find_between(line_contents, '("', '")')
        if view_file == "":
            view_file = self.find_between(line_contents, "'", "'")
        if view_file == "":
            view_file = self.find_between(line_contents, '@view ', ' ')

        return view_file.replace(".", "/")

    def find_between(self, s, first, last=None):
        """
        Returns the string found between first and last
        """
        try:
            start = s.index(first) + len(first)
            if last is None:
                end = 0
            else:
                end = s.index(last, start)

            return s[start:end]
        except ValueError:
            return ""

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

    def find_in_routes_file(self, laravel_routes_file, route_name):
        """
        Find route_name in laravel_routes_file
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

    def get_controller_and_method(self, route_line):
        """
        @todo: controllers can be organised into sub-directories
        """
        s = route_line.replace(' ', '').split(',')[-1].split("@")

        if "->name" in route_line:
            controller = re.sub(r'\W+', '', s[0])
            method = re.sub(r'\W+', '', self.find_between(route_line, "@", ")->name("))
        else:
            method = s[1]
            method = re.sub(r'\W+', '', method)

            controller = s[0].split("=>")[1]
            controller = re.sub(r'\W+', '', controller)

        return {
            "controller": controller,
            "method": method
        }

    def check_directory(self, new_path):
        directory = path.dirname(new_path)
        print("directory: " + directory)
        if not path.exists(directory):
            os.makedirs(directory)
