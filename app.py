from settings import Settings
import os
import sys
from datetime import datetime
from datetime import timedelta
import dateutil.parser
from flask import Flask, session, render_template, request, redirect, url_for, jsonify, make_response
import pandas as pd
import string
import re
from beaker.middleware import SessionMiddleware
from flask.sessions import SessionInterface
from random import choice
import functools
from random import randrange

session_opts = {
    'session.type': 'ext:memcached',
    'session.url': '127.0.0.1:11211',
    'save_accessed_time': True,
    'secure': True,
    'timeout': Settings.session_timeout
}

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = "".join([choice(string.ascii_letters + string.digits + '_' + '-' + '!' + '#' + '&')
                          for i in range(64)])
app.config['JSON_AS_ASCII'] = False


class BeakerSessionInterface(SessionInterface):

    def open_session(self, app, request):
        return request.environ['beaker.session']

    def save_session(self, app, session, response):
        session.save()


if Settings.envrionment == "production":
    app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    app.session_interface = BeakerSessionInterface()


def init_settings():
    session['app_name'] = Settings.app_name
    session['sid'] = Settings.sid
    session['root'] = Settings.root
    session['environment'] = Settings.envrionment
    session['japanese_calendar'] = Settings.japanese_calendar
    session['last_access'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def init_session():
    init_settings()
    session.pop('title', None)
    session.pop('alert_message', None)
    session.pop('alert_level', None)
    session.pop('uid', None)
    session.pop('role', None)
    session.pop('department', None)
    session.pop('attendant', None)
    session.pop('last_login', None)


def _isalnum(s):
    rep = re.compile(r'^[a-zA-Z0-9_]+$')
    return rep.match(s) is not None


def _isalnum_space(s):
    rep = re.compile(r'^[a-zA-Z0-9_\ ]+$')
    return rep.match(s) is not None


def _isdatetime(s):
    rep = re.compile(r'^([1-9]{1}[0-9]{3})\/([0-1][0-9])\/([0-3][0-9])$')
    return rep.match(s) is not None


def _isvaliddate(s):
    try:
        dateutil.parser.parse(s)
        return True
    except ValueError:
        return False


def check_content_length_of_request_decorator(max_content_length):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorated_view(*args, **kwargs):
            if int(request.headers.get('Content-Length') or 0) > max_content_length:
                return abort(400, description='Too much content in request')
            else:
                return fn(*args, **kwargs)
        return decorated_view
    return wrapper


def check_from_to(date_from, date_to):
    if not _isdatetime(date_from) or not _isdatetime(date_to):
        session['alert_level'] = "warning"
        session['alert_message'] = "日時の形式が正しくありません。日時は YYYY/MM/DD の形式で入力してください。"
        return False

    if not _isvaliddate(date_from) or not _isvaliddate(date_to):
        session['alert_level'] = "warning"
        session['alert_message'] = "カレンダーに存在しない日時が入力されました。有効な日時を入力してください。"
        return False

    if dateutil.parser.parse(date_from) > dateutil.parser.parse(date_to):
        session['alert_level'] = "warning"
        session['alert_message'] = "期間指定において開始日より終了日が前になっています。"
        return False
    return True


def next_day(day):
    try:
        return datetime.strftime(datetime.strptime(day, "%Y/%m/%d") + timedelta(days=1), "%Y/%m/%d")
    except OverflowError:
        return datetime(9999, 12, 31, 23, 59, 59, 999999)


def avail(screen_name):
    session.pop('alert_message', None)
    session.pop('alert_level', None)

    if session.get('last_access') is None:
        return False

    if session.get('sid') != Settings.sid:
        return False

    if len(request.query_string) > 0:
        return False

    if datetime.strptime(session.get('last_access'), "%Y-%m-%d %H:%M:%S") < datetime.now() - timedelta(seconds=Settings.session_timeout):
        return False

    if session.get('sid') is None:
        return False
    if session.get('uid') is None:
        return False

    if screen_name not in Settings.available_screens:
        return False

    session['last_access'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return True


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/', methods=['GET'])
def Login():
    init_session()
    session['title'] = "ログイン"
    return render_template('login.html')


@app.errorhandler(404)
def page_not_found(error):
    init_session()
    session['title'] = "ログイン"
    session['alert_level'] = "danger"
    session['alert_message'] = "ページが見つかりません。"
    return render_template('login.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    init_session()
    session['title'] = "ログイン"
    session['alert_level'] = "danger"
    session['alert_message'] = "不正なリクエストが送信されました。"
    return render_template('login.html'), 405


@app.errorhandler(500)
def internal_server_error(error):
    init_session()
    session['title'] = "ログイン"
    session['alert_level'] = "danger"
    session['alert_message'] = "エラーが発生しました。"
    return render_template('login.html'), 500


@app.route('/login', methods=['GET'])
def Auth_Failure():
    init_session()
    session['title'] = "ログイン"
    session['alert_level'] = "danger"
    session['alert_message'] = "認証に失敗しました。"
    return render_template('login.html')


@app.route('/dashboard', methods=['POST', 'GET'])
@check_content_length_of_request_decorator(10000000)
def Dashboard():
    screen_name = 'dashboard'

    datas = pd.DataFrame([['A',randrange(100),],['B',randrange(100)],['C',randrange(100)]])

    notifications = pd.DataFrame([['A','a'], ['B','b']])

    search_from = ''
    search_to = ''

    dfs = pd.DataFrame([['A','a',1], ['B','b',2], ['C','c',3], ['D','d',4], ['E','e',5], ['F','f',6]])

    if request.method == 'POST':
        session['role'] = 'normal'
        session['department'] = '01'
        session['attendant'] = '01'
        session['sid'] = '9999'
        session['uid'] = '10000001'
        session['alert_level'] = "success"
        session['alert_message'] = "ログインに成功しました。"

    session['title'] = "ダッシュボード"
    return render_template('dashboard.html',
                           notifications=notifications,
                           datas=datas,
                           dfs=dfs)


@app.route('/api/breakdown', methods=['GET'])
def Breakdown():
    screen_name = 'dashboard'
    if avail(screen_name) is False:
        return redirect(url_for('Auth_Failure'))

    labels = []
    data = []
    colors = []

    for label in ['要素1', '要素2', '要素3', '要素4', '要素5', '要素6', '要素7']:
        labels.append(label)
        data.append(randrange(100))

    palette = ['#0074bf', '#f2cf01', '#c93a40',
               '#56a764', '#cc528b', '#d16b16', '#9460a0']
    for i, label in enumerate(labels):
        colors.append(palette[i % len(palette)])

    json_data = {
        'type': 'pie',
        'data': {
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': colors
            }],
        },
    }
    return jsonify(json_data)


@app.route('/api/transition', methods=['GET'])
def Transition():
    screen_name = 'dashboard'
    if avail(screen_name) is False:
        return redirect(url_for('Auth_Failure'))

    labels = []
    data = []
    maxdata = 100
    stepsize = 10

    for label in ['要素1', '要素2', '要素3', '要素4', '要素5', '要素6']:
        labels.append(label)
        data.append(randrange(100))

    json_data = {
        'type': 'bar',
        'data': {
            'labels': labels,
            'datasets': [{
                'label': "残高",
                'backgroundColor': "rgba(77,145,187,0.8)",
                'borderColor': "rgba(77,145,187,1)",
                'data': data,
                'borderWith': 1,
            }],
        },
        'options': {
            'scales': {
                'xAxes': [{
                    'time': {
                        'unit': 'month'
                    },
                    'gridLines': {
                        'display': False
                    },
                    'ticks': {
                        'maxTicksLimit': len(labels)
                    }
                }],
                'yAxes': [{
                    'ticks': {
                        'min': 0,
                        'max': maxdata,
                        'stepSize': stepsize,
                        'maxTicksLimit': len(data)
                    },
                    'gridLines': {
                        'display': True
                    }
                }],
            },
            'legend': {
                'display': False
            }
        }
    }
    return jsonify(json_data)


if __name__ == "__main__":
    if Settings.envrionment == "production":
        app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
        app.session_interface = BeakerSessionInterface()
    port = os.getenv('PORT', '3000')
    app.run(host='0.0.0.0', port=int(port))
