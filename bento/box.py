from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bento.auth import login_required
from bento.db import get_db

bp = Blueprint('box', __name__)


@bp.route('/')
def index():
    db = get_db()
    boxes = db.execute(
        'SELECT box.id, name, received, user_id, username'
        ' FROM box JOIN user ON box.user_id = user.id'
        ' ORDER BY received DESC'
    ).fetchall()
    return render_template('box/index.html', boxes=boxes)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO box (user_id, name)'
                ' VALUES (?, ?)',
                (g.user['id'], name)
            )
            db.commit()
            return redirect(url_for('box.index'))
    return render_template('box/create.html')


def get_box(box_id, check_user=True):
    box = get_db().execute(
        'SELECT box.id, name, received, user_id, username'
        ' FROM box JOIN user on box.user_id = user.id'
        ' WHERE box.id = ?',
        (box_id,)
    ).fetchone()

    if box is None:
        abort(404, f"Box id {box_id} doesn't exist.")

    if check_user and box['user_id'] != g.user['id']:
        abort(403)

    return box


@bp.route('/<int:box_id>/update', methods=('GET', 'POST'))
@login_required
def update(box_id):
    box = get_box(box_id)

    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE box set name = ?'
                ' WHERE id = ?',
                (name, box_id)
            )
            db.commit()
            return redirect(url_for('box.index'))
        
    return render_template('box/update.html', box=box)


@bp.route('/<int:box_id>/delete', methods=('POST',))
@login_required
def delete(box_id):
    get_box(box_id)
    db = get_db()
    db.execute('DELETE FROM box WHERE id = ?', (box_id,))
    db.commit()
    return redirect(url_for('box.index'))
