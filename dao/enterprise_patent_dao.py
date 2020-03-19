"""
有关企业专利的数据库查询文件
"""
# -*- coding: utf-8 -*-
import pymysql

from config.config import BERT_Params
from config.config import Milvus_Params
from config.config import MysqlDB_Params
from bert_serving.client import BertClient
from milvus import Milvus, IndexType, MetricType

bc = BertClient(ip=BERT_Params['ip'])
# 初始化一个Milvus类，以后所有的操作都是通过milvus来的
milvus = Milvus()
# # 连接到服务器，注意端口映射，要和启动docker时设置的端口一致
s = milvus.connect(host=Milvus_Params['host'], port=Milvus_Params['port'])
#mysql数据库连接
conn = pymysql.connect(host=MysqlDB_Params['host'], user=MysqlDB_Params["user"], password=MysqlDB_Params["password"], db=MysqlDB_Params['db'], port=MysqlDB_Params['port'],
                       charset=MysqlDB_Params['charset'])
cursor = conn.cursor()


def stringTovector(searched_patent):
    """
    将企业专利搜索结果转化为向量
    :param searched_patent: 搜索的专利成果
    :return:文本向量
    """
    result = searched_patent.strip().replace(" ", "").replace('\n', '').replace('\r', '')
    result = list(result)
    input = bc.encode(result)
    return input[0]

def arraystr_to_vector(patent_vector):
    """
    将Bert生成的二位数组字符串转化为float向量列表
    :param str:
    :return: float列表
    """
    patent_vector = str(patent_vector)
    temp = []
    for i in patent_vector.replace("[", "").replace("]", "").split("\n"):
        for j in i.split(" "):
            if j != '':
                temp.append(float(j))
    return temp

def get_pa_id_by_patent(searched_patent):
    """
    从Milvus根据搜索专利成果的向量搜索专利id
    :param searched_patent:搜索向量
    :return:专利
    """

    # 进行查询, 注意这里的参数nprobe和建立索引时的参数nlist 会因为索引类型不同而影响到查询性能和查询准确率
    # 对于 FLAT类型索引，两个参数对结果和速度没有影响
    searched_patent_vector = [arraystr_to_vector(stringTovector(searched_patent))]
    # print(searched_patent)
    try:
        status, results = milvus.search(table_name="patent_vector", query_records=searched_patent_vector, top_k=4, nprobe=16)
        # 断开连接
        temp = []
        milvus.disconnect()
        for i in results[0]:
            temp.append(int(str(i)[str(i).index("=") + 1:str(i).index(",")]))
        return temp
    except:
        return "error"

def get_en_name_by_pa_id(pa_id):
    """
    根据专利id获取企业名
    :param pa_id:专利id
    :return:企业名
    """
    sql = """select pa_applicant from enterprise_patent where pa_id=%s""" .format(pa_id)
    cursor.execute(sql,pa_id)
    result = cursor.fetchone()[0]
    return result


def get_count_by_firstkind(field):
    """
     根据第一类技术领域寻找专利数量
    """
    query_param = ['%%%s%%' % field]
    sql = "select count(*) from enterprise_patent where pa_first_kind like %s "
    cursor.execute(sql, query_param)
    result = cursor.fetchone()
    return result

def get_count_by_secondkind(field):
    """
     根据第二类技术领域寻找专利数量
    """
    query_param = ['%%%s%%' % field]
    sql = "select count(*) from enterprise_patent where pa_second_kind like %s "
    cursor.execute(sql, query_param)
    result = cursor.fetchone()
    return result

def get_count_by_thirdkind(field):
    """
     根据第三类技术领域寻找专利数量
    """
    query_param = ['%%%s%%' % field]
    sql = "select count(*) from enterprise_patent where pa_third_kind like %s "
    cursor.execute(sql, query_param)
    result = cursor.fetchone()
    return result

def get_all_field():
    """
    获取所有技术领域
    :return:
    """
    sql1 = "select distinct firstkind from technical_field"
    sql2 = "select distinct secondkind from technical_field"
    sql3 = "select distinct thirdkind from technical_field"
    cursor.execute(sql1)
    firstkind = cursor.fetchall()
    cursor.execute(sql2)
    secondkind = cursor.fetchall()
    cursor.execute(sql3)
    thirdkind = cursor.fetchall()
    result = [[firstkind],[secondkind],[thirdkind]]
    return result

def get_second_field(field):
    """
    根据一级技术领域寻找二级技术领域
    :param field:
    :return:
    """
    sql = "select distinct secondkind from technical_field where firstkind = %s " .format(field)
    cursor.execute(sql, field)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        result.append(i[0])
    return result


def get_third_field(field):
    """
    根据二级技术领域寻找三级技术领域
    :param field:
    :return:
    """
    sql = "select distinct thirdkind from technical_field where secondkind = %s " .format(field)
    cursor.execute(sql, field)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        result.append(i[0])
    return result

def get_engineer_by_thirdkind(field):
    """
    根据第三类技术领域寻找相关工程师
    :param field:
    :return:
    """
    query_param = ['%%%s%%' % field]
    sql = "select pa_inventor from enterprise_patent where pa_third_kind like %s "
    cursor.execute(sql, query_param)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        for j in i[0].split(","):
            result.append(j)
    return list(set(result))


def get_engineer_and_en_by_field(field):
    """
    根据技术领域获取工程师以及所在的公司
    :param field: 技术领域
    :return: 公司以及工程师
    """
    query_param = ['%%%s%%' % field]
    sql = "select en_id, pa_inventor from enterprise_patent where pa_third_kind like %s "
    cursor.execute(sql, query_param)
    result = cursor.fetchall()
    return result

if __name__ == "__main__":
    # print(get_pa_id_by_patent("不锈钢"))
    # gg = get_en_name_by_pa_id(56460)
    # print(gg)
    # print(get_engineer("电子信息技术"))
    # print(get_all_field())
    # print(get_engineer_and_en_by_field("低温余热发电技术"))
    pass