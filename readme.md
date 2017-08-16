# Laravel Opener - Sublime Text 3 plugin
Open view files and named routes quickly.

## Prerequisites

1. Sublime Text 3
2. Laravel or Lumen installation
3. composer.json in the project's root directory

## Installation

### GitHub

1. Change to your Sublime Text `Packages` directory
2. Clone repository `git clone https://github.com/pszucs/LaravelOpener.git 'LaravelOpener'`

### Manual installation

1. Download the latest [stable release](https://github.com/pszucs/LaravelOpener/releases)
2. Unzip the archive to your Sublime Text `Packages` directory

## Setup
1. Add the project's root directory to the project's config file `Sublime -> Project -> Edit project`:
    ```js
    "laravel_opener_project_root": "your_app_root"
    ```
    > this is to help determine which directory to work in if you have multiple directories added to the project
2. Open `Packages / LaravelOpener / LaravelOpener.sublime-settings` and change these if necessary
3. Add / replace the key combination in `Sublime -> Preferences -> Key Bindings` to trigger the plugin:
    ```js
    {"keys": ["ctrl+shift+o"], "command": "laravel_opener" }
    ```

## Usage
### View files
1. Place the cursor in the source file where the link to the view file is.
    ```php
    return view('user.edit.permissions', compact('user', 'roles'));
    ```
2. Press the key combination (default: `ctrl+shift+o`)
    > if the view file doesn't exist and you save the file it will be saved in the appropriate directory
### Named routes
1. Place the cursor in the source file where the link to the route is.
    ```php
    {{ route("createUser") }}
    ```
2. Press the key combination (default: `ctrl+shift+o`)

#### Disclaimer
I'm not a Python programmer.

### To-dos
o handle controllers that are in sub-directories