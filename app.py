import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# 1. 장학금 데이터베이스 생성 (최신 정보로 전면 수정)
# --------------------------------------------------------------------------
def create_scholarship_df():
    """
    장학금 데이터를 pandas DataFrame으로 생성하는 함수
    """
    data = [
        # '필수 조건'으로 컬럼명 변경 및 전체 데이터 업데이트
        {'장학금명': 'AI서울테크 대학원 장학금', '구분': '대학원생', '학년 정보': '대학원 재학생', '전공 계열': 'AI/이공계', '필수 조건': '해당 없음', '경제상황 요건': '해당 없음'},
        {'장학금명': '서울희망 대학진로 장학금', '구분': '대학생', '학년 정보': '대학교 재학생, 대학 신입생', '전공 계열': '전공무관', '필수 조건': '해당 없음', '경제상황 요건': '기초생활수급자/법정차상위계층, 학자금지원 4구간 이내'},
        {'장학금명': '서울희망 공익인재 장학금', '구분': '대학생', '학년 정보': '대학생', '전공 계열': '전공무관', '필수 조건': '사회공헌활동 경험자', '경제상황 요건': '해당 없음'},
        {'장학금명': '독립유공자 후손 장학금', '구분': '대학생', '학년 정보': '대학 재학생, 대학 신입생', '전공 계열': '전공무관', '필수 조건': '독립유공자 후손 (4~6대)', '경제상황 요건': '해당 없음'},
        {'장학금명': '서울 해외교환학생 장학금', '구분': '대학생', '학년 정보': '4년제 대학 재학생', '전공 계열': '전공무관', '필수 조건': '해외교환학생으로 선발된 자', '경제상황 요건': '기초생활수급자/법정차상위계층, 학자금지원 4구간 이내'},
        {'장학금명': '청춘Start 장학금', '구분': '대학생', '학년 정보': '대학 신입생', '전공 계열': '전공무관', '필수 조건': '해당 없음', '경제상황 요건': '기초생활수급자/법정차상위계층, 아동복지시설 퇴소자'},
        {'장학금명': '서울희망 직업전문학교 장학금', '구분': '고등학생', '학년 정보': '직업전문학교 재학생', '전공 계열': '해당 없음', '필수 조건': '해당 없음', '경제상황 요건': '기초생활수급자/법정차상위계층'},
        {'장학금명': '서울희망고교진로 장학금', '구분': '고등학생', '학년 정보': '고등학교 재학생', '전공 계열': '해당 없음', '필수 조건': '해당 없음', '경제상황 요건': '기초생활수급자, 차상위계층, 북한이탈주민, 경제사각지대'},
        {'장학금명': '서울희망 예체능 장학금', '구분': '고등학생', '학년 정보': '고등학교 재학생', '전공 계열': '예체능', '필수 조건': '예체능 특기자', '경제상황 요건': '기초생활수급자/법정차상위계층, 학교장 추천 받은 학생'},
        {'장학금명': '서울꿈길장학금', '구분': '고등학생', '학년 정보': '비인가 대안교육기관 재학 청소년', '전공 계열': '해당 없음', '필수 조건': '학교장 추천', '경제상황 요건': '기초생활수급자/법정차상위계층, 학교장 추천'}
    ]
    return pd.DataFrame(data)

# --------------------------------------------------------------------------
# 2. 결과 출력 함수
# --------------------------------------------------------------------------
def display_results(result_df):
    """결과를 스트림릿 화면에 예쁘게 출력하는 함수"""
    st.subheader("🏆 추천 장학금 결과")
    if result_df.empty:
        st.info("✅ 아쉽지만 현재 조건에 맞는 장학금이 없습니다.")
    else:
        st.success(f"총 {len(result_df)}개의 장학금을 추천합니다!")
        # 표시할 필요 없는 '구분', '학년 정보' 컬럼 제외
        result_df_display = result_df.drop(columns=['구분', '학년 정보'], errors='ignore')
        st.dataframe(result_df_display, hide_index=True)

# --------------------------------------------------------------------------
# 3. 메인 프로그램 로직 (수정된 데이터 기반으로 재구성)
# --------------------------------------------------------------------------
def main():
    df = create_scholarship_df()

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ffd240;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("✨ 나에게 맞는 서울 장학금 추천")
    st.write("간단한 질문에 답변하고, 나에게 딱 맞는 장학금을 찾아보세요!")

    main_type = st.selectbox("학생 구분을 선택해주세요.", ['--선택--', '대학원생', '대학생', '고등학생'])

    if main_type == '--선택--':
        return

    # 선택한 구분에 맞는 데이터만 필터링
    filtered_df = df[df['구분'] == main_type].copy()

    # --- 시나리오 1: 대학원생 ---
    if main_type == '대학원생':
        display_results(filtered_df)
        return

    # --- 공통 로직: 상세 신분(학년 정보) 선택 ---
    status_options = ['--선택--'] + sorted(list(filtered_df['학년 정보'].unique()))
    user_status = st.selectbox("조금 더 상세한 신분을 선택해주세요.", status_options)

    if user_status == '--선택--':
        return

    # 상세 신분에 맞는 데이터만 필터링 (여러 학년 정보 포함 가능성 처리)
    filtered_df = filtered_df[filtered_df['학년 정보'].str.contains(user_status, na=False)]

    # --- 시나리오 2: 대학생 ---
    if main_type == '대학생':
        unique_conditions = set()
        for _, row in filtered_df.iterrows():
            conditions = row['필수 조건'].split(', ') + row['경제상황 요건'].split(', ')
            unique_conditions.update(c.strip() for c in conditions if c != '해당 없음')
        
        user_conditions = []
        if unique_conditions:
            user_conditions = st.multiselect("해당하는 모든 조건을 선택해주세요.", sorted(list(unique_conditions)))

        final_recommendations = []
        for _, row in filtered_df.iterrows():
            all_required = row['필수 조건'] + ", " + row['경제상황 요건']
            is_eligible = False
            if not user_conditions and '해당 없음' in all_required:
                is_eligible = True
            elif any(cond in all_required for cond in user_conditions):
                is_eligible = True
            if is_eligible:
                final_recommendations.append(row)
        display_results(pd.DataFrame(final_recommendations))

    # --- 시나리오 3: 고등학생 ---
    elif main_type == '고등학생':
        # 꿈길/직업전문학교는 바로 결과 표시
        if user_status in ['비인가 대안교육기관 재학 청소년', '직업전문학교 재학생']:
            display_results(filtered_df)
            return

        # 일반 고등학생 로직
        user_major = st.selectbox("전공 계열을 선택해주세요.", ['--선택--', '예체능', '기타'])
        if user_major == '--선택--':
            return
            
        eco_options = [
            '--선택--', '기초생활수급자 또는 법정차상위계층', '북한이탈주민',
            '위에 해당하지 않지만 경제적 지원이 필요한 상황 (경제사각지대 등)',
            '학교장 추천을 받은 학생', '해당 없음'
        ]
        user_eco_choice = st.selectbox("경제적 상황 및 추천 여부를 선택해주세요.", eco_options)
        if user_eco_choice == '--선택--':
            return

        user_eco_conditions = []
        if user_eco_choice == eco_options[1]: user_eco_conditions = ['기초생활수급자', '차상위계층', '법정차상위계층']
        elif user_eco_choice == eco_options[2]: user_eco_conditions = ['북한이탈주민']
        elif user_eco_choice == eco_options[3]: user_eco_conditions = ['경제사각지대']
        elif user_eco_choice == eco_options[4]: user_eco_conditions = ['학교장 추천']

        final_recommendations = []
        for _, row in filtered_df.iterrows():
            if user_major == '예체능' and row['전공 계열'] != '예체능': continue
            if user_major == '기타' and row['전공 계열'] == '예체능': continue
            
            all_required = row['필수 조건'] + ", " + row['경제상황 요건']
            if user_eco_choice == '해당 없음':
                if '해당 없음' in all_required:
                    final_recommendations.append(row)
            elif any(cond in all_required for cond in user_eco_conditions):
                final_recommendations.append(row)
        
        display_results(pd.DataFrame(final_recommendations))

# --------------------------------------------------------------------------
# 4. 프로그램 실행
# --------------------------------------------------------------------------
if __name__ == "__main__":
    main()
