"""
有关企业信息的数据库查询文件
"""
# -*- coding: utf-8 -*-
import pymysql
from config.config import BERT_Params
from config.config import Milvus_Params
from config.config import MysqlDB_Params


conn = pymysql.connect(host=MysqlDB_Params['host'], user=MysqlDB_Params["user"], password=MysqlDB_Params["password"], db=MysqlDB_Params['db'], port=MysqlDB_Params['port'],
                       charset=MysqlDB_Params['charset'])
cursor = conn.cursor()

def get_en_info_by_name_1(en_name):
    """
    根据企业名获取企业列表
    :param en_name: 企业名
    :return: 企业信息
    """
    sql = "select * from en_base_info where en_name=%s" .format(en_name)
    cursor.execute(sql,en_name)
    result = cursor.fetchone()
    return result

def get_en_info_by_name_2(en_name):
    """
    根据企业名获取企业列表，模糊查询
    :param en_name: 企业名
    :return: 企业信息
    """
    query_param = ['%%%s%%' % en_name]
    sql = "select * from en_base_info where en_name like %s"
    cursor.execute(sql,query_param)
    result = cursor.fetchall()
    return result

def get_en_info_by_scope(scope):
    """
    根据企业经营获取企业列表，模糊查询
    :param en_name: 企业经营范围
    :return: 企业信息
    """
    query_param = ['%%%s%%' % scope]
    sql = "select * from en_base_info where en_scope like %s"
    cursor.execute(sql, query_param)
    result = cursor.fetchall()
    return result



if __name__ == "__main__":
    print(get_en_info_by_name_1("昆山雅森电子材料科技有限公司"))
