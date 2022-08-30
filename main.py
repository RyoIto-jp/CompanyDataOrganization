from src import company
import gui
import argparse
import datetime
import msvcrt
import sys
import os


def app_cli():
    """DEBUG用 CLIで動作確認"""

    # 2. パーサを作る
    parser = argparse.ArgumentParser(description='Companyデータ整理補助ツール')

    # 3. parser.add_argumentで受け取る引数を追加していく # required=True,で必須指定
    parser.add_argument('-M', '--mode', help='実行モードを選択 cli, gui(他の引数は無視されます)')
    parser.add_argument('-u', '--USER', required=False, help='認証ユーザーID(例: 608409)')
    parser.add_argument('-p', '--PASS', required=False, help='認証ユーザーPW(例: abcde)※env有効時は無効化されます')
    parser.add_argument('-x', '--env', action='store_true', help='認証ユーザーPWを環境変数OST_PWから取得')
    parser.add_argument('-m', '--member', help='対象ユーザをリストで渡す(例: 608409,608410)')
    parser.add_argument('-d', '--date', default=datetime.datetime.now().strftime('%Y,%m'), help='対象年月を指定(例: 2022,2)')

    # 4. 引数を解析
    args = parser.parse_args()

    # 引数をコンソール出力
    # pp(vars(args))

    # GUIモード判定
    if args.mode == 'GUI' or args.mode == 'gui':
        print('GUIモードで実行します')
        gui.run()
        return
    
    if args.USER is None or args.PASS is None:
        print("\n認証情報が入力されていません。USER | PASS")
        os.system('pause')
        sys.exit()
    
    if args.env:
        print('環境変数からパスワードを抽出')
        user_pw = os.environ.get("OST_PW")
        if not user_pw:
            print("\n環境変数 OST_PW が存在しません。")
            os.system('pause')
            sys.exit()
    else:
        user_pw = args.PASS

    if not args.member:
        print("\n対象ユーザーが入力されていません。member")
        os.system('pause')
        sys.exit()
    else:
        members = [x.strip() for x in args.member.split(",")]
        for member in members:
            if len(member) != 6:
                print('Error! ' + member + 'は不正な値です。')
                os.system('pause')
                sys.exit()
    
    try:
        target_date = tuple([str(int(d.strip())) for d in args.date.split(",")])
    except Exception:
        print('\n対象年月が不正です。')
        os.system('pause')
        sys.exit()

    credential = {'user': args.USER, 'pass': user_pw}

    # print(target_date)
    web_settings = {
        "credential": credential, "target_date": target_date, "members": members
    }
    company.main(web_settings)


def secure_password_input(prompt=''):
    p_s = ''
    proxy_string = [' '] * 64
    while True:
        sys.stdout.write('\x0D' + prompt + ''.join(proxy_string))
        c = msvcrt.getch()
        if c == b'\r':
            break
        elif c == b'\x08':
            p_s = p_s[:-1]
            proxy_string[len(p_s)] = " "
        else:
            proxy_string[len(p_s)] = "*"
            p_s += c.decode()

    sys.stdout.write('\n')
    return p_s


def input_year():
    dt_year = input("対象年を入力してください(数値4桁) : ")
    if len(dt_year) != 4:
        print('対象年が不正です。')
        dt_year = input_year()
    else:
        try:
            if int(dt_year) < 2000 or int(dt_year) >= 2099:
                print('対象年が不正です。')
                dt_year = input_year()
        except Exception:
            print('対象年が不正です。')
            dt_year = input_year()
    return str(int(dt_year))


def input_month():
    dt_month = input("対象月を入力してください(数値1~2桁) : ")
    if len(dt_month) > 2:
        print('対象月が不正です。')
        dt_month = input_month()
    else:
        try:
            if int(dt_month) < 1 or int(dt_month) >= 13:
                print('対象月が不正です。')
                dt_month = input_month()
        except Exception:
            print('対象月が不正です。')
            dt_month = input_month()
    return str(int(dt_month))


def input_members():
    print('対象メンバーの社員番号を入力してください。')
    print('カンマ区切りで複数選択が可能です')
    members_raw = input(" 入力: ")
    members = [x.strip() for x in members_raw.split(",")]
    for member in members:
        if len(member) != 6:
            print('Error! ' + member + 'は不正な値です。')
            members = input_members()
    return members


def wizard_mode():
    gui_mode = input("GUIモードで実行しますか？(y/n) : ")
    if gui_mode == 'y':
        gui.run()
        return
    else:
        print('\nウィザード形式で実行します')
        user_id = input("ユーザーIDを入力してください : ")
        user_pw = secure_password_input("ユーザーPWを入力してください : ")
        dt_year = input_year()
        dt_month = input_month()

        print(user_id)
        print(dt_year, dt_month)
        credential = {'user': user_id, 'pass': user_pw}
        target_date = (dt_year, dt_month)
        members = input_members()
        print(members)
        web_settings = {
            "credential": credential, "target_date": target_date, "members": members
        }
        company.main(web_settings)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app_cli()
    else:
        print("実行引数が存在しないためウィザードモードで実行します。")
        print("詳細は、「python main.py --help」 で確認してください。\n")
        wizard_mode()
