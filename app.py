import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# 1. 장학금 데이터베이스 생성 (최신 정보 반영)
# --------------------------------------------------------------------------
def create_scholarship_df():
    """
    장학금 데이터를 pandas DataFrame으로 생성하는 함수
    """
    data = [
        # 대학원생
        {'장학금명': 'AI서울테크 대학원 장학금', '구분': '대학원생', '학년 정보': '대학원 재학생', '전공 계열': 'AI/이공계', '필수 조건': '해당 없음', '경제상황 요건': '해당 없음'},
        
        # 대학생
        {'장학금명': '서울희망 대학진로 장학금', '구분': '대학생', '학년 정보': '신입생(1학년), 재학생(2학년 이상)', '전공 계열': '전공무관', '필수 조건': '해당 없음', '경제상황 요건': '기초생활수급자/법정차상위계층, 학자금지원 4구간 이내'},
        {'장학금명': '서울희망 공익인재 장학금', '구분': '대학생', '학년 정보': '재학생(2학년 이상)', '전공 계열': '전공무관', '필수 조건': '사회공헌활동 경험자', '경제상황 요건': '해당 없음'},
        {'장학금명': '독립유공자 후손 장학금', '구분': '대학생', '학년 정보': '신입생(1학년), 재학생(2학년 이상)', '전공 계열': '전공무관', '필수 조건': '독립유공자 후손 (4~6대)', '경제상황 요건': '해당 없음'},
        {'장학금명': '서울 해외교환학생 장학금', '구분': '대학생', '학년 정보': '재학생(2학년 이상)', '전공 계열': '전공무관', '필수 조건': '해외교환학생으로 선발된 자', '경제상황 요건': '기초생활수급자/법정차상위계층, 학자금지원 4구간 이내'},
        {'장학금명': '청춘Start 장학금', '구분': '대학생', '학년 정보': '신입생(1학년)', '전공 계열': '전공무관', '필수 조건': '해당 없음', '경제상황 요건': '기초생활수급자/법정차상위계층, 아동복지시설 퇴소자'},
        {'장학금명': '서울희망 직업전문학교 장학금', '구분': '대학생', '학년 정보': '직업전문학교 학생', '전공 계열': '전공무관', '필수 조건': '해당 없음', '경제상황 요건': '기초생활수급자/법정차상위계층'},

        # 고등학생
        {'장학금명': '서울희망고교진로 장학금', '구분': '고등학생', '학년 정보': '고등학교 재학생', '전공 계열': '전공무관', '필수 조건': '해당 없음', '경제상황 요건': '기초생활수급자, 차상위계층, 북한이탈주민, 경제사각지대'},
        {'장학금명': '서울희망 예체능 장학금', '구분': '고등학생', '학년 정보': '고등학교 재학생', '전공 계열': '예체능', '필수 조건': '예체능 특기자', '경제상황 요건': '기초생활수급자/법정차상위계층, 학교장 추천 받은 학생'},
        {'장학금명': '서울꿈길장학금', '구분': '고등학생', '학년 정보': '비인가 대안교육기관 재학 청소년', '전공 계열': '전공무관', '필수 조건': '학교장 추천', '경제상황 요건': '기초생활수급자/법정차상위계층, 학교장 추천'}
    ]
    return pd.DataFrame(data)

# --------------------------------------------------------------------------
# 2. 결과 출력 함수
# --------------------------------------------------------------------------
def display_results(result_df):
    st.subheader("🏆 추천 장학금 결과")
    if result_df.empty:
        st.info("✅ 아쉽지만 현재 조건에 맞는 장학금이 없습니다.")
    else:
        st.success(f"총 {len(result_df)}개의 장학금을 추천합니다!")
        result_df_display = result_df.drop(columns=['구분', '학년 정보'], errors='ignore')
        st.dataframe(result_df_display, hide_index=True)

# --------------------------------------------------------------------------
# 3. 메인 프로그램 로직
# --------------------------------------------------------------------------
def main():
    df = create_scholarship_df()
    st.markdown(
        """
        <style>
        .stApp { background-color: #ffd240; }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("✨ 나에게 맞는 서울 장학금 추천")
    st.write("간단한 질문에 답변하고, 나에게 딱 맞는 장학금을 찾아보세요!")

    main_type = st.selectbox("학생 구분을 선택해주세요.", ['--선택--', '대학원생', '대학생', '고등학생'])

    if main_type == '--선택--': return

    if main_type == '대학원생':
        display_results(df[df['구분'] == '대학원생'])
        return

    if main_type == '대학생':
        status_options = ['--선택--', '신입생(1학년)', '재학생(2학년 이상)', '직업전문학교 학생']
        user_status = st.selectbox("학년 정보를 선택해주세요.", status_options)

        if user_status == '--선택--': return

        if user_status == '직업전문학교 학생':
            result_df = df[df['장학금명'] == '서울희망 직업전문학교 장학금']
            display_results(result_df)
            return

        if user_status == '신입생(1학년)':
            scholarship_names = ['서울희망 대학진로 장학금', '청춘Start 장학금', '독립유공자 후손 장학금']
            result_df = df[df['장학금명'].isin(scholarship_names)]
            display_results(result_df)
            return

        if user_status == '재학생(2학년 이상)':
            excluded_scholarships = ['청춘Start 장학금', '서울희망 직업전문학교 장학금']
            result_df = df[(df['구분'] == '대학생') & (~df['장학금명'].isin(excluded_scholarships))]
            display_results(result_df)
            return

    elif main_type == '고등학생':
        status_options = ['--선택--', '고등학교 재학생', '비인가 대안교육기관 재학 청소년']
        user_status = st.selectbox("조금 더 상세한 신분을 선택해주세요.", status_options)

        if user_status == '--선택--': return

        if user_status == '비인가 대안교육기관 재학 청소년':
            display_results(df[df['학년 정보'] == user_status])
            return

        filtered_df = df[df['학년 정보'] == user_status]
        
        user_major = st.selectbox("전공 계열을 선택해주세요.", ['--선택--', '예체능', '기타'])
        if user_major == '--선택--': return
        
        eco_options = [
            '--선택--', '기초생활수급자 또는 법정차상위계층', '북한이탈주민',
            '위에 해당하지 않지만 경제적 지원이 필요한 상황 (경제사각지대 등)', '해당 없음'
        ]
        user_eco_choice = st.selectbox("경제적 상황을 선택해주세요.", eco_options)
        if user_eco_choice == '--선택--': return

        user_eco_conditions = []
        if user_eco_choice == eco_options[1]:
            user_eco_conditions = ['기초생활수급자', '차상위계층', '법정차상위계층']
        elif user_eco_choice == eco_options[2]:
            user_eco_conditions = ['북한이탈주민']
        elif user_eco_choice == eco_options[3]:
            user_eco_conditions = ['경제사각지대', '학교장 추천 받은 학생']

        final_recommendations = []
        for _, row in filtered_df.iterrows():
            if user_major == '예체능' and row['전공 계열'] != '예체능': continue
            if user_major == '기타' and row['전공 계열'] == '예체능': continue
            
            # ✨ 수정된 부분: 별도의 '필수 조건' 질문 없이, 전공과 경제상황만으로 필터링합니다.
            # 예체능 장학금의 '예체능 특기자' 조건은 '예체능' 전공 선택으로 갈음합니다.
            
            req_eco = row['경제상황 요건']
            
            if user_eco_choice == '해당 없음':
                if '해당 없음' in row['필수 조건'] and '해당 없음' in req_eco:
                    final_recommendations.append(row)
            elif any(cond in req_eco for cond in user_eco_conditions):
                 final_recommendations.append(row)
        
        display_results(pd.DataFrame(final_recommendations))

# --------------------------------------------------------------------------
# 4. 프로그램 실행
# --------------------------------------------------------------------------
if __name__ == "__main__":
    main()
