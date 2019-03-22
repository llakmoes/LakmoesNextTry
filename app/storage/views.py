from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import storage
from .forms import RecordForm
from ..models import Record
from .. import db


@storage.route('/storage', methods=['GET', 'POST'])
@login_required
def list_records():

    records = Record.query.all()

    return render_template('admin/departments/departments.html',
                           records=records, title="Departments")


@storage.route('/record/add')
def add_records():
    add_record = True

    form = RecordForm()
    if form.validate_on_submit():
        record = Record(name=form.name.data,
                      description=form.description.data)

        try:
            # add role to the database
            db.session.add(record)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_record=add_record,
                           form=form, title='Add Record')


@storage.route('/record/edit/<int:id')
@login_required
def edit_records(id):
    add_record = False

    record = Record.query.get_or_404(id)
    form = RecordForm(obj=record)
    if form.validate_on_submit():
        record.name = form.name.data
        record.description = form.description.data
        db.session.add(record)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = record.description
    form.name.data = record.name
    return render_template('admin/roles/role.html', add_record=add_record,
                           form=form, title="Edit Record")


@storage.route('/record/delete/<int:id>')
@login_required
def delete_records(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Record")
