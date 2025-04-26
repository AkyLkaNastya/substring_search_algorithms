import pandas as pd

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

pattern_path = 'benchmarks/test.txt'

pattern = create_string(pattern_path)
df = create_pattern_dataframe(pattern)

print(df)