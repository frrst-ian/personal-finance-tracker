from . import storage
from datetime import datetime


def _validate_text(value, name):
    if not isinstance(value, str) or not value.strip():
        return f"{name} must not be empty"
    return None


def _validate_amount(value):
    try:
        v = float(value)
    except Exception:
        return 'Amount must be a number'
    if v <= 0:
        return 'Amount must be positive'
    return None


def validate_input(description, amount, extra_value, extra_key_name):
    err = _validate_text(description, 'Description') or _validate_amount(amount) or _validate_text(extra_value, extra_key_name.capitalize())
    return {"success": False, "error": err} if err else {"success": True}


def _next_id(data):
    return max((t.get('id', 0) for t in data.get('transactions', [])), default=0) + 1


def add_expense(description, amount, category='General'):
    v = validate_input(description, amount, category, 'category')
    if not v['success']:
        return v
    data = storage.load_data()
    new = {
        'id': _next_id(data),
        'type': 'expense',
        'description': description.strip(),
        'amount': float(amount),
        'category': (category or 'General').strip(),
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    data.setdefault('transactions', []).append(new)
    saved = storage.save_data(data)
    return {"success": saved, "transaction": new} if saved else {"success": False, "error": 'Failed to save file'}


def add_income(description, amount, source='General'):
    v = validate_input(description, amount, source, 'source')
    if not v['success']:
        return v
    data = storage.load_data()
    new = {
        'id': _next_id(data),
        'type': 'income',
        'description': description.strip(),
        'amount': float(amount),
        'source': (source or 'General').strip(),
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    data.setdefault('transactions', []).append(new)
    saved = storage.save_data(data)
    return {"success": saved, "transaction": new} if saved else {"success": False, "error": 'Failed to save file'}


def get_all_transactions():
    data = storage.load_data()
    return data.get('transactions', [])


def get_summary():
    tx = get_all_transactions()
    total_income = sum(t.get('amount', 0.0) for t in tx if t.get('type', '').lower() == 'income')
    total_expense = sum(t.get('amount', 0.0) for t in tx if t.get('type', '').lower() == 'expense')
    categories = {}
    sources = {}
    for t in tx:
        if t.get('type', '').lower() == 'expense':
            cat = t.get('category', 'General')
            categories[cat] = categories.get(cat, 0.0) + float(t.get('amount', 0.0))
        elif t.get('type', '').lower() == 'income':
            src = t.get('source', 'General')
            sources[src] = sources.get(src, 0.0) + float(t.get('amount', 0.0))
    return {
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'net_balance': float(total_income) - float(total_expense),
        'categories': categories,
        'income_sources': sources
    }


def list_transactions(limit=10, category=None, source=None, from_date=None, to_date=None):
    tx = get_all_transactions()
    if not tx:
        print('\nNo transactions found.\n')
        return

    # normalize filters
    cat_f = category.lower() if category else None
    src_f = source.lower() if source else None

    filtered = []
    for t in tx:
        ttype = t.get('type', '').lower()
        cat = t.get('category', '').lower()
        src = t.get('source', '').lower()

        if cat_f and not (cat == cat_f):
            # if user supplied category but this is income, skip
            if ttype == 'income':
                continue
        if src_f and not (src == src_f):
            # if user supplied source but this is expense, skip
            if ttype == 'expense':
                continue
        # If both provided, ensure either matches
        if cat_f and src_f:
            if not (cat == cat_f or src == src_f):
                continue

        # date filters
        try:
            if from_date:
                from_dt = datetime.strptime(from_date, '%Y-%m-%d')
                if datetime.strptime(t['date'], '%Y-%m-%d') < from_dt:
                    continue
            if to_date:
                to_dt = datetime.strptime(to_date, '%Y-%m-%d')
                if datetime.strptime(t['date'], '%Y-%m-%d') > to_dt:
                    continue
        except ValueError:
            print('Invalid date format. Use YYYY-MM-DD')
            return

        filtered.append(t)

    filtered = filtered[-limit:]
    if not filtered:
        print('\nNo matching transactions.\n')
        return

    # print table
    print("\n+----+------------+-----------+----------------------+--------------+---------------+")
    print("| ID |    Date    |   Type    | Description          |   Amount     | Cat/Source    |")
    print("+----+------------+-----------+----------------------+--------------+---------------+")
    for t in filtered:
        cat_or_src = t.get('category') if t.get('type', '').lower() == 'expense' else t.get('source', 'General')
        print(f"| {t['id']:<2} | {t['date']:<10} | {t['type']:<9} | {t['description'][:20]:<20} | ${float(t['amount']):>10,.2f} | {cat_or_src:<13} |")
    print("+----+------------+-----------+----------------------+--------------+---------------+\n")
