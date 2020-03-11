from flask import Flask,render_template,request
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

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)
