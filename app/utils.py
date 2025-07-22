import os
import json
import re
from PIL import Image
from pydantic import BaseModel, Field, ValidationError
from datetime import date, datetime
from typing import Optional, Any
from flask import current_app


from app.donut_service import convert_file_to_image


class ReceiptData(BaseModel):
    """
    Pydantic model to validate the structured data extracted from a receipt.
    """
    vendor: str = Field(..., description="The name of the vendor or store.")
    transaction_date: date = Field(..., description="The transaction date in YYYY-MM-DD format.")
    amount: float = Field(..., description="The total amount of the transaction.")
    category: Optional[str] = Field(None, description="A suggested category for the expense (e.g., Groceries, Utilities).")


def extract_data_with_donut(file_path: str) -> Optional[dict]:
    """
    Uses the Donut model to extract structured data from a receipt file.
    This version is specifically adapted to parse the output of the
    'naver-clova-ix/donut-base-finetuned-cord-v2' model.
    """
    try:
        donut_service = current_app.donut_service
        task_prompt = current_app.config['DONUT_TASK_PROMPT']
        
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            file_name = os.path.basename(file_path)
            
            image = convert_file_to_image(file_bytes, file_name)
            result = donut_service.analyze(image, task_prompt)

            if result['status'] == 'success':
                extracted_json = result['data']
                print(f"Donut raw extraction: {json.dumps(extracted_json, indent=2)}")

                
                
                
                
                vendor_name = "N/A"
                if 'menu' in extracted_json and isinstance(extracted_json['menu'], list):
                    for item in extracted_json['menu']:
                        
                        if isinstance(item, dict) and 'nm' in item and 'price' not in item and 'cnt' not in item:
                            vendor_name = item['nm']
                            break 
                
                
                total_amount_str = "0"
                if 'total' in extracted_json and isinstance(extracted_json['total'], dict):
                    total_amount_str = str(extracted_json['total'].get('total_price', '0'))
                elif 'paymentinfo' in extracted_json and isinstance(extracted_json['paymentinfo'], dict):
                     total_amount_str = str(extracted_json['paymentinfo'].get('price', '0'))

                
                amount_val = float(re.sub(r'[^\d.]', '', total_amount_str)) if total_amount_str else 0.0
                
                
                transaction_dt = date.today() 
                if 'meta' in extracted_json and isinstance(extracted_json['meta'], dict):
                    date_str = extracted_json['meta'].get('date')
                    if date_str:
                        try:
                            
                            transaction_dt = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except ValueError:
                            try:
                                transaction_dt = datetime.strptime(date_str, '%m/%d/%Y').date()
                            except ValueError:
                                print(f"Could not parse date: {date_str}")
                
                receipt_info = {
                    "vendor": vendor_name,
                    "transaction_date": transaction_dt,
                    "amount": amount_val,
                    "category": "Dining" 
                }
                
                validated_data = ReceiptData(**receipt_info).model_dump()
                return validated_data
            else:
                print(f"Donut analysis failed: {result.get('message')}")
                return None

    except Exception as e:
        print(f"An error occurred during Donut extraction: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_dashboard_analytics(receipts: list) -> dict:
    """
    Computes various statistics and prepares data for charts.
    """
    if not receipts:
        return {
            'total_spend': 0,
            'avg_spend': 0,
            'receipt_count': 0,
            'spend_by_category': {},
            'spend_over_time': {}
        }

    total_spend = sum(r.amount for r in receipts)
    receipt_count = len(receipts)
    avg_spend = total_spend / receipt_count if receipt_count > 0 else 0

    spend_by_category = {}
    for r in receipts:
        category = r.category or 'Uncategorized'
        spend_by_category[category] = spend_by_category.get(category, 0) + r.amount

    spend_over_time = {}
    for r in receipts:
        if r.transaction_date:
            month_key = r.transaction_date.strftime('%Y-%m')
            spend_over_time[month_key] = spend_over_time.get(month_key, 0) + r.amount
    
    spend_over_time = dict(sorted(spend_over_time.items()))

    return {
        'total_spend': total_spend,
        'avg_spend': avg_spend,
        'receipt_count': receipt_count,
        'spend_by_category': spend_by_category,
        'spend_over_time': spend_over_time
    }


def allowed_file(filename):
    """Checks if a file's extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
