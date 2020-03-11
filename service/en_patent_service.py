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