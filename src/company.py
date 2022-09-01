from playwright.sync_api import Playwright, sync_playwright
import csv
import os


def loginCompany(page, cred):
    # Go to Company Web page
    page.goto("https://gcws3.outsourcing.co.jp/cws/cws")

    # Authorize
    page.locator("input[name=\"uid\"]").fill(cred["user"])
    page.locator("input[name=\"pwd\"]").fill(cred["pass"])
    page.locator("input[alt=\"login\"]").press("Enter")
    
    loginStatus = False
    if page.title() == 'メインメニュー':
        loginStatus = True
    return page, loginStatus


def moveToApprovalPage(page):
    # 就労管理/上長用メニュー/勤務実績承認（期間承認用）
    page.locator("text=就労管理").click()
    page.locator("a:has-text(\"上長用メニュー\")").click()
    page.locator("text=勤務実績承認（期間承認用）").click()
    return page


def navMyPage(page, target_date):
    page.locator("text=就労管理").click()
    page.click("a:has-text('勤務実績入力（期間入力用）')")

    while True:
        buf = page.locator('span.sp_kintai_kikan').text_content()
        now_date = buf[0:4] + ('00' + buf[5:buf.find("月\xa0")])[-2:]
        target = target_date[0] + ('00' + target_date[1])[-2:]
        if target == now_date:
            break
        elif target < now_date:
            page.locator("#TOPRVTM").click()  # go to previous month
        elif target > now_date:
            page.locator("#TONXTTM").click()
        else:
            print('不正な値です')
            os.system('pause')

    page.wait_for_load_state("load")
    empName = page.locator('.syain > div:nth-child(2)').text_content().replace('社員名称：\xa0', '').replace('\u3000', ' ')
    header_text = page.query_selector("form[name=\"FormListPersonalDetails\"]").text_content()

    reportStatus = getReportStatus(header_text)

    return page, empName, reportStatus


def navMemberPage(page, target_date, empNum):
    # fill condition values
    page.locator("input[name=\"\\@PSTDDATEYEAR\"]").fill(target_date[0])
    page.locator("select[name=\"\\@PSTDDATEMONTH\"]").select_option(target_date[1])
    page.locator("select[name=\"\\@PSTDDATEDAY\"]").select_option("1")
    page.locator("input[name=\"emps_cond\"]").fill(empNum)

    # 検索処理の実行 ：個人ごとの期間合計を表示
    with page.expect_navigation():
        page.locator("text=個人ごとの期間合計を表示").click()

    # Get a employee Name
    empName = page.locator("#EmpNm1").text_content().replace("\u3000", ' ')

    # todo: 提出状況
    reportStatus = page.locator("#flowinfo1").text_content().replace("\u3000", ' ')
    print(reportStatus)

    # Click input:has-text("詳細")
    page.locator("input:has-text(\"詳細\")").click()
    return page, empName, reportStatus


def navPrintPage(page):
    with page.expect_event("popup") as page_info:
        page.locator("input[name=\"btnPrint\"]").click()
    popup = page_info.value

    # Get a table html
    popup.wait_for_load_state("domcontentloaded")
    return popup


def getReportStatus(header_text):
    choices = {
        "この期間の勤務データはまだ月次提出": "状態：未入力",
        "この期間の勤務データは既に提出され": "第１段階の承認待ち",
        "この期間の実績はすでに承認済です。": "最終承認済み"
    }
    for choice in choices:
        if choice in header_text:
            return choices[choice]
            break
    
    return "empty"


def getStatus(class_name):
    if class_name == 'mg_normal':
        return '未提出'
    elif class_name == 'mg_saved':
        return '一時保存'
    elif class_name == 'mg_dc_saved':
        return '日次提出'
    elif class_name == 'mg_confirmed':
        return '-'
    else:
        return ''


def getTable(popup, target_year):
    table_rows = popup.query_selector_all("table[name=\"APPROVALGRD\"] > tbody > tr")

    # initialize
    result_row = {}
    result = []

    for row in table_rows[1:]:
        tempWork = row.query_selector("td:nth-child(3)")
        # 提出状況
        rowStatus = getStatus(tempWork.get_attribute('class'))
        # 業務区分
        rowWork = tempWork.text_content()

        # 日付
        tempDate = row.query_selector("td >> nth=0")
        # 日付がない行は処理をしない
        if tempDate.query_selector("#MONTH"):
            targetDate = target_year + '-' + tempDate.query_selector("#MONTH").text_content() + '-' + tempDate.query_selector("#DAY").text_content()
            print(targetDate)

        # project code
        # time, code, name: 35-000
        tempProjects = row.query_selector("td:nth-child(32) > table:nth-child(1) > tbody")
        comment_idx = 35
        resPrj = ""

        # ProjectCode列にTableなし時はスキップ。
        if not tempProjects:
            tempProjects = row.query_selector("td:nth-child(14) > table:nth-child(1) > tbody")
            comment_idx = 15
            if not tempProjects:
                continue

        # 各行の1列目のデータが35-000なら取得。
        for prj in tempProjects.query_selector_all("tr"):
            resPrj = prj.query_selector("td:nth-child(3)").text_content()[1:-1]
            result_row["date"] = targetDate
            result_row["work"] = rowWork
            result_row['status'] = rowStatus
            result_row["times"] = resPrj
            result_row["type"] = prj.query_selector("td:nth-child(2)").text_content()

            # データが存在しなければこの行はスキップ。
            if resPrj == "":
                continue

            # 備考欄を取得
            tempComment = row.query_selector(f"td:nth-child({comment_idx})").text_content().replace('\xa0', '')
            result_row["comment"] = tempComment

            # 取得結果をresultに格納
            result.append(result_row)
            result_row = {}
    return result


def exportCSV(result, empNum, empName, target_date):
    # [2012, 5] -> 1205
    file_name_date = target_date[0][2:] + ('00' + target_date[1])[-2:]
    # CSVに出力
    try:
        with open(f'result/company_{file_name_date}_{empNum}.csv', 'w', encoding='utf8', newline="") as f:
            if result:
                writer = csv.DictWriter(f, fieldnames=result[0].keys())
                writer.writeheader()
                for elem in result:
                    writer.writerow(elem)
            else:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(["date", "times", "comment", "Name", "Num"])
                writer.writerow(["2/1", 0, "DataISEmpty", empName, empNum])
                print("DataISEmpty: ", f"{empNum}:{empName}")
    except IOError:
        print("I/O error")


def getUserWorkTime(page, empNum, empName, reportStatus, target_date):
    # 印刷用ページを開く
    popup = navPrintPage(page)

    # テーブル情報を取得
    result = getTable(popup, target_year=target_date[0])

    # 結果を整形
    result = [{**row, "Name": empName, "Num": empNum, "Report": reportStatus} for row in result]

    # 結果をCSV出力
    exportCSV(result, empNum, empName, target_date)

    popup.close()
    # todo


def run(playwright: Playwright, web_settings: dict, eel) -> None:
    credential = web_settings["credential"]
    target_date = web_settings["target_date"]
    members = web_settings["members"]
    is_self = web_settings.get("is_self")

    print("start playwright...")
    browser = playwright.chromium.launch(
        headless=True,  # ! DEBUG
        executable_path="./driver/chrome-win/chrome.exe")
    context = browser.new_context()

    # Test Eel
    if eel:
        eel.pyUpdateMessage("browserを起動")

    # Open new page
    page = context.new_page()

    # Login to Company
    page, loginStatus = loginCompany(page, credential)
    
    if not loginStatus:
        if eel:
            eel.pyUpdateMessage("ログインに失敗しました。処理を中断します。")
    
    else:
        if eel:
            eel.pyUpdateMessage("Company認証完了")

        # getWorkTimeMe
        if is_self:
            # todo: 月度移動
            page, empName, reportStatus = navMyPage(page, target_date)
            if eel:
                eel.pyUpdateMessage(f"{empName}の処理を実行中")
            # 工数CSVを取得
            getUserWorkTime(page, credential['user'], empName, reportStatus, target_date)
            page.locator('.globalnavi > div:nth-child(1) > a').click()
            print('complete my worktime')

        # Go to the Company Approval Page
        page = moveToApprovalPage(page)

        for i, empNum in enumerate(members):
            page, empName, reportStatus = navMemberPage(page, target_date, empNum)

            if eel:
                eel.pyUpdateMessage(f"{empName}の処理を実行中 {i + 1}/{len(members)}")

            # 工数CSVを取得
            getUserWorkTime(page, empNum, empName, reportStatus, target_date)
            page.query_selector('#BTNBCK0').click()

        if eel:
            eel.pyUpdateMessage("処理が完了しました")
            print("処理が完了しました")

        context.close()
        browser.close()


def main(web_settings: dict, eel=None):
    with sync_playwright() as playwright:
        run(playwright, web_settings, eel)


if __name__ == '__main__':
    # Companyの認証情報を設定
    credential = {"user": "608409", "pass": os.environ.get("OST_PW")}

    # 取得したい社員番号リストを設定
    EmployeeNumbers = [
        "618329",
        "611606",
        # "629576", "319794",
        # "611646", "611674", "618679", "629576", "629588", "629600", "629606"
    ]

    # 対象月度を設定
    target_date = ("2021", "12")

    # parameter
    web_settings = {
        "credential": credential,
        "target_date": target_date,
        "members": EmployeeNumbers,
        "is_self": True
    }

    # メイン処理を実行
    main(web_settings)
