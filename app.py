from threading import Thread
from datetime import datetime
from flask import Flask, jsonify, g
from flask import render_template, request
from flask_basicauth import BasicAuth

from plugins.scanners import (
    update_wpscan,
    find_cms
)
from core import Scanner
from db import (
    init_db,
    get_db,
    dict_factory
)

app = Flask(__name__, static_folder="static")
# Basic Auth Credentials
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
app.config['BASIC_AUTH_FORCE'] = False

basic_auth = BasicAuth(app)

try:
    Thread(target=update_wpscan).start()
    init_db(app)
except:
    pass


@app.teardown_appcontext
def close_connection(exception):
    dbo = getattr(g, '_database', None)
    if dbo is not None:
        dbo.close()


@app.template_filter('tmstring')
def tms_filter(tms):
    if tms:
        tmso = datetime.utcfromtimestamp(float(tms))
        return tmso.strftime('%Y-%m-%d %H:%M:%S')
    return ""


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/scans", methods=['GET'])
def list_scans():
    dbo = get_db()
    dbo.row_factory = dict_factory
    cur = dbo.cursor().execute('SELECT id,url,cms,tms from cmsscan')
    all_scans = cur.fetchall()
    all_scans.reverse()
    cur.close()
    return render_template('scans.html', scans=all_scans)


@app.route("/result/<int:scan_id>", methods=['GET'])
def view_result(scan_id):
    resp = {
        "id": "",
        "url": "",
        "cms": "",
        "tms": "",
        "res": "",
    }
    dbo = get_db()
    cur = dbo.cursor().execute('SELECT * from cmsscan WHERE id=?', (scan_id,))
    res = cur.fetchall()
    cur.close()
    if res:
        resp = {
            "id": res[0][0],
            "url": res[0][1],
            "cms": res[0][2],
            "tms": res[0][4],
            "res": res[0][3],
        }
    if resp["cms"] in ["joomla", "vbulletin"]:
        return render_template('result_plain.html', result=resp)
    return render_template('result.html', result=resp)


@app.route("/delete", methods=['POST'])
def delete_scan():
    scan_id = request.form.get('id')
    dbo = get_db()
    dbo.cursor().execute('DELETE FROM cmsscan WHERE id=?', (scan_id,))
    dbo.commit()
    dbo.close()
    return jsonify({"status": "ok"})


@app.route("/scan", methods=['POST'])
def scan():
    url = request.form.get('url')
    cmsg = request.form.get('cms')
    if cmsg in ['wordpress', 'drupal', 'joomla', 'vbulletin']:
        cms = cmsg
    else:
        cms = find_cms(url)
    if cms == "unknown":
        resp = {"error": "Cannot Detect CMS"}
    else:
        resp = {"url": url, "cms": cms, "message": "Scheduled for Scan"}
        scano = Scanner(app, url, cms)
        Thread(target=scano.scan).start()
    return jsonify(resp)

if __name__ == "__main__":
    app.run(debug=True)
