import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import seaborn as sns
import matplotlib.pyplot as plt
os_name = input('OS환경을 입력하세요(1.mac, 2.window): ')
# 시도 입력 받아서 데이터 불러오기
local = ['강원', '경기', '경남', '경북', '광주', '대구', '대전', '부산', '서울', '세종', '울산',  '인천', '전남', '전북', '제주', '충남', '충북']
print('강원', '경기', '경남', '경북', '광주', '대구', '대전', '부산', '서울', '세종', '울산',  '인천', '전남', '전북', '제주', '충남', '충북', '중에 입력')

#지역을 제대로 입력할 때까지
file_name = input("스타벅스 상권을 분석할 지역을 입력하세요 : ")
while file_name not in local:
    file_name = input("스타벅스 상권을 분석할 지역을 입력하세요(재시도) : ")

file_path = f'data/소상공인시장진흥공단_상가(상권)정보_{file_name}_202212.csv'

try:
    df = pd.read_csv(file_path, low_memory=False)
    # 데이터 확인
    print(df.head())

    # 두 지점 간의 거리를 재는 기능을 하는 haversine_distance 함수 정의
    def haversine_distance(lat1, lon1, lat2, lon2):
        R = 6371.0  # 지구의 반지름 (단위: km)

        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)

        dlon = lon2_rad - lon1_rad #경도 계산
        dlat = lat2_rad - lat1_rad #위도 계산
        #하버 사인 공식을 이용
        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        return distance

    # 필요한 컬럼만 선택
    selected_columns = ['시도명', '상호명', '상권업종중분류명', '경도', '위도']
    # 데이터 전처리
    filtered_df = df[selected_columns]

    # '스타벅스'를 포함하는 데이터 필터링
    starbucks_data = filtered_df[filtered_df['상호명'].str.contains('스타벅스', na=False)]
    print(starbucks_data)
    print(f'스타벅스 점포 수 : {len(starbucks_data)}')

    # 모든 스타벅스의 위도와 경도 가져오기
    starbucks_latitudes = starbucks_data['위도'].tolist()
    starbucks_longitudes = starbucks_data['경도'].tolist()

    # 일정 거리 이내의 데이터 필터링 (1km로 설정)
    nearby_data_list = []

    if len(starbucks_data) > 10:
        print('스타벅스 지점 수가 많을 경우 10개 임의 선정')
        for i in range(10):
            reference_latitude = starbucks_latitudes[i]
            reference_longitude = starbucks_longitudes[i]
            # 1km 이내의 스타벅스 주변 상권 데이터 모으기
            nearby_data = filtered_df[filtered_df.apply(
                lambda row: haversine_distance(reference_latitude, reference_longitude, row['위도'],
                                               row['경도']) < 1.0,
                axis=1)]
            # 리스트에 데이터 추가
            nearby_data_list.append(nearby_data)
    #10개 이내인 경우
    else:
        #위의 알고리즘과 동일
        for i in range(len(starbucks_data)):
            reference_latitude = starbucks_latitudes[i]
            reference_longitude = starbucks_longitudes[i]

            nearby_data = filtered_df[filtered_df.apply(
                lambda row: haversine_distance(reference_latitude, reference_longitude, row['위도'],
                                               row['경도']) < 1.0, axis=1)]
            nearby_data_list.append(nearby_data)

    # 각 시도별 top 10 업종 찾기
    top10_by_sido_list = [nearby_data.groupby(['시도명', '상권업종중분류명']).size().groupby(level=0, group_keys=False).nlargest(
        10).reset_index(name='count') for nearby_data in nearby_data_list]



    #os 마다 다른 폰트를 성정해줘야 한글이 제대로 나옴
    if os_name == 'mac':
        plt.rcParams['font.family'] = 'AppleGothic'
    else:
        plt.rcParams['font.family'] = 'NanumBarunGothic'

    # '상권업종중분류명' 기준으로 분포 시각화
    g = sns.catplot(x='count', y='상권업종중분류명', col='시도명', col_wrap=3, data=pd.concat(top10_by_sido_list),
                    kind='bar', height=5, aspect=1.2,
                    order=top10_by_sido_list[0]['상권업종중분류명'].unique())
    g.set_xticklabels(rotation=45, ha='right')
    g.fig.suptitle('스타벅스 전체 주변 Top 10 상권업종중분류명', y=0.98)
    plt.show()

    # 각 스타벅스 주변의 상권 밀도 분석
    density_data_list = [nearby_data.groupby(['시도명', '상권업종중분류명']).size().reset_index(name='density') for nearby_data in
                         nearby_data_list]

    # 각 지역의 스타벅스별 밀도 표현
    for i, density_data in enumerate(density_data_list):
        # Get the top 20 business categories
        top20_categories = density_data.groupby('상권업종중분류명')['density'].sum().nlargest(20).index

        # 20개의 업종의 밀도만 표현
        heatmap_data = density_data[density_data['상권업종중분류명'].isin(top20_categories)]
        heatmap_data = heatmap_data.pivot(index='상권업종중분류명', columns='시도명', values='density').fillna(0)

        # 히트맵 표현
        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".0f", linewidths=.5)
        plt.title(f'Top 20 비즈니스 밀도 {file_name} 스타벅스 {i + 1} 구역 by 상권업종중분류명')
        plt.show()

#에러가 날 경우 출력
except Exception as e:
    print(f"Error: {e}")
    print("데이터를 불러오거나 분석하는 도중 오류가 발생했습니다.")
