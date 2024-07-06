# 6.2. Модуль pandas
## 1. Длины всех слов - 2
```python
import pandas as pd


def length_stats(text):
    text = pd.Series([text])
    text = text.str.lower()
    text = text.str.replace(r'[^\w\s]', '', regex=True)
    text = text.str.replace(r'\d+', '', regex=True)

    words = text.str.split(expand=True).stack()

    word_lengths = words.to_frame(name='word')
    word_lengths.columns = ['word']
    word_lengths['length'] = word_lengths['word'].str.len()

    word_lengths = word_lengths.drop_duplicates(subset='word')
    word_lengths = word_lengths.set_index('word').sort_index()

    return word_lengths['length'].rename(None).rename_axis(None)
```
## 2. Длины всех слов по чётности
```python
import pandas as pd


def length_stats(text):
    words = sorted(set(''.join([symbol for symbol in text.lower() if symbol.isalpha() or symbol == ' ']).split()))
    data = pd.Series([len(elem) for elem in words], index=words)
    odd_ = data[data % 2 != 0]
    even_ = data[data % 2 == 0]
    return odd_, even_
```
## 3. Чек - 2
```python
import pandas as pd


def cheque(price_list, **kwargs):
    price_df = pd.DataFrame(list(price_list.items()), columns=['product', 'price'])
    kwargs_df = pd.DataFrame(list(kwargs.items()), columns=['product', 'number'])
    result_df = pd.merge(price_df, kwargs_df, on='product', how='inner')
    result_df['cost'] = result_df['price'] * result_df['number']
    return result_df.sort_values('product').reset_index(drop=True)
```
## 4. Акция
```python
import pandas as pd


def cheque(price_list, **kwargs):
    price_df = pd.DataFrame(list(price_list.items()), columns=['product', 'price'])
    kwargs_df = pd.DataFrame(list(kwargs.items()), columns=['product', 'number'])
    result_df = pd.merge(price_df, kwargs_df, on='product', how='inner')
    result_df['cost'] = result_df['price'] * result_df['number']
    return result_df.sort_values('product').reset_index(drop=True)


def discount(df):
    new_df = df.copy()
    new_df.loc[new_df['number'] > 2, 'cost'] *= 0.5
    return new_df
```
## 5. Длинные слова
```python
import pandas as pd


def get_long(data, min_length=5):
    return data[data >= min_length]
```
## 6. Отчёт успеваемости
```python
import pandas as pd


def best(df):
    return df[(df['maths'] >= 4) & (df['physics'] >= 4) & (df['computer science'] >= 4)]
```
## 7. Отчёт неуспеваемости
```python
import pandas as pd


def need_to_work_better(df):
    return df[(df['maths'] < 3) | (df['physics'] < 3) | (df['computer science'] < 3)]
```
## 8. Обновление журнала
```python
import pandas as pd


def update(df):
    data_frame = df.copy()
    data_frame['average'] = data_frame[['maths', 'physics', 'computer science']].sum(axis=1) / 3
    return data_frame.sort_values(['average', 'name'], ascending=[False, True])
```
## 9. Бесконечный морской бой
```python
import pandas as pd

a, b = map(int, input().split())
c, d = map(int, input().split())
data = pd.read_csv('data.csv')
print(data[(a <= data['x']) & (data['x'] <= c) & (d <= data['y']) & (data['y'] <= b)])
```
## 10. Экстремум функции
```python
import pandas as pd
import numpy as np


def values(func, start, end, step):
    index_ = np.arange(start, end + step, step)
    return pd.Series(map(func, index_), index=index_, dtype='float64')


def min_extremum(data):
    return data[data == data.min()].index.min()


def max_extremum(data):
    return data[data == data.max()].index.max()
```
