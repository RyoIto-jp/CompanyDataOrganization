import datetime
import csv


def getUsers():
    data = []
    with open('tmp/users.csv', encoding='sjis') as fr:
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


def updateUser(users, payload):
    with open('tmp/users.csv', 'w', encoding='sjis', newline="") as fw:
        writer = csv.DictWriter(fw, fieldnames=users[0].keys())
        writer.writeheader()
        for index, elem in enumerate(users):
            if index == payload["index"]:
                elem[payload["key"]] = payload["value"]
                elem["modified"] = datetime.datetime.now().strftime("%Y/%m/%d %H:%M") 
            writer.writerow(elem)
    return payload


def addUser(users):
    with open('tmp/users.csv', 'a', encoding='sjis', newline="") as fw:
        writer = csv.DictWriter(fw, fieldnames=users[0].keys())
        newData = {"id": "", "name": "", "created": datetime.datetime.now().strftime("%Y/%m/%d %H:%M"), "modified": ""}
        writer.writerow()
    return newData


def deleteUser(users, deleteIndex):
    with open('tmp/users.csv', 'w', encoding='sjis', newline="") as fw:
        writer = csv.DictWriter(fw, fieldnames=users[0].keys())
        writer.writeheader()
        for index, elem in enumerate(users):
            if index == deleteIndex:
                result = elem
            else:
                writer.writerow(elem)
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


if __name__ == '__main__':
    users = getUsers()
    print(users)
    result = updateUser(users, {"index": 0, "key": "name", "value": "ABC"})
