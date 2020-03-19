from flask import Flask, render_template, request, jsonify
import service.enterprise_service as en_service
import service.en_patent_service as en_pa_service
from config.config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search_en',methods=['GET', 'POST'])
def search_en():
    if request.method == 'POST':
        search_content = request.form.get("enterprise")
        search_style = request.values.get("optradio")
        if search_style == "企业名":
            result = en_service.get_en_info_by_name(search_content)
            return render_template("en_info.html", enterprises=result, enterprise_name = search_content)
        elif search_style == "企业经营范围":
            result = en_service.get_en_info_by_scope(search_content)
            return render_template("en_info.html", enterprises=result, enterprise_name = search_content)
        else:
            result = en_pa_service.get_en_info_by_patent(search_content)
            return render_template("en_info.html", enterprises=result, enterprise_name = search_content)

@app.route('/area_info')
def area_info():
    return render_template("area_info.html")

@app.route('/patent_info')
def patent_info():
    return render_template("patent_info.html")

@app.route('/engineer_info')
def engineer_info():
    return render_template("engineer_info.html")

@app.route('/init_field_pic')
def init_field_pic():
    """
    初始化技术领域分组的饼图
    :return:
    """
    data = en_pa_service.get_pa_count_by_firstkind()
    data1 = []
    data2 = []
    for i in data:
        data1.append(i[0])
        data2.append({"value": i[1], "name": i[0]})
    return jsonify({
        'status': 'ok',
        'data1': data1,
        'data2': data2
    })

@app.route('/init_patent_pic')
def init_patent_pic():
    """
    :return:
    """
    data = en_pa_service.get_patent_by_first_ipc()
    data1 = []
    data2 = []
    for i in data:
        data1.append(i[0])
        data2.append({"value": i[1], "name": i[0]})
    return jsonify({
        'status': 'ok',
        'data1': data1,
        'data2': data2
    })


@app.route('/init_engineer_bar')
def init_engineer_bar():
    """
    初始化工程师分组的柱状图
    :return:
    """
    data = en_pa_service.get_engineer_count_with_first_ipc()
    data1 = []
    data2 = []
    for i in data:
        data1.append(i[0])
        data2.append({"value": i[1], "name": i[0]})
    return jsonify({
        'status': 'ok',
        'data1': data1,
        'data2': data2
    })

@app.route('/get_field_data')
def get_field_data():
    all_field = en_pa_service.get_all_field()
    field_name = request.args.get('name')
    if field_name == "高技术服务业":
        data = en_pa_service.get_count_by_secondkind(field_name)
        data1 = []
        data2 = []
        for i in data:
            data1.append(i[0])
            data2.append({"value": i[1], "name": i[0]})
        return jsonify({
            'status': 'ok',
            'data1': data1,
            'data2': data2
        })
    if field_name == "航空航天技术":
        data = en_pa_service.get_count_by_secondkind(field_name)
        data1 = []
        data2 = []
        for i in data:
            data1.append(i[0])
            data2.append({"value": i[1], "name": i[0]})
        return jsonify({
            'status': 'ok',
            'data1': data1,
            'data2': data2
        })
    if field_name in all_field[0]:
        data = en_pa_service.get_count_by_firstkind(field_name)
        data1 = []
        data2 = []
        for i in data:
            data1.append(i[0])
            data2.append({"value": i[1], "name": i[0]})
        return jsonify({
            'status': 'ok',
            'data1': data1,
            'data2': data2
        })
    elif field_name in all_field[1]:
        data = en_pa_service.get_count_by_secondkind(field_name)
        data1 = []
        data2 = []
        for i in data:
            data1.append(i[0])
            data2.append({"value": i[1], "name": i[0]})
        return jsonify({
            'status': 'ok',
            'data1': data1,
            'data2': data2
        })
    else:
        return jsonify({
            'status': 'third'
        })


@app.route('/get_ipc_data')
def get_ipc_data():
    """
    根据ipc_id获取专利数量
    :return:
    """
    ipc_id = request.args.get('name')[0:request.args.get('name').index(":")]
    if len(ipc_id) == 1:
        data = en_pa_service.get_patent_by_second_ipc(ipc_id)
        data1 = []
        data2 = []
        for i in data:
            data1.append(i[0])
            data2.append({"value": i[1], "name": i[0]})
        return jsonify({
            'status': 'ok',
            'data1': data1,
            'data2': data2
        })
    elif len(ipc_id) == 4:
        data = en_pa_service.get_patent_by_third_ipc(ipc_id)
        data1 = []
        data2 = []
        for i in data:
            if i[1] != 0:
                data1.append(i[0])
                data2.append({"value": i[1], "name": i[0]})
        return jsonify({
            'status': 'ok',
            'data1': data1,
            'data2': data2
        })
    else:
        return jsonify({
            'status': 'third'
        })


@app.route('/get_engineer_second_ipc')
def get_engineer_second_ipc():
    """
    根据第二类ipc_id获取工程师数量
    :return:
    """
    data = en_pa_service.get_engineer_count_with_second_ipc()
    data1 = []
    data2 = []
    for i in data:
        data1.append(i[0])
        data2.append({"value": i[1], "name": i[0]})
    return jsonify({
        'status': 'ok',
        'data1': data1,
        'data2': data2
    })

@app.route('/get_engineer_third_ipc')
def get_engineer_third_ipc():
    """
    根据第三类ipc_id获取工程师数量
    :return:
    """
    data = en_pa_service.get_engineer_count_with_third_ipc()
    data1 = []
    data2 = []
    for i in data:
        data1.append(i[0])
        data2.append({"value": i[1], "name": i[0]})
    return jsonify({
        'status': 'ok',
        'data1': data1,
        'data2': data2
    })

@app.route("/get_field_engineer/<field>")
def get_field_engineer(field):
    #获取技术领域的工程师以及所在的企业
    engineer_list = en_pa_service.get_engineer_and_en_by_field(field)
    return render_template("field_engineer.html", engineer_list = engineer_list, field=field)

@app.route("/get_patent_engineer/<ipc_id>")
def get_patent_engineer(ipc_id):
    #获取ipc分类的工程师以及所在的企业
    ipc_id = ipc_id.replace("$", "/")
    engineer_list = en_pa_service.get_engineer_and_en_by_ipc(ipc_id[0:ipc_id.index(":")])
    return render_template("patent_engineer.html", engineer_list = engineer_list, ipc_id = ipc_id)


@app.route("/get_engineer/<ipc_id>")
def get_engineer(ipc_id):
    #获取ipc分类的工程师以及所在的企业
    ipc_id = ipc_id.replace("$", "/")
    engineer_list = en_pa_service.get_engineer_and_en_by_ipc2(ipc_id[0:ipc_id.index(":")])
    return render_template("patent_engineer.html", engineer_list = engineer_list, ipc_id = ipc_id)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)
