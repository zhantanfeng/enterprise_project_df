"""
处理有关企业信息的数据库获取结果的处理
"""
import dao.enterprise_dao as enterprise_dao


def get_en_info_by_name(name):
    """
    根据企业名获取企业列表
    :param name: 企业名
    :return: 企业信息
    """
    result = enterprise_dao.get_en_info_by_name_2(name)
    return result


def get_en_info_by_scope(scope):
    """
    根据企业经营范围获取企业列表
    :param scope: 企业经营范围
    :return: 企业信息
    """
    result = enterprise_dao.get_en_info_by_scope(scope)
    return result



if __name__ == "__main__":
    print(enterprise_dao.get_en_info_by_name("钢铁"))