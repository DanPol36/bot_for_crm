import os
from typing import List, Dict, Any, Optional

_ENGINE = None


def _init_engine():
    global _ENGINE
    if _ENGINE:
        return _ENGINE
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        return None
    try:
        # prefer SQLAlchemy if available
        from sqlalchemy import create_engine
        try:
            _ENGINE = create_engine(db_url, pool_pre_ping=True)
            return _ENGINE
        except Exception:
            # Try switching common psycopg driver name if present in URL
            if '+psycopg' in db_url and '+psycopg2' not in db_url:
                try:
                    alt = db_url.replace('+psycopg', '+psycopg2')
                    _ENGINE = create_engine(alt, pool_pre_ping=True)
                    return _ENGINE
                except Exception:
                    _ENGINE = None
                    return None
            _ENGINE = None
            return None
    except Exception:
        _ENGINE = None
        return None


def get_engine():
    return _init_engine()


def _fetch_all(sql: str, params: Optional[dict] = None) -> List[Dict[str, Any]]:
    eng = get_engine()
    if not eng:
        raise RuntimeError('No database engine configured (set DATABASE_URL)')
    from sqlalchemy import text
    with eng.connect() as conn:
        res = conn.execute(text(sql), params or {})
        rows = [dict(r) for r in res.mappings().all()]
    return rows


def get_clients() -> List[Dict[str, Any]]:
    sql = '''
        SELECT
            "ФИО" AS fio,
            "Пол" AS gender,
            "Адрес" AS address,
            "Возраст" AS age,
            COALESCE("Номер_телефона", '') AS phone,
            "Почта" AS email
        FROM practic2
        ORDER BY "ФИО"
        LIMIT 1000
    '''
    return _fetch_all(sql)


def get_person(fio: str) -> Dict[str, Any]:
    sql = '''
        SELECT
            "ФИО" AS fio,
            "Пол" AS gender,
            "Адрес" AS address,
            "Возраст" AS age,
            "Дата_рождения"::text AS birth_date,
            COALESCE("Номер_телефона", '') AS phone,
            "Почта" AS email,
            "Примечания" AS notes
        FROM practic2
        WHERE "ФИО" = :fio
        LIMIT 1
    '''
    rows = _fetch_all(sql, {'fio': fio})
    return rows[0] if rows else {}


def get_orders(fio: str) -> List[Dict[str, Any]]:
    # Try to find orders in order2 table by matching fio or phone
    eng = get_engine()
    if not eng:
        raise RuntimeError('No database engine configured (set DATABASE_URL)')
    from sqlalchemy import text
    # first load person phone
    p_sql = 'SELECT COALESCE("Номер_телефона", '') AS phone, "ФИО" AS fio FROM practic2 WHERE "ФИО" = :fio LIMIT 1'
    with eng.connect() as conn:
        prow = conn.execute(text(p_sql), {'fio': fio}).mappings().one_or_none()
        if not prow:
            return []
        phone = prow.get('phone') or ''
        digits = ''.join(ch for ch in phone if ch.isdigit())
        # detect client column in order2
        col_q = text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'order2' AND (column_name ILIKE '%клиент%' OR column_name ILIKE '%client%')
            ORDER BY ordinal_position LIMIT 1
        """)
        col_res = conn.execute(col_q).fetchone()
        client_col = col_res[0] if col_res else None
        if not client_col:
            return []
        orders_sql = text(f'''
            SELECT * FROM order2
            WHERE COALESCE("{client_col}", '') = :phone_exact
               OR regexp_replace(COALESCE("{client_col}", ''), '\\D', '', 'g') LIKE :phone_digits
               OR COALESCE("{client_col}", '') = :fio_exact
            ORDER BY 1
        ''')
        params = {'phone_exact': phone, 'phone_digits': f'%{digits}%', 'fio_exact': fio}
        ord_res = conn.execute(orders_sql, params).mappings().fetchall()
        orders = [dict(r) for r in ord_res]
    return orders
