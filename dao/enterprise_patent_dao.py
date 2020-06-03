"""
有关企业专利的数据库查询文件
"""
# -*- coding: utf-8 -*-
import pymysql

from config.config import BERT_Params
from config.config import Milvus_Params
from config.config import MysqlDB_Params
from config.config import MysqlDB_Params_kunshan
from bert_serving.client import BertClient
from milvus import Milvus, IndexType, MetricType

bc = BertClient(ip=BERT_Params['ip'])
# 初始化一个Milvus类，以后所有的操作都是通过milvus来的
milvus = Milvus()
# # 连接到服务器，注意端口映射，要和启动docker时设置的端口一致
s = milvus.connect(host=Milvus_Params['host'], port=Milvus_Params['port'])
# mysql数据库连接
conn = pymysql.connect(host=MysqlDB_Params['host'], user=MysqlDB_Params["user"], password=MysqlDB_Params["password"],
                       db=MysqlDB_Params['db'], port=MysqlDB_Params['port'],
                       charset=MysqlDB_Params['charset'])
cursor = conn.cursor()


conn_kunshan = pymysql.connect(host=MysqlDB_Params_kunshan['host'], user=MysqlDB_Params_kunshan["user"], password=MysqlDB_Params_kunshan["password"],
                       db=MysqlDB_Params_kunshan['db'], port=MysqlDB_Params_kunshan['port'],
                       charset=MysqlDB_Params_kunshan['charset'])
cursor_kunshan = conn_kunshan.cursor()


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
        status, results = milvus.search(table_name="patent_vector", query_records=searched_patent_vector, top_k=4,
                                        nprobe=16)
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
    sql = """select pa_applicant from enterprise_patent where pa_id=%s""".format(pa_id)
    cursor.execute(sql, pa_id)
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
    result = [[firstkind], [secondkind], [thirdkind]]
    return result


def get_second_field(field):
    """
    根据一级技术领域寻找二级技术领域
    :param field:
    :return:
    """
    sql = "select distinct secondkind from technical_field where firstkind = %s ".format(field)
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
    sql = "select distinct thirdkind from technical_field where secondkind = %s ".format(field)
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


def get_first_ipc():
    """
    获取第一类ipc目录，只有1位
    :return:
    """
    sql = "select ipc_id, ipc_content from ipc where char_length (ipc_id) = 1"
    cursor.execute(sql)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        result.append([i[0], i[1]])
    return result


def get_second_ipc(ipc_id):
    """
    获取第二类ipc目录，只有4位
    :return:
    """
    query_param = ['%s%%' % ipc_id]
    sql = "select ipc_id, ipc_content from ipc where char_length (ipc_id) = 4 and ipc_id like %s"
    cursor.execute(sql, query_param)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        if "(" in i[1]:
            result.append([i[0], i[1][0:i[1].index("(")]])
        else:
            result.append([i[0], i[1]])
    return result


def get_second_ipc():
    """
    获取第二类ipc目录，只有4位
    :return:
    """
    sql = "select ipc_id, ipc_content from ipc where char_length (ipc_id) = 4"
    cursor.execute(sql)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        if "(" in i[1]:
            result.append([i[0], i[1][0:i[1].index("(")]])
        else:
            result.append([i[0], i[1]])
    return result


def get_third_ipc(ipc_id):
    """
    获取第三类ipc目录，超过4位
    :return:
    """
    query_param = ['%s%%' % ipc_id]
    sql = "select ipc_id, ipc_content from ipc where char_length (ipc_id) > 4 and ipc_id like %s"
    cursor.execute(sql, query_param)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        if "(" in i[1]:
            result.append([i[0], i[1][0:i[1].index("(")]])
        else:
            result.append([i[0], i[1]])
    return result


def get_third_ipc():
    """
    获取第三类ipc目录，超过4位
    :return:
    """
    sql = "select ipc_id, ipc_content from ipc where char_length (ipc_id) > 4"
    cursor.execute(sql)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        if "(" in i[1]:
            temp1 = i[0][4:7].replace("0", "")
            result.append([i[0][0:4] + temp1 + i[0][7:], i[1][0:i[1].index("(")]])
        else:
            result.append([i[0], i[1]])
    return result


def get_ipc_content_by_ipc_id(ipc_id):
    """
    根据ipc_id获取ipc内容
    :return:
    """
    if len(ipc_id) > 4:
        ipc_id = ipc_id[0:4]
    sql = "select ipc_content from ipc where ipc_id = %s".format(ipc_id)
    cursor.execute(sql, ipc_id)
    temp = cursor.fetchone()
    result = ''
    if "(" in temp[0]:
        result = temp[0][0: temp[0].index("(")]
    else:
        result = temp[0]
    return result


def get_all_third_ipc():
    """
    从专利表中统计第三类ipc目录
    :return:
    """
    sql = "select pa_main_kind_num from enterprise_patent"
    cursor.execute(sql)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        result.append(i[0])
    result_dict = {}
    for key in result:
        result_dict[key] = result_dict.get(key, 0) + 1
    result_1 = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    result_2 = []
    for i in result_1:
        if len(i[0]) > 5:
            result_2.append([i[0], i[1]])
    result_2 = sorted(result_2, key=lambda x: x[1], reverse=True)[0:50]
    final_result = []
    for i in result_2:
        final_result.append([i[0], get_ipc_content_by_ipc_id(i[0])])
    return final_result


def get_patent_by_ipc(ipc_id):
    """
    获取ipc_id开头的所有专利数量
    :param ipc_id:
    :return:
    """
    query_param = ['%s%%' % ipc_id]
    sql = "select count(*) from enterprise_patent where pa_main_kind_num like %s"
    cursor.execute(sql, query_param)
    result = cursor.fetchone()
    return result


def get_engineer_and_en_by_ipc(ipc_id):
    """
    根据ipc获取工程师以及所在的公司
    :param field: 技术领域
    :return: 公司以及工程师
    """
    sql = "select en_id, pa_inventor from enterprise_patent where pa_main_kind_num =%s ".format(ipc_id)
    cursor.execute(sql, ipc_id)
    result = cursor.fetchall()
    return result


def get_count_with_ipc(ipc_id):
    """
    根据ipc获取相关的所有工程师数量
    :return:
    """
    query_param = ['%s%%' % ipc_id]
    sql = "select pa_inventor from enterprise_patent where pa_main_kind_num like %s"
    cursor.execute(sql, query_param)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        for j in i:
            result.append(j)
    result = list(set(result))
    return len(result)


def get_count_with_ipc2(ipc_id):
    """
    根据ipc获取相关的所有工程师数量,第三类
    :return:
    """
    sql = "select pa_inventor from enterprise_patent where pa_main_kind_num = %s".format(ipc_id)
    cursor.execute(sql, ipc_id)
    temp = cursor.fetchall()
    result = []
    for i in temp:
        for j in i:
            result.append(j)
    result = list(set(result))
    return len(result)


def get_ep_and_inventor_by_keyword(keyword):
    """
    根据关键字获取相关企业
    """
    query_param = ['%%%s%%' % keyword]
    sql = """select ebi.name ep_name, ifnull(ebi.telephone,"") telephone, p.inventor inventor
            from  ep_base_info ebi 
            left join patent p on p.ep_name = ebi.name 
            where p.abstract like %s""" .format(query_param)
    cursor_kunshan.execute(sql, query_param)
    result = cursor_kunshan.fetchall()
    return result


def get_inventor_by_keyword(ep_name, keyword):
    """
    根据企业名和关键词获取发明人
    """
    query_param = ['%%%s%%' % keyword]
    sql = "select inventor from patent where ep_name=%s and abstract like %s" .format(ep_name, query_param)
    cursor_kunshan.execute(sql, (ep_name, query_param))
    temp = cursor_kunshan.fetchall()
    result = []
    for i in temp:
        result.extend(i)
    return list(set(result))


if __name__ == "__main__":
    # print(get_pa_id_by_patent("不锈钢"))
    # gg = get_en_name_by_pa_id(56460)
    # print(gg)
    # print(get_engineer("电子信息技术"))
    # print(get_all_field())
    # print(get_engineer_and_en_by_field("低温余热发电技术"))
    # print(get_engineer_and_en_by_ipc("A23C7/00"))
    # print(get_patent_by_first_ipc("A"))
    print(get_ep_by_keyword("纳米纤维"))
    # print(get_ipc_content_by_ipc_id("F21S"))
    # pass
