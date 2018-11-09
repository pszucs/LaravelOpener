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
### Open view files from the controller

#### Method 1

1. Place the cursor on the line in the source file where the link to the view file is.
    ```php
    return view('user.edit.permissions', compact('user', 'roles'));
    ```
2. Press the key combination (default: `ctrl+shift+o`)
    > if the view file doesn't exist and you save the file it will be saved in the appropriate directory

![controller_view](https://user-images.githubusercontent.com/2471046/48292738-80ea2280-e473-11e8-87e3-f1a2a87aa1d0.gif)

#### Method 2

1. Navigate to the controller method using the Command Palette - this will select/highlight the function name.
2. Press the key combination (default: `ctrl+shift+o`)

![controller_method_name_view](https://user-images.githubusercontent.com/2471046/48292731-7af44180-e473-11e8-86e2-5b87d884253a.gif)

### Open controllers from the routes file
1. Place the cursor on the line in the routes file where the controller and method is defined:
    ```php
    Route::post('upload/store_image', ['as' => 'image', 'uses' => 'FileUploadController@storeImage']);
    ```
2. Press the key combination (default: `ctrl+shift+o`) and the controller opens with the method name selected. Press the key combination again and the view file opens too.

![routes_controller_view](https://user-images.githubusercontent.com/2471046/48292743-83e51300-e473-11e8-8372-1a789a27b833.gif)

### Named routes (temporarily disabled)
1. Place the cursor in the source file where the link to the route is.
    ```php
    {{ route("createUser") }}
    ```
2. Press the key combination (default: `ctrl+shift+o`)

#### Disclaimer
I'm not a Python programmer. ;)