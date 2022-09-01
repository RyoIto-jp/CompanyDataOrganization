import eel
from . import pickle_obj as pkl
from . import company
import glob
import time
import csv


@eel.expose
def python_function(val):
    print(val)  # (val + " from JavaScript")
    eel.run_js_from_python(val)  # ("result: " + val)
    time.sleep(3)


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
def py_download_company(val):
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
            csv_data_obj = csv.DictReader(
                fr,
                delimiter=",",
                doublequote=True,
                lineterminator="\r\n",
                quotechar='"',
                skipinitialspace=True)
            csv_data_dict = [row for row in csv_data_obj]
            data.extend(csv_data_dict)

    return data


@eel.expose
def hello():
    print('hello')
