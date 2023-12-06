import pandas as pd

file_population = 'data2/행정안전부_지역별(행정동) 성별 연령별 주민등록 인구수_20230930.csv'
df_pop = pd.read_csv(file_population, encoding='euc-kr', low_memory=False)
#시도명으로 그룹화, 필요없는 칼럼 drop
df_pop_group = df_pop.groupby('시도명').mean()
df_pop_group = df_pop_group.drop(['행정기관코드'], axis=1)
#인구수이므로 int형으로 형변환
df_pop_group = df_pop_group.astype(int)

# 세대별 연령층 칼럼을 만들고 초기화
for i in range(11):
    df_pop_group[f'{i*10}대남자'] = 0
    df_pop_group[f'{i*10}대여자'] = 0

# 연령별 나이를 ~대로 나누기
for i in range(10):
    for gender in ['남자', '여자']:
        name = f'만{i}세{gender}'
        df_pop_group[f'0대{gender}'] += df_pop_group[name]

        name = f'만{i+10}세{gender}'
        df_pop_group[f'{(i+1)*10}대{gender}'] += df_pop_group[name]

# 만 70세 이상부터는 나머지로 합치기
df_pop_group['70세이상남자'] = df_pop_group.loc[:, '70대남자':].sum(axis=1)
df_pop_group['70세이상여자'] = df_pop_group.loc[:, '70대여자':].sum(axis=1)

# 필터링되지 않은 만 나이 데이터를 드롭하기
df_pop_group = df_pop_group[df_pop_group.columns.drop(list(df_pop_group.filter(like='만')))]

#70대부터 100대 남자,여자 칼럼 드롭하기
for i in range(7,11):
    df_pop_group = df_pop_group[df_pop_group.columns.drop(list(df_pop_group.filter(like=f'{i}0대남자')))]
    df_pop_group = df_pop_group[df_pop_group.columns.drop(list(df_pop_group.filter(like=f'{i}0대여자')))]
#출력하여 확인
print(df_pop_group)

# 결과 데이터프레임을 CSV 파일로 저장
df_pop_group.to_csv('data2/df_pop_data.csv', index=True)