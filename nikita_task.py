import os
import re
import jsbeautifier
import random
import string
import logging
import traceback

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def exception(function):
    def wrapper(*args, **kwargs):
        try:
            logging.debug(f"Вызов функции {function.__name__} с аргументами: {args} и ключевыми словами: {kwargs}")
            result = function(*args, **kwargs)
            logging.debug(f"Функция {function.__name__} вернула результат: {result}")
            return result
        except Exception as e:
            logging.error(f"Произошла ошибка в функции {function.__name__}: {e}")
            traceback.print_exc()  # Вывод трассировки стека
            return None
    return wrapper

@exception
def get_js_files(directory):
    js_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".js"):
                js_files.append(os.path.join(root, file))
    return js_files

@exception
def obfuscate_names(code):
    logging.debug("Начало обфускации имен в коде")
    
    def random_string(length=8):
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    keywords = {'function', 'var', 'let', 'const', 'if', 'else', 'for', 'while', 'return', 'console', 'log'}
    
    # Исключаем строки из кода при поиске имен переменных
    # Добавляем отрицательные предпросмотры для игнорирования символов кавычек
    names = re.findall(r'(?<!["\'])\b\w+\b(?!["\'])', code)
    obfuscated_names = {name: random_string() for name in set(names) if name not in keywords and not name.startswith('__')}
    
    for name, obf_name in obfuscated_names.items():
        pattern = re.compile(r'\b' + re.escape(name) + r'\b')
        code = pattern.sub(obf_name, code)
        print(name)
    logging.debug(f"Конец обфускации имен, обфусцированный код: {code}")
    return code


@exception
def remove_comments(code):
    code = re.sub(r'//.*', '', code)  
    code = re.sub(r'/\*[\s\S]*?\*/', '', code)  
    return code

@exception
def beautify_code(code):
    opts = jsbeautifier.default_options()
    opts.indent_size = 2
    return jsbeautifier.beautify(code, opts)

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

@exception
def obfuscate_code(code):
    methods = []
    
    code = remove_comments(code)
    methods.append("remove_comments")
    
    code = obfuscate_names(code)
    methods.append("obfuscate_names")
    
    code = beautify_code(code)
    methods.append("beautify_code")

    code = convert_string_literals_to_unicode(code)
    methods.append("convert_string_literals_to_unicode")
    return code, methods

@exception
def log_obfuscation(file, methods):
    logging.info(f"File: {file} obfuscated using methods: {methods}")

@exception
def generate_report(js_files):
    report = f"Total files processed: {len(js_files)}\n"
    for file in js_files:
        report += f"Processed file: {file}\n"
    with open("obfuscation_report.txt", "w") as report_file:
        report_file.write(report)

@exception
def main(directory):
    logging.info(f"Начало работы скрипта в директории: {directory}")
    js_files = get_js_files(directory)
    logging.debug(f"Найденные JS файлы: {js_files}")
    for js_file in js_files:
        logging.info(f"Обработка файла: {js_file}")
    js_files = get_js_files(directory)
    for js_file in js_files:
        with open(js_file, 'r', encoding='utf-8') as file:
            code = file.read()
        
        obfuscated_code, methods = obfuscate_code(code)
        
        with open(js_file, 'w', encoding='utf-8') as file:
            file.write(obfuscated_code)
        
        log_obfuscation(js_file, methods)
    
    generate_report(js_files)
    logging.info(f"Конец работы скрипта")

if __name__ == "__main__":
    main(r"C:\Users\BigBoss\pract\files")

    
