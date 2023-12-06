import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

os_name = input('OS환경을 입력하세요(1.mac, 2.window): ')

#지역별 평균월소득액 데이터 얻기
region_column = '시군구'
#파일경로
file_path = 'data2/국민연금공단_자격 시구신고 평균소득월액_20200531.csv'
local = ['강원도', '경기도', '경상남도', '경상북도', '광주', '대구', '대전', '부산', '서울', '세종', '울산', '인천', '전라남도', '전라북도', '제주', '충청남도', '충청북도']

try:
    #encoding 'euc-kr'로 하지 않으면 제대로 읽을 수 없음
    df = pd.read_csv(file_path, encoding='euc-kr', low_memory=False)

    #평균 급여 딕셔너리
    avg_income_dict = {}
    for region in local:
        #local 리스트에 있는 str이 포함되어 있는 칼럼만 넣기
        df_region = df[df[region_column].str.contains(region, na=False)]
        #평균소득월액의 평균값 구하기
        avg_income_region = df_region['평균소득월액'].mean()
        #지역-월급 key-value로 값 대입
        avg_income_dict[region] = avg_income_region
        #출력 소수점 2자리까지
        print(f"{region}: {avg_income_region:.2f} 원")

    # 막대 그래프 생성
    if os_name == 'mac':
        plt.rcParams['font.family'] = 'AppleGothic'
    else:
        plt.rcParams['font.family'] = 'NanumBarunGothic'
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(avg_income_dict.keys()), y=list(avg_income_dict.values()), palette='viridis')
    #제목, x축, y축
    plt.title('지역별 평균 급여')
    plt.xlabel('지역')
    plt.ylabel('평균 지역별 월급 급여 (원)')
    plt.xticks(rotation=45, ha='right')
    plt.show()

except UnicodeDecodeError:
    print("Failed to read with encoding")
