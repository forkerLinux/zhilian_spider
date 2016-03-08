#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-

from random import randint
import json
from flask import Flask, make_response, request, redirect, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from process.zhilian import Zhilian
from models import ResumeSource, db

app = Flask(__name__)
zhilian = Zhilian()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        validcode = request.form.get('validcode', None)
        zhilian.login(validcode)
        return render_template('search.html')

    # GET method
    ret = '''<img src="/validcode?r=%d" >''' % randint(1,99999)
    ret += '''<form action="#" method="post" >'''
    ret += '''<input type="text" id="validcode" name="validcode" />'''
    ret += '''<input type="submit" />'''
    ret += '''</form>'''
    return ret


@app.route('/validcode')
def validcode():
    resp = zhilian.load_login().read()
    response = make_response(resp)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@app.route('/search', methods=['POST', ])
def show_result():
    keyword = request.form['keyword']
    edu_min = request.form.get('edu_min', None)
    edu_max = request.form.get('edu_max', None)

    search_param = {
        'keyword': keyword,
        'edu_min': edu_min,
        'edu_max': edu_max,
    }

    result_list, pageinfo = zhilian.search_cv(**search_param)
    ret = {
        'result_list': result_list,
        'pageinfo': pageinfo,
    }
    return render_template('show_result.html', **ret)


@app.route('/api/skip_nearby', methods=['POST', ])
def skip_nearby():
    """ 跳转下一页，上一页
    """
    post_data = request.get_json()
    ret_dict = {
        'errcode': 1,
        'errmsg': 'unknown error'
    }
    if len(post_data) != 1:
        return json.dumps(ret_dict)

    assert_type_tuple = ('next', 'prev')
    if post_data['type'] not in assert_type_tuple:
        ret_dict['errmsg'] = 'param error'
        return json.dumps(ret_dict)

    if post_data['type'] == 'next':
        result_list, pageinfo = zhilian.go_next()
    else:
        result_list, pageinfo = zhilian.go_prev()

    ret_dict = {
        'errcode': 0,
        'errmsg': 'ok',
        'items': result_list,
        'pageinfo': pageinfo,
    }

    return json.dumps(ret_dict)


@app.route('/cv_detail/<cv_id>')
def cv_detail(cv_id):
    html_content = zhilian.get_cv_page(cv_id)
    ret = {
        'html_content': html_content,
        'cv_id': cv_id,
    }

    return render_template('cv_detail.html', **ret)


@app.route('/add_cv/<cv_id>')
def add_cv(cv_id):
    try:
        resume = ResumeSource(cv_id, 'zhilian')
        db.session.add(resume)
        db.session.commit()
        return '添加成功'
    except Exception as e:
        db.session.rollback()
        raise e
        return '添加失败'


@app.route('/query')
def query():
    return 'query'

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=False)
