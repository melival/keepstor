from urllib.request import urlopen
from json import loads, dumps, dump

alts = loads(urlopen("https://job.firstvds.ru/alternatives.json").read()).get("alternatives")
stor = loads(urlopen("https://job.firstvds.ru/spares.json").read())
order_list = {}

def _check_alts(alts, stor):
    for k in alts.keys(): # check with alternatives first
        cnt, arr, mbe = 0, 0, 0
        for i in alts.get(k):
            item = stor.get(i)
            if (i in stor.keys()):
                stor.pop(i)
            else:
                continue
            cnt += item.get("count") 
            arr += item.get("arrive")
            mbe = mbe if (mbe > item.get("mustbe")) else item.get("mustbe")
        stor[k] = {'count': cnt, 'mustbe': mbe, 'arrive': arr}
        if (cnt + arr < mbe):
            order_list[k] = mbe - arr - cnt


def _build_order_list(stor):
    for k in stor.keys(): # check all list
        item = stor.get(k)
        cnt = item.get("count") 
        arr = item.get("arrive")
        mbe = item.get("mustbe")
        if (cnt + arr < mbe):
            order_list[k] = mbe - (arr + cnt)
    
    return order_list


def _print_list(stor, order_list):           
    for k in stor.keys():
        item = stor.get(k)
        c = item.get("count")
        a = item.get("arrive")
        m = item.get("mustbe")
        print("!!! " if k in order_list.keys() else "", k,
            " : we have:", c, " wait for:", a, " need:", m)


def order_dump_to_json(order_list):
    print("Order list:")
    order_list = dict({"order_list": order_list})      
    #print(dumps(order_list, sort_keys=True, indent=4)) #if need pretty out
    print(dumps(order_list)) #if need just a string
    with open("order_list.json", mode="w") as f:
        f.write(dumps(order_list, sort_keys=True, indent=4))

def build_http_table(stor, order_list):
    # Create a html table
    result = "<table>\n"
    result += "<tr><td>Description</td><td>Count</td><td>Arrive</td><td>Must be</td></tr>\n"
    td = "</td><td>"
    
    for k in stor.keys():
        item = stor.get(k)
        c = str(item.get("count"))
        a = str(item.get("arrive"))
        m = str(item.get("mustbe"))
        row_color = " bgcolor=\"red\"" if k in order_list.keys() else ""
        result += "".join(["<tr", row_color, "><td>", k, td, c, td, a, td, m, "</td></tr>", "\n"])

    result += "</table>\n"
    return result


def get_http_result_table():
    # Проверяем список замены
    _check_alts(alts, stor)
    
    # Строим список для закупки
    order_list = _build_order_list(stor)
    
    # Печатаем таблицу по наличию
    #_print_list(stor, order_list)
    
    # Сохраняем список для закупки в json-файл
    order_dump_to_json(order_list)
    
    return build_http_table(stor, order_list)


def main(alts, stor, order_list):
    # Проверяем список замены
    _check_alts(alts, stor)
    
    # Строим список для закупки
    order_list = _build_order_list(stor)
    
    # Печатаем таблицу по наличию
    #_print_list(stor, order_list)
    
    # Сохраняем список для закупки в json-файл
    order_dump_to_json(order_list)
    with open("http_table", mode="w") as f:
        f.write(build_http_table(stor, order_list))


if (__name__ == "__main__"):
    main(alts, stor, order_list)