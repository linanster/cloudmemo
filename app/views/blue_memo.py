from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required
from sqlalchemy import asc
from flask_paginate import Pagination, get_page_parameter
import math
#
from app.models.mysql import MemoRecord, MemoType
#
blue_memo = Blueprint('blue_memo', __name__, url_prefix='/memo')

@blue_memo.route('/')
@blue_memo.route('/index/')
@login_required
def vf_index():
    # records = MemoRecord.query.all()
    # records = MemoRecord.query.order_by(asc(MemoRecord.id)).all()
    myquery_mysql_memorecord = MemoRecord.query.order_by(asc(MemoRecord.id))
    # pagination code
    total_count = myquery_mysql_memorecord.count()
    PER_PAGE = 10
    page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    # start/end is like 0/100, 100/200, .etc
    start = (page-1)*PER_PAGE
    end = page * PER_PAGE if total_count > page * PER_PAGE else total_count
    pagination = Pagination(page=page, total=total_count, per_page=PER_PAGE, bs_version=3)
    records = myquery_mysql_memorecord.slice(start, end)
    return render_template('memo_index.html', pagination = pagination, page=page, records = records)

@blue_memo.route('/edit/')
@login_required
def edit():
    recordid = request.args.get('recordid')
    # edit
    if recordid:
        record = MemoRecord.query.get(recordid)
        typecode = record.typecode
        summary = record.summary
        comment = record.comment
        page = request.args.get('page')
        params = {
            'page': page,
            'recordid': recordid,
            'typecode': typecode,
            'summary': summary,
            'comment': comment,
        }
    # new
    else:
        params = {}
    return render_template('memo_edit.html', **params)

@blue_memo.route('/cmd_save/', methods=['get', 'post'])
@login_required
def cmd_save():
    recordid = request.args.get('recordid', None)
    typecode = request.form.get('typecode')
    summary = request.form.get('summary')
    comment = request.form.get('comment')
    # edit
    if recordid:
        record = MemoRecord.query.get(recordid)
        record.typecode = typecode
        record.summary = summary
        record.comment = comment
        page = request.args.get('page')
    # new
    else:
        record = MemoRecord(typecode, summary, comment)
        total_count = MemoRecord.query.count() + 1
        PER_PAGE = 10
        page = math.ceil(total_count/PER_PAGE)
    record.save()
    return redirect(url_for('blue_memo.vf_index', page=page))

@blue_memo.route('/cmd_delete/')
@login_required
def cmd_delete():
    recordid = request.args.get('recordid')
    page = request.args.get('page')
    record = MemoRecord.query.get(recordid)
    record.delete()
    return redirect(url_for('blue_memo.vf_index', page=page))
