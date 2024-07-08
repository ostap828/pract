import logging
import re
import traceback

def exception(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            traceback.print_exc()  # Добавляем вывод трассировки стека
            return None
    return wrapper

@exception
def convert_string_literals_to_unicode(code):
    def to_unicode(match):
        string = match.group(1)
        logging.debug(f"Original string: {string}")
        unicode_string = ''.join(r'\\u{:04x}'.format(ord(c)) for c in string)
        logging.debug(f"Unicode string: {unicode_string}")
        return f'"{unicode_string}"'
    
    # Добавляем логирование до и после обработки регулярным выражением
    logging.debug("Before conversion: " + code)
    converted_code = re.sub(r'"([^"]*)"', to_unicode, code)
    logging.debug("After conversion: " + converted_code)
    
    return converted_code
