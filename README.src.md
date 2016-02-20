[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
# AoikClose
A Sublime Text plugin to close tabs (a.k.a views) in various ways:
- Close Active Tab
- Close Tabs to the Left
- Close Tabs to the Right
- Close Other Tabs
- Close All Tabs

Tested working with:
- Sublime Text 2
- Sublime Text 3

## Table of Contents
[:toc(beg='next', indent=-1)]

## Setup

### Setup via git
Clone this repository to Sublime Text's **Packages** directory (Preferences - Browse Packages...):
```
git clone https://github.com/AoiKuiyuyou/AoikClose-SublimeText AoikClose
```

Make sure the repository directory is renamed to **AoikClose**
(without the "-SublimeText" postfix), otherwise it may not work well.

## Usage

### Run via Console Panel
Open "View - Show Console (Ctrl+Shift+C)", run:
```
window.run_command('aoik_close', { "mode": "active", "force": False })

window.run_command('aoik_close', { "mode": "left", "force": False })

window.run_command('aoik_close', { "mode": "right", "force": False })

window.run_command('aoik_close', { "mode": "other", "force": False })

window.run_command('aoik_close', { "mode": "all", "force": False })
```

### Run via Context Menu
Open "Preferences - Package Settings - AoikClose - Tab Context.sublime-menu (Example)",
copy the content to your "Packages/User/Tab Context.sublime-menu" file. Then
right click a tab to show the context menu and select a command to run.
