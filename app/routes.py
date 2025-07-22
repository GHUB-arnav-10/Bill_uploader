import os
import re
import json
import csv
from io import StringIO
from datetime import datetime, date
from flask import (
    Blueprint, render_template, request, flash, redirect, url_for,
    current_app, jsonify, Response
)
from werkzeug.utils import secure_filename
from sqlalchemy import or_

from app import db
from app.models import Receipt
from app.utils import allowed_file, extract_data_with_donut, get_dashboard_analytics

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['GET'])
def index():
    
    query = request.args.get('q', '', type=str)
    sort_by = request.args.get('sort_by', 'transaction_date', type=str)
    order = request.args.get('order', 'desc', type=str)

    receipt_query = Receipt.query

    
    if query:
        search_term = f"%{query}%"
        receipt_query = receipt_query.filter(
            or_(
                Receipt.vendor.ilike(search_term),
                Receipt.category.ilike(search_term)
            )
        )

   
    if sort_by == 'vendor':
        order_by_col = Receipt.vendor
    elif sort_by == 'amount':
        order_by_col = Receipt.amount
    else: 
        order_by_col = Receipt.transaction_date

    
    if order == 'asc':
        receipt_query = receipt_query.order_by(order_by_col.asc())
    else:
        receipt_query = receipt_query.order_by(order_by_col.desc())

    receipts = receipt_query.all()
    analytics = get_dashboard_analytics(receipts)

    return render_template(
        'index.html',
        receipts=receipts,
        analytics=analytics,
        query=query,
        sort_by=sort_by,
        order=order
    )


@main.route('/upload', methods=['POST'])
def upload_file():
   
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('main.index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('main.index'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        
        extracted_data = extract_data_with_donut(filepath)

        if extracted_data:
            try:
                
                new_receipt = Receipt(
                    vendor=extracted_data['vendor'],
                    transaction_date=extracted_data['transaction_date'],
                    amount=extracted_data['amount'],
                    category=extracted_data.get('category', 'Uncategorized'),
                    file_name=filename
                )
                db.session.add(new_receipt)
                db.session.commit()
                flash('Receipt processed and saved successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error saving receipt to database: {e}', 'danger')
        else:
            flash('Could not extract data from the document using Donut.', 'danger')
            
        return redirect(url_for('main.index'))

    else:
        flash('File type not allowed.', 'danger')
        return redirect(url_for('main.index'))




@main.route('/export/csv')
def export_csv():
    """
    Exports the current view of receipts to a CSV file.
    """
    receipts = Receipt.query.order_by(Receipt.transaction_date.desc()).all()
    
    si = StringIO()
    cw = csv.writer(si)
    
    
    cw.writerow(['ID', 'Vendor', 'Date', 'Amount', 'Category', 'Uploaded At'])
    
    
    for r in receipts:
        cw.writerow([r.id, r.vendor, r.transaction_date, r.amount, r.category, r.uploaded_at])
        
    output = si.getvalue()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=receipts_export.csv"}
    )


@main.route('/export/json')
def export_json():
   
    receipts = Receipt.query.order_by(Receipt.transaction_date.desc()).all()
    receipts_as_dicts = [r.to_dict() for r in receipts]
    
    return jsonify(receipts_as_dicts)
