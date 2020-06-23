import json

from flask import Flask, render_template, redirect, request, Markup, escape
from datetime import datetime

application = Flask(__name__)

DATA_FILE = "norilog.json"

def save_data(start, finish, memo, created_at):
    """記録データを保存する処理
    :param start　乗った駅
    :type start str
    :param finish　降りた駅
    :type finish str
    :param memo　その時の状況
    :type memo str
    :param created_at　その時の日時
    :type created_at datetime.dattime
    """
    try:
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database =[ ]

    #データベースファイル更新
    database.insert(0, {
        "start": start,
        "finish": finish,
        "memo": memo,
        "created_at": created_at.strftime("%Y-%M-%d %H:%M"),
    })

    # JSONデータ出力
    json.dump(database, open(DATA_FILE, mode="w", encoding="utf-8"), indent=4, ensure_ascii=False)

def load_data():
    """記録データを返す
    """
    try:
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileExistsError:
        database = []
    
    return database

@application.route('/save', methods=['POST'])
def save():
    """記録されたデータを取得します"""
    start = request.form.get('start')
    finish = request.form.get('finish')
    memo = request.form.get('memo')
    create_at = datetime.now()
    save_data(start, finish, memo, create_at)

    return redirect('/')

@application.template_filter('n12br')
def n12br_filter(s):
    """改行文字をbrタグに置き換えるテンプレートフィルタ
    """
    return escape(s).replace('¥n', Markup('<br>'))

@application.route('/')
def index():
    """トップページの表示
    """
    rides = load_data()
    return render_template('index.html', rides=rides)

if __name__ == '__main__':
    # サーバ起動
    application.run('0.0.0.0', 8000, debug=True)
