import re
from datetime import datetime

from django.core.exceptions import ValidationError

_product_code_error = ValidationError("JANコードを正しく入力してください")


def validate_product_code(code: str):
    """
    JANコードのバリデーションを行う関数
    """
    if len(code) not in [9, 10, 12, 13]:
        raise _product_code_error

    if re.match(r"^\d+$", code):
        _validate_jan_code(code)
    else:
        _validate_original_code(code)


def _validate_jan_code(code: str):
    # チェックデジットの計算
    if len(code) == 9:
        check_digit = sum(int(code[i]) * (3 if i % 2 == 0 else 1) for i in range(8))
    else:
        check_digit = sum(int(code[i]) * (3 if i % 2 == 1 else 1) for i in range(len(code) - 1))
    check_digit = (10 - check_digit % 10) % 10

    # チェックデジットが正しいか確認
    if int(code[-1]) != check_digit:
        raise _product_code_error


def _validate_original_code(code: str):
    if not "A" <= code[0] <= "Z":
        raise _product_code_error

    try:
        datetime.strptime(code[1:], "%Y%m%d%H%M")
    except ValueError:
        raise _product_code_error
