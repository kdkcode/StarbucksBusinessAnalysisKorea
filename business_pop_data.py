import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#폰트 깨짐을 방지하기 위해 입력
os_name = input('OS환경을 입력하세요(1.mac, 2.window): ')

#아래 파일에서 가공한 파일들 입력으로 받기
file_business = 'data/business_data.csv'
file_pop = 'data2/df_pop_data.csv'

df_pop = pd.read_csv(file_pop, low_memory=False)
print(df_pop)
df_bs = pd.read_csv(file_business, low_memory=False)

#상호명이 스타벅스인 데이터 가공 및 출력
starbucks_data = df_bs[df_bs['상호명'].str.contains('스타벅스', na=False)]
print(starbucks_data)

# 시도명으로 그룹화하고 스타벅스 개수 세서 출력
df_starbucks = starbucks_data.groupby('시도명').size().reset_index(name='스타벅스_지점_개수')
print(df_starbucks)

# seaborn을 이용한 barplot 그리기
# os 마다 다른 폰트를 성정해줘야 한글이 제대로 나옴
if os_name == 'mac':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumBarunGothic'

#스타벅스 지점개수의 지역별 분포 확인을 위한 그래프
plt.figure(figsize=(12, 6))
sns.barplot(x='스타벅스_지점_개수', y='시도명', data=df_starbucks, palette='viridis')
plt.title('스타벅스 지점 개수 분포')
plt.xlabel('스타벅스 지점 개수')
plt.ylabel('시도명')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.show()


# 스타벅스 지점 개수를 데이터 프레임화 하기
starbucks_count_by_region = pd.DataFrame({
    '시도명': ['강원도', '경기도', '경상남도', '경상북도', '광주', '대구', '대전', '부산', '서울', '세종', '울산', '인천', '전라남도', '전라북도', '제주', '충청남도', '충청북도'],
    '스타벅스_지점_개수': [72, 696, 142, 116, 112, 138, 98, 238, 936, 14, 58, 134, 48, 54, 50, 80, 60]
})

# 지역별 평균 소득을 데이터 프레임화하기
avg_income_by_region = pd.DataFrame({
    '시도명': ['강원도', '경기도', '경상남도', '경상북도', '광주', '대구', '대전', '부산', '서울', '세종', '울산', '인천', '전라남도', '전라북도', '제주', '충청남도', '충청북도'],
    '평균소득월액': [1268324.50, 1374013.32, 1238354.44, 1237611.04, 1300559.50, 1322809.89, 1288168.80, 1304940.94, 1417313.44, 1348116.00, 1316547.60, 1339170.20, 1207099.23, 1197758.71, 1296596.00, 1296546.00, 1282512.82],
})

# 두개의 데이터 프레임을 합치기, 시도명 기준
income_starbucks_count_data = pd.merge(starbucks_count_by_region, avg_income_by_region, on='시도명', how='left')

# 두 변수의 상관관계를 알아보기 위한 산점도 그래프 그리기
plt.figure(figsize=(12, 8))
sns.scatterplot(x='스타벅스_지점_개수', y='평균소득월액', data=income_starbucks_count_data, hue='시도명', palette='viridis', s=100)
plt.title('산점도 : 스타벅스 지점 개수 vs. 지역별 평균소득')
plt.xlabel('스타벅스 지점수')
plt.ylabel('평균 소득 (원)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


# 스타벅스 지점수, 소득, 연령, 성별 등의 상관계수를 알아보기 위해 이전의 데이터들을 긁어와서 프레임화
starbucks_count_by_region = pd.DataFrame({
    '시도명': ['강원도', '경기도', '경상남도', '경상북도', '광주', '대구', '대전', '부산', '서울', '세종', '울산', '인천', '전라남도', '전라북도', '제주', '충청남도', '충청북도'],
    '스타벅스_지점_개수': [72, 696, 142, 116, 112, 138, 98, 238, 936, 14, 58, 134, 48, 54, 50, 80, 60],
    '평균소득월액': [1268324.50, 1374013.32, 1238354.44, 1237611.04, 1300559.50, 1322809.89, 1288168.80, 1304940.94, 1417313.44, 1348116.00, 1316547.60, 1339170.20, 1207099.23, 1197758.71, 1296596.00, 1296546.00, 1282512.82],
    '남자': [3969, 11985, 5290, 3859, 7244, 7688, 8786, 7851, 10686, 8010, 10130, 9400, 2819, 3602, 7872, 5189, 5299],
    '여자': [3920, 11836, 5216, 3782, 7425, 7954, 8830, 8249, 11396, 8070, 9586, 9391, 2775, 3635, 7855, 4941, 5120],
    '10대남자': [31, 117, 48, 33, 70, 66, 79, 63, 78, 117, 97, 82, 23, 30, 82, 46, 45],
    '10대여자': [30, 112, 55, 31, 74, 72, 87, 66, 83, 124, 108, 91, 25, 34, 91, 49, 47],
    '20대남자': [34, 125, 56, 35, 80, 75, 88, 69, 88, 123, 108, 94, 26, 35, 91, 52, 50],
    '20대여자': [33, 119, 52, 32, 74, 72, 80, 66, 83, 118, 100, 86, 25, 33, 87, 49, 47],
    '30대남자': [35, 124, 56, 35, 80, 75, 88, 69, 88, 123, 108, 94, 26, 35, 91, 52, 50],
    '30대여자': [33, 119, 52, 32, 74, 72, 80, 66, 83, 118, 100, 86, 25, 33, 87, 49, 47],
    '40대남자': [33, 117, 49, 32, 76, 70, 83, 67, 80, 119, 100, 88, 24, 31, 88, 51, 48],
    '40대여자': [31, 112, 52, 30, 72, 69, 80, 63, 77, 115, 92, 84, 23, 30, 87, 46, 45],
    '50대남자': [35, 122, 54, 34, 81, 75, 86, 66, 91, 122, 105, 89, 26, 36, 89, 51, 46],
    '50대여자': [33, 117, 51, 32, 75, 70, 84, 63, 86, 117, 99, 86, 24, 34, 86, 48, 43],

})


# 흰색 그리드 설정
sns.set(style="whitegrid")
# 한글 폰트 깨짐 방지
if os_name == 'mac':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumBarunGothic'
# 상관 계수 행렬 계산
correlation_matrix = starbucks_count_by_region.corr()

# 상관 계수 히트맵 그리기
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
plt.title('상관 계수 히트맵')
plt.show()