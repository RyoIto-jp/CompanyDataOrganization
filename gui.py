
import sys
import os

import eel.browsers
import eel

from src import find_browser
from src import func_eel
print(func_eel)
# from src.func_eel import *


def disable_chromium_api_message():
    """ ChromiumのAPIキー欠落アラートの非表示
    https://code-examples.net/ja/q/144a85b"""
    os.environ["GOOGLE_API_KEY"] = 'no'
    os.environ["GOOGLE_DEFAULT_CLIENT_ID"] = 'no'
    os.environ["GOOGLE_DEFAULT_CLIENT_SECRET "] = 'no'


def react_run():
    # develop用起動処理
    eel.init("web", ['.tsx', '.ts', '.jsx', '.js', '.html'])
    eel.start({"port": 3000}, host="localhost", port=8888, size=(
        1400, 850), position=(200, 200), close_callback=python_exit)


# 終了時処置
def python_exit(page, sockets):
    if not sockets:
        # sys.exit()
        pass


def setChromePath(useDriver=False):
    """Eel(GUI)を表示するブラウザをChromiumに設定

    Returns:
        str: Path to chrome.exe
    """
    chrome_path = find_browser.findBrowserPath('chrome')
    if chrome_path == "" or useDriver:
        print('use the downloaded webDriver')
        ROOT_DIR = os.path.dirname(sys.argv[0])
        chrome_path = os.path.join(ROOT_DIR, 'driver/chrome-win/chrome.exe')

    if os.path.exists(chrome_path):
        eel.browsers.set_path('chrome', chrome_path)
    return chrome_path


disable_chromium_api_message()
setChromePath()  # Eel(GUI)を表示するブラウザをChromiumに設定(Chrome未インストールPC用)


if __name__ == '__main__':
    debug_mode = 1

    if len(sys.argv) > 1:
        debug_mode = 1 if sys.argv[1] == '--develop' else 0

    if debug_mode == 1:
        eel.init('client')
        react_run()
    else:
        eel.init('web/build')
        eel.start(
            'index.html',
            port=8888,
            size=(1400, 850),
            position=(200, 200),
            close_callback=python_exit
        )
