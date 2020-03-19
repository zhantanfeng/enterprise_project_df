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

@app.route('/init_pic')
def init_pic():
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

@app.route('/get_data')
def get_data():
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

@app.route("/get_engineer/<field>")
def get_engineer(field):
    #获取技术领域的工程师以及所在的企业
    engineer_list = en_pa_service.get_engineer_and_en_by_field(field)
    return render_template("engineer.html", engineer_list = engineer_list, field=field)





if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)
