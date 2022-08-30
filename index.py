# coding: utf-8
import eel.browsers
import eel
import sys
import os


@eel.expose
def hello():
    print('hello')
    

# ChromiumのAPIキー欠落アラートの非表示
def disable_chromium_api_message():
    "https://code-examples.net/ja/q/144a85b"
    os.environ["GOOGLE_API_KEY"] = 'no'
    os.environ["GOOGLE_DEFAULT_CLIENT_ID"] = 'no'
    os.environ["GOOGLE_DEFAULT_CLIENT_SECRET "] = 'no'


# develop用起動処理
def react_run():
    disable_chromium_api_message()
    eel.init("client", ['.tsx', '.ts', '.jsx', '.js', '.html'])
    eel.start({"port": 3000}, host="localhost", port=8888, size=(1400, 850), position=(200, 200), close_callback=python_exit)


# 終了時処置
def python_exit(page, sockets):
    if not sockets:
        sys.exit()


# Eel(GUI)を表示するブラウザをChromiumに設定(Chrome未インストールPC用)
ROOT_DIR = os.path.dirname(sys.argv[0])
chrome_path = os.path.join(ROOT_DIR, 'driver/chrome-win/chrome.exe')
if os.path.exists(chrome_path):
    eel.browsers.set_path('chrome', chrome_path)

if __name__ == '__main__':
    debug_mode = 1

    if len(sys.argv) > 2:
        debug_mode = 1 if sys.argv[1] == '--develop' else 0

    if  debug_mode == 1:
        eel.init('client')
        react_run()
    else:
        eel.init('build')
        eel.start('index.html')
