"""
处理有关企业专利信息的数据库获取结果的处理
"""
import dao.enterprise_patent_dao as enterprise_patent_dao
import dao.enterprise_dao as enterprise_dao

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

def get_count_by_field():
    field = ["电子信息技术", "生物与新医药技术", "新材料技术", "资源与环境技术", "高新技术改造传统产业", "高技术服务业", "航空航天技术", "新能源及节能技术"]
    result = []
    for i in field:
        result.append([i, enterprise_patent_dao.get_count(i)[0]])
    print(result)


if __name__ == "__main__":
    get_count_by_field()