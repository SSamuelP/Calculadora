def convert_decimal_to_base(decimal, base, precision=5):
    result = ""
    for _ in range(precision):
        decimal *= base
        digit = int(decimal)
        result += str(digit)
        decimal -= digit
    return result

def convert_to_bases(number):
    try:
        decimal = float(number)
        integer_part = int(decimal)
        decimal_part = decimal - integer_part

        binary_int = bin(integer_part)[2:]
        octal_int = oct(integer_part)[2:]
        hexadecimal_int = hex(integer_part)[2:]

        binary_decimal = convert_decimal_to_base(decimal_part, 2)
        octal_decimal = convert_decimal_to_base(decimal_part, 8)
        hexadecimal_decimal = convert_decimal_to_base(decimal_part, 16)

        return {
            'binary': f"{binary_int}.{binary_decimal}",
            'octal': f"{octal_int}.{octal_decimal}",
            'hexadecimal': f"{hexadecimal_int}.{hexadecimal_decimal}"
        }
    except ValueError:
        return {'error': 'Entrada inválida'}