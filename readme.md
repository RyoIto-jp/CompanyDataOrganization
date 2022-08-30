# CompanyDataOrganization



https://github.com/RyoIto-jp/CompanyDataOrganization



## Installation



Download zip

https://github.com/hrdtbs/template-create-react-app-eel



### Python

https://www.notion.so/mathworks-lic-211102-854c3b7094c845cbbdaacfb26bc7b98b#05660e71d7ea42a8a7b25aa3a9deab66

pip

```shell
python -m venv myvenv
myvenv\Scripts\activate
myvenv\scripts\python.exe -m pip install --upgrade pip
```



1. eel
   ```shell
   pip install eel
   ```

   

2. playwright
    ```shell
    pip install playwright
    
    set PLAYWRIGHT_BROWSERS_PATH=0  
    playwright install chromium  
    ```

    

3. driver設定
    以下のフォルダからchrome-winフォルダをコピーして、開発Dir直下のdriverフォルダにペースト
    `%localappdata%\ms-playwright`

    

> tips: recording
>
> playwright codegen wikipedia.org
> playwright codegen lama05:8082/fuel



### react

```shell
yarn install

rem reactサーバーの起動を確認
yarn start:js

rem build確認
yarn build:js
```



### Eel

```shell
rem reactサーバーをバインドして、Eelを起動
rem 別ターミナルで実行すること
yarn start:js
yarn start:eel

rem buildしたreactページをEelで起動
python index.py --product
```



#### index.pyカスタマイズ
```python
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

```







### フォルダ構成変更

`./` -> `web/`

https://www.luku.work/create-react-app-rename-src



```shell
yarn add -D react-app-rewired
```



ROOTに`config-overrides.js`を作成

```js
const path = require('path');
module.exports = {
  paths: function(paths, env) {
    paths.appPublic = path.resolve(__dirname, 'web/public');
    paths.appHtml = path.resolve(__dirname, 'web/public/index.html');
    paths.appIndexJs = path.resolve(__dirname, 'web/src/index.js');
    paths.appSrc = path.resolve(__dirname, 'web/src');
    paths.appBuild = path.resolve(__dirname, 'web/build');
    return paths;
  }
};
```



`package.json`を修正

```json
{
  "name": "create-react-app-with-eel",
   //...
  },
  "scripts": {
    //...
    "start": "react-app-rewired start",
    "build": "react-app-rewired build",
    //...
  },
```







eel, playwright

eel api

browser

chrome ext alart

react環境構築

デバッグモード

build

deploy







# デバッグモードの切り替え

### react 開発モード

eelを起動

```
C:\\Project\\Python\\01_Company\\[gui.py](<http://gui.py/>)
```

debug_mode は 0。2が良い？かもしれないが、起動しない。必要なら調査。

reactを起動