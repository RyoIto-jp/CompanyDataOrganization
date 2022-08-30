# coding: utf-8
import eel.browsers
import eel
import sys
import os


@eel.expose
def python_function(val):
    print(val)  # (val + " from JavaScript")
    eel.run_js_from_python(val)  # ("result: " + val)
    time.sleep(3)


# @eel.expose
def python_exit(page, sockets):
    if not sockets:
        sys.exit()


@eel.expose
def load_labels_from_file():
    return [{"Test": 1, "name": "test"}, {"Test": 2, "name": "testman"}]


def getMembers(val):
    print(val)
    members = [x.strip() for x in val.split(",")]
    for member in members:
        if len(member) != 6:
            print('Error! ' + member + 'は不正な値です。')
            eel.pyUpdateMessage('Error! ' + member + 'は不正な値です。')
            return ''
    eel.pyUpdateMessage('')
    return members


def updateMessage(text):
    eel.pyUpdateMessage(text)


@eel.expose
def sync_js_py(val):
    print(val)
    print('called')
    pkl.pkl_dumps_loads(val, 'company_cond')
    credential = {'user': val['username'], 'pass': val['password']}
    target_date = (str(val['Year']), str(val['Month']))
    members = getMembers(val['members'])
    web_settings = {
        "credential": credential,
        "target_date": target_date,
        "members": members,
        "is_self": val['isSelf']
    }
    
    print(members)
    if members:
        company.main(web_settings, eel=eel)
        return val


@eel.expose
def load_pickle(obj_name):
    print('called load_pickle')
    result = pkl.pkl_loads(obj_name)
    # print(result)
    return result


@eel.expose
def getFileList():
    fileList = glob.glob("./result/*.csv")
    fileList = [x.replace("./result\\", "") for x in fileList]
    print(fileList)
    return fileList


@eel.expose
def getFileDatas(fileList: dict[str, str]) -> list[dict[str, str]]:
    """ファイル名一覧から全データを取得

    Args:
        fileList (dict[str, str]): ファイル名リスト

    Returns:
        list[dict[str, str]]: 行を辞書形式で1つのリストにまとめる
    """
    data = []
    for filename in fileList:
        with open('result/' + filename, encoding='utf8') as fr:
            csv_data_obj = csv.DictReader(fr, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
            csv_data_dict = [row for row in csv_data_obj]
            data.extend(csv_data_dict)
    
    return data


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
