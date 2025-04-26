import pandas as pd
import time

def create_string(file_path):
    f = open(file_path, 'r', encoding='utf-8')
    text = f.read()
    return text

def create_pattern_dict(pattern):
    chars = list(pattern)  
    df = pd.DataFrame({'symb': chars})
    df = df[::-1].reset_index(drop=True)

    char_min_numbers = {}
    
    for i in range(1, df.shape[0]):
        current_char = df.at[i, 'symb']
        
        if current_char in char_min_numbers:
            df.at[i, 'num'] = char_min_numbers[current_char]
        else:
            new_number = i
            df.at[i, 'num'] = new_number
            char_min_numbers[current_char] = new_number
            
    first_char = df.at[0, 'symb']
    char_count = df['symb'].value_counts()[first_char]

    if char_count == 1:
        df.at[0, 'num'] = len(df)
    else:
        df.at[0, 'num'] = char_min_numbers.get(first_char, 1)

    df = df.drop_duplicates()
    symbol_value_dict = dict(zip(df['symb'], df['num']))
    return symbol_value_dict

def find_pattern_in_text(pattern, text):
    pattern_len = len(pattern)

    for i in range(pattern_len, len(text)):
        j = pattern_len - 1

        while (text[i] == pattern[j]) and (j >= 0):
            i-=1
            j-=1

        if j == -1:
            res = f'Первое вхождение подстроки: {i+1}'
            return res
        elif i in symbol_value_dict:
            num = symbol_value_dict[i]
            i += num
        else:
            i+=pattern_len

    res = 'Подстрока не найдена'
    return

print('============== Bad files ==============')
for n in range(1, 5):

    start = time.perf_counter()

    pattern_path = f'benchmarks/bad_w_{n}.txt'
    pattern = create_string(pattern_path)
    symbol_value_dict = create_pattern_dict(pattern)

    text_path = f'benchmarks/bad_t_{n}.txt'
    text = create_string(text_path)

    result = find_pattern_in_text(pattern, text)

    end = time.perf_counter()

    print()
    print(f'Bad #{n}')
    print(result)
    print(f'Время выполнения: {end - start:.4f} секунд')

print()
print('============== Good files =============')
for n in range(1, 5):

    pattern_path = f'benchmarks/good_w_{n}.txt'
    pattern = create_string(pattern_path)
    symbol_value_dict = create_pattern_dict(pattern)

    text_path = f'benchmarks/good_t_{n}.txt'
    text = create_string(text_path)

    result = find_pattern_in_text(pattern, text)

    end = time.perf_counter()

    print()
    print(f'Good #{n}')
    print(result)
    print(f'Время выполнения: {end - start:.4f} секунд')