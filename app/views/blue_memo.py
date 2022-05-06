from flask import Blueprint, request, render_template, redirect, url_for, flash, send_from_directory, session
from flask_login import login_required
from sqlalchemy import asc
from flask_paginate import Pagination, get_page_parameter
from werkzeug.utils import secure_filename
import os
import math
#
from app.models.mysql import MemoRecord, MemoType, MemoFile, MemoComment
from app.myglobals import uploadfolder
#
blue_memo = Blueprint('blue_memo', __name__, url_prefix='/memo')

PER_PAGE = 30

@blue_memo.route('/')
@blue_memo.route('/index/')
@login_required
def index():
    # records = MemoRecord.query.all()
    # records = MemoRecord.query.order_by(asc(MemoRecord.id)).all()
    myquery_mysql_memorecord = MemoRecord.query.order_by(asc(MemoRecord.id))
    # pagination code
    total_count = myquery_mysql_memorecord.count()
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
        memorecord = MemoRecord.query.get(recordid)
        memocomment = memorecord.comments[0]
        typecode = memorecord.typecode
        summary = memorecord.summary
        author = memorecord.author
        comment = memocomment.comment
        files = memorecord.files
        page = request.args.get('page')
        params = {
            'page': page,
            'recordid': recordid,
            'typecode': typecode,
            'summary': summary,
            'author': author,
            'comment': comment,
            'files': files,
        }
    # new
    else:
        params = {}
        # record = 0
    return render_template('memo_edit.html', **params)

@blue_memo.route('/cmd_save/', methods=['get', 'post'])
@login_required
def cmd_save():
    recordid = request.args.get('recordid', None)
    typecode = request.form.get('typecode')
    summary = request.form.get('summary')
    comment = request.form.get('comment')
    memorecord = None
    memocomment = None
    # edit
    if recordid:
        memorecord = MemoRecord.query.get(recordid)
        memocomment = memorecord.comments[0]
        memorecord.typecode = typecode
        memorecord.summary = summary
        memocomment.comment = comment
        page = request.args.get('page')
        memorecord.save()
        memocomment.save()
    # new
    else:
        try:
            author = session.get('username')
        except:
            author = ''
        memorecord = MemoRecord(typecode, summary, author)
        memorecord.save()
        memocomment = MemoComment(memorecord.id, comment)
        memocomment.save()
        total_count = MemoRecord.query.count() + 1
        page = math.ceil(total_count/PER_PAGE)
    return redirect(url_for('blue_memo.index', page=page))

@blue_memo.route('/cmd_delete/')
@login_required
def cmd_delete():
    recordid = request.args.get('recordid')
    page = request.args.get('page')
    # 1. delete correlated momefile
    memofiles = MemoFile.query.filter_by(memorecordid=recordid)
    # version1: only delete db
    # [memofile.delete() for memofile in memofiles]
    # version2: delete db and file
    for memofile in memofiles:
        # step1: delete file
        fullname = os.path.join(uploadfolder, memofile.filename)
        os.remove(fullname)
        # step2: delete database record
        memofile.delete()
    # 2. delete correlated memocomment
    memocomments = MemoComment.query.filter_by(memorecordid=recordid)
    [memocomment.delete() for memocomment in memocomments]
    # 3. delete self
    memofile = MemoRecord.query.get(recordid)
    memofile.delete()
    return redirect(url_for('blue_memo.index', page=page))

###################
#### filezella ####
###################

@blue_memo.route('/cmd_upload/', methods=['post'])
@login_required
def cmd_upload():
    recordid = request.args.get('recordid')
    page = request.args.get('page')
    uploadfile = request.files.get('file')
    if uploadfile.filename == '':
        flash('no file selected')
        pass
    if uploadfile:
        # 1.save file
        filename = secure_filename(uploadfile.filename)
        fullname = os.path.join(uploadfolder, filename)
        uploadfile.save(fullname)
        # 2.update database
        # 2.1 clean record with same recordid and filename
        fs = MemoFile.query.filter_by(memorecordid=recordid, filename=filename)
        for f in fs:
            f.delete()
        # 2.2 insert a new record
        memofile = MemoFile(recordid, filename, False)
        memofile.save()
    return redirect(url_for('blue_memo.edit', recordid=recordid, page=page))

@blue_memo.route('/cmd_download/', methods=['get'])
@login_required
def cmd_download():
    filename = request.args.get('filename')
    return send_from_directory(uploadfolder, filename, as_attachment=True)

@blue_memo.route('/cmd_deletefile/', methods=['get'])
@login_required
def cmd_deletefile():
    filename = request.args.get('filename')
    recordid = request.args.get('recordid')
    page = request.args.get('page')
    # version1: mark this file as deleted, not really do
    # memofile = MemoFile.query.filter_by(memorecordid=recordid, filename=filename).first()
    # memofile.deleted = True
    # memofile.save()
    # version2: do delete
    # step1: delete file
    fullname = os.path.join(uploadfolder, filename)
    os.remove(fullname)
    # step2: delete database record
    memofile = MemoFile.query.filter_by(memorecordid=recordid, filename=filename).first()
    memofile.delete()

    return redirect(url_for('blue_memo.edit', recordid=recordid, page=page))
    

