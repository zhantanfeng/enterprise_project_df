"""
处理有关企业专利信息的数据库获取结果的处理
"""
import dao.enterprise_patent_dao as enterprise_patent_dao
import dao.enterprise_dao as enterprise_dao
from collections import Counter

def get_en_info_by_patent(searched_patent):
    """
    根据企业成果检索企业
    :param searched_patent:
    :return:企业信息
    """
    en_id_list = enterprise_patent_dao.get_pa_id_by_patent(searched_patent)
    en_name_list = []
    for i in en_id_list:
        en_name_list.append(enterprise_patent_dao.get_en_name_by_pa_id(i))
    result = []
    for i in en_name_list:
        result.append(enterprise_dao.get_en_info_by_name_1(i))
    return result

def get_pa_count_by_firstkind():
    """
    初始获取所有一类技术领域的专利数量
    :return:
    """
    firstkind = get_all_field()[0]
    result = []
    for i in firstkind:
        result.append([i, enterprise_patent_dao.get_count_by_firstkind(i)[0]])
    return result

def get_count_by_firstkind(field):
    """
    获取第二类的专利数量
    :param field:
    :return:
    """
    second_field = enterprise_patent_dao.get_second_field(field)
    result = []
    for i in second_field:
        result.append([i, enterprise_patent_dao.get_count_by_secondkind(i)[0]])
    return result

def get_count_by_secondkind(field):
    """
    获取第三类的专利数量
    :param field:
    :return:
    """
    third_field = enterprise_patent_dao.get_third_field(field)
    result = []
    for i in third_field:
        result.append([i, enterprise_patent_dao.get_count_by_thirdkind(i)[0]])
    return result

def get_all_field():
    """
    获取所有技术领域
    :return:
    """
    temp = enterprise_patent_dao.get_all_field()
    firstkind = []
    secondkind = []
    thirdkind = []
    for i in temp[0]:
        for j in i:
            firstkind.append(j[0])
    for i in temp[1]:
        for j in i:
            secondkind.append(j[0])
    for i in temp[2]:
        for j in i:
            thirdkind.append(j[0])
    result = [firstkind, secondkind, thirdkind]
    return result

def get_engineer_and_en_by_field(field):
    """
    根据技术领域获取工程师以及所在的公司
    :param field: 技术领域
    :return: 前10家的企业以及专利前10的工程师
    """
    temp = enterprise_patent_dao.get_engineer_and_en_by_field(field)
    en_id_list = []
    for i in temp:
        en_id_list.append(i[0])
    en_id_dict = {}
    for key in en_id_list:
        en_id_dict[key] = en_id_dict.get(key, 0) + 1
    list1 = sorted(en_id_dict.items(), key=lambda x:x[1], reverse=True)
    ten_en = []
    for i in list1[0:10]:
        ten_en.append(i[0])
    result = []
    for i in ten_en:
        temp1 = []
        for j in temp:
            if j[0] == i:
                temp1.extend(j[1].split(","))
        engineer_dict = {}
        for key in temp1:
            engineer_dict[key] = engineer_dict.get(key, 0) + 1
        engineer_list = sorted(engineer_dict.items(), key=lambda x: x[1], reverse=True)
        ten_engineer = []
        for x in engineer_list[0:10]:
            ten_engineer.append(x[0])
        if ten_engineer != ['不公告发明人']:
            result.append([ enterprise_dao.get_en_name_by_en_id(i), ten_engineer ])
    return result

def get_patent_by_first_ipc():
    """
    获取所有第一类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    all_first_ipc = enterprise_patent_dao.get_first_ipc()
    result = []
    for i in all_first_ipc:
        result.append([i[0]+":"+i[1], enterprise_patent_dao.get_patent_by_ipc(i[0])])
    return result


def get_patent_by_second_ipc(ipc_id):
    """
    获取所有第二类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    all_first_ipc = enterprise_patent_dao.get_second_ipc(ipc_id)
    result = []
    for i in all_first_ipc:
        if enterprise_patent_dao.get_patent_by_ipc(i[0])[0] != 0:
            result.append([i[0]+":"+i[1], enterprise_patent_dao.get_patent_by_ipc(i[0])[0]])
    result = sorted(result, key=lambda x:(x[1]), reverse=True)
    if len(result) > 10:
        count = 0
        for i in result[9:]:
            count = count + i[1]
        result = result[0:9]
        result.append(["其他", count])
    return result

def get_patent_by_third_ipc(ipc_id):
    """
    获取所有第二类ipc的所有专利数量
    :param ipc_id:
    :return:
    """
    all_first_ipc = enterprise_patent_dao.get_third_ipc(ipc_id)
    result = []
    for i in all_first_ipc:
        temp = i[0][4:7].replace("0","")
        if enterprise_patent_dao.get_patent_by_ipc(i[0][0:4]+temp+i[0][7:])[0] != 0:
            result.append([i[0][0:4]+temp+i[0][7:]+":"+i[1], enterprise_patent_dao.get_patent_by_ipc(i[0][0:4]+temp+i[0][7:])[0]])
    result = sorted(result, key=lambda x:(x[1]), reverse=True)
    if len(result) > 10:
        count = 0
        for i in result[9:]:
            count = count + i[1]
        result = result[0:9]
        result.append(["其他", count])
    return result

def get_engineer_and_en_by_ipc(ipc_id):
    """
    根据ipc获取工程师以及所在的公司,用于专利分组
    :param ipc_id: ipc
    :return: 前10家的企业以及专利前10的工程师
    """
    temp = enterprise_patent_dao.get_engineer_and_en_by_ipc(ipc_id)
    en_id_list = []
    for i in temp:
        en_id_list.append(i[0])
    en_id_dict = {}
    for key in en_id_list:
        en_id_dict[key] = en_id_dict.get(key, 0) + 1
    list1 = sorted(en_id_dict.items(), key=lambda x:x[1], reverse=True)
    ten_en = []
    for i in list1[0:10]:
        ten_en.append(i[0])
    result = []
    for i in ten_en:
        temp1 = []
        for j in temp:
            if j[0] == i:
                temp1.extend(j[1].split(","))
        engineer_dict = {}
        for key in temp1:
            engineer_dict[key] = engineer_dict.get(key, 0) + 1
        engineer_list = sorted(engineer_dict.items(), key=lambda x: x[1], reverse=True)
        ten_engineer = []
        for x in engineer_list[0:10]:
            ten_engineer.append(x[0])
        if ten_engineer != ['不公告发明人']:
            result.append([ enterprise_dao.get_en_name_by_en_id(i), ten_engineer ])
    return result

def get_engineer_and_en_by_ipc2(ipc_id):
    """
    根据ipc获取工程师以及所在的公司,用于工程师分组
    :param ipc_id: ipc
    :return: 前10家的企业以及工程师
    """
    temp = enterprise_patent_dao.get_engineer_and_en_by_ipc(ipc_id)
    en_id_list = []
    for i in temp:
        en_id_list.append(i[0])
    en_id_dict = {}
    for key in en_id_list:
        en_id_dict[key] = en_id_dict.get(key, 0) + 1
    list1 = sorted(en_id_dict.items(), key=lambda x:x[1], reverse=True)
    ten_en = []
    for i in list1[0:10]:
        ten_en.append(i[0])
    result = []
    for i in ten_en:
        temp1 = []
        for j in temp:
            if j[0] == i:
                temp1.extend(j[1].split(","))
        engineer_dict = {}
        for key in temp1:
            engineer_dict[key] = engineer_dict.get(key, 0) + 1
        engineer_list = sorted(engineer_dict.items(), key=lambda x: x[1], reverse=True)
        ten_engineer = []
        for x in engineer_list[0:15]:
            ten_engineer.append(x[0])
        if ten_engineer != ['不公告发明人']:
            result.append([ enterprise_dao.get_en_name_by_en_id(i), ten_engineer ])
    return result

def get_engineer_count_with_first_ipc():
    """
    根据第一类ipcid获取工程师数量
    :return:
    """
    all_first_ipc = enterprise_patent_dao.get_first_ipc()
    result = []
    for i in all_first_ipc:
        result.append([i[0] + ":" + i[1], enterprise_patent_dao.get_count_with_ipc(i[0])])
    result = sorted(result, key=lambda x:(x[1]), reverse=True)
    return result

def get_engineer_count_with_second_ipc():
    """
    根据第二类ipcid获取工程师数量
    :return:
    """
    all_second_ipc = enterprise_patent_dao.get_second_ipc()
    result = []
    for i in all_second_ipc:
        if enterprise_patent_dao.get_count_with_ipc(i[0]) > 100:
            result.append([i[0] + ":" + i[1], enterprise_patent_dao.get_count_with_ipc(i[0])])
    result = sorted(result, key=lambda x: (x[1]), reverse=True)
    return result

def get_engineer_count_with_third_ipc():
    """
    根据第三类ipcid获取工程师数量
    :return:
    """
    all_third_ipc = enterprise_patent_dao.get_all_third_ipc()
    result = []
    for i in all_third_ipc:
        if enterprise_patent_dao.get_count_with_ipc2(i[0]) > 50:
            result.append([i[0] + ":" + i[1], enterprise_patent_dao.get_count_with_ipc2(i[0])])
    result = sorted(result, key=lambda x: (x[1]), reverse=True)
    return result

if __name__ == "__main__":
    # print(get_count_by_firstkind("电子信息技术"))
    # print(get_engineer_and_en_by_ipc("A23C7/00"))
    print(get_engineer_count_with_third_ipc())
    # pass