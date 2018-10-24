from urllib.request import urlopen
from json import loads, dumps
import os

json_raw_path = "./tabview/templates/tabview/order_list.json"

alts = loads(urlopen("https://job.firstvds.ru/alternatives.json").read()).get("alternatives")
stor = loads(urlopen("https://job.firstvds.ru/spares.json").read())
order_list = {}


def _check_alts(alts, stor):
    '''Пересчитывает позиции по списку аналогов.
    '''
    for k in alts.keys():
        cnt, arr, mbe = 0, 0, 0 # init counters
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
    '''Пересчитывает недостающие по всему списку.
    '''
    for k in stor.keys():
        item = stor.get(k)
        cnt = item.get("count") 
        arr = item.get("arrive")
        mbe = item.get("mustbe")
        if (cnt + arr < mbe):
            order_list[k] = mbe - (arr + cnt)
    
    return order_list


def order_dump_to_json(order_list):
    '''Сохраняет спецификацию для заказа в json-файл.
    '''
    order_list = dict({"order_list": order_list})      
    with open(os.path.normpath(json_raw_path), mode="w") as f:
        f.write(dumps(order_list, sort_keys=True, indent=4))


def build_html_table(stor, order_list):
    ''' Строит html-таблицу для отчета из готовых данных.
    '''
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


def get_html_result_table():
    '''Готовит данные для отчета, json-файл для заказа
    и выдает таблицу для отображения на странице.'''
    # Проверяем список замены
    _check_alts(alts, stor)
    
    # Строим список для закупки
    order_list = _build_order_list(stor)
    # Сохраняем в json-файл
    order_dump_to_json(order_list)
    
    return build_html_table(stor, order_list)

'''#Главная функция для отдельного запуска
def main(alts, stor, order_list):
    # Проверяем список аналогов
    _check_alts(alts, stor)
    # Пересчитываем все недостающие
    order_list = _build_order_list(stor)
    # Сохраняем для заказа в json
    order_dump_to_json(order_list)
    # Сохраняем таблицу для вставки в html-файл
    with open("http_table", mode="w") as f:
        f.write(build_html_table(stor, order_list))
'''

if (__name__ == "__main__"):
    #main(alts, stor, order_list)
    print("Only as module using allowed.")
