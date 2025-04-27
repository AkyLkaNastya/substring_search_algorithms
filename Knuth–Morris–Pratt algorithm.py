import pandas as pd
import time

data = pd.read_csv('algorithm_results.csv')

def create_string(file_path):
    f = open(file_path, 'r', encoding='utf-8')
    text = f.read()
    return text

def create_pattern_dataframe(pattern):
    chars = list(pattern)  
    df = pd.DataFrame({'symb': chars})
    df['num'] = None
    for i in range(len(pattern)):
        for j in range(1, i+1):
            flag = True
            for n in range(1, j+1):
                if pattern[n-1] != pattern[(i-j)+n]:
                    flag = False
                    break
            if flag:
                df.loc[i, 'num'] = j

        if pd.isna(df.loc[i, 'num']):
            df.at[i, 'num'] = 0
    return df


def find_pattern_in_text(pattern, df, text):
    j = 0
    pattern_len = len(pattern)

    for i in range(len(text)):
        while (j < pattern_len) and (text[i] == pattern[j]):
            i+=1
            j+=1
        if j == pattern_len:
            result = f'Первое вхождение подстроки: {i - pattern_len}'
            return result
        if j != 0:
            j = df.at[j, 'num']
            i -= 1

    return 'Подстрока не найдена'


print('============== Bad files ==============')
for n in range(1, 5):

    start = time.perf_counter()

    pattern_path = f'benchmarks/bad_w_{n}.txt'
    pattern = create_string(pattern_path)
    pattern_df = create_pattern_dataframe(pattern)

    text_path = f'benchmarks/bad_t_{n}.txt'
    text = create_string(text_path)

    result = find_pattern_in_text(pattern, pattern_df, text)

    end = time.perf_counter()

    time_res = f'{end - start:.6f}'
    data.loc[data['benchmarks'] == f'bad {n}', 'K-M-P'] = time_res

    print()
    print(f'Bad #{n}')
    print(result)
    print(f'Время выполнения: {time_res} секунд')

print()
print('============== Good files =============')
for n in range(1, 5):

    start = time.perf_counter()

    pattern_path = f'benchmarks/good_w_{n}.txt'
    pattern = create_string(pattern_path)
    pattern_df = create_pattern_dataframe(pattern)

    text_path = f'benchmarks/good_t_{n}.txt'
    text = create_string(text_path)

    result = find_pattern_in_text(pattern, pattern_df, text)

    end = time.perf_counter()

    time_res = f'{end - start:.6f}'
    data.loc[data['benchmarks'] == f'good {n}', 'K-M-P'] = time_res

    print()
    print(f'Good #{n}')
    print(result)
    print(f'Время выполнения: {time_res} секунд')

data.to_csv('algorithm_results.csv', index=False)