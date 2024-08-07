import streamlit as st
from PIL import Image
import pytesseract
from openai import OpenAI
import io

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='kor+eng')
    return text

def get_gpt_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 한국어 교육 전문가이며, 학생들의 문제 풀이를 도와주는 역할을 합니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

st.title("문제 분석 및 학습 도우미")

uploaded_file = st.file_uploader("문제 이미지를 업로드하세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 이미지', use_column_width=True)
    
    # 이미지에서 텍스트 추출
    extracted_text = extract_text_from_image(image)
    st.write("추출된 텍스트:")
    st.write(extracted_text)
    
    # 사용자 입력 받기
    user_answer = st.text_input("당신이 선택한 답을 입력하세요:")
    correct_answer = st.text_input("정답을 입력하세요:")
    
    if st.button("분석 및 해설 생성"):
        # GPT에 프롬프트 전송
        prompt = f"""
        다음은 학생이 틀린 문제입니다:

        문제: {extracted_text}

        학생의 답: {user_answer}
        정답: {correct_answer}

        1. 이 문제에 대한 상세한 해설을 제공해주세요.
        2. 학생이 왜 틀렸을지 분석해주세요.
        3. 이 문제와 유사하지만 난이도가 약간 높은 새로운 문제를 만들어주세요.
        """
        
        gpt_response = get_gpt_response(prompt)
        
        st.write("### GPT 분석 및 해설:")
        st.write(gpt_response)

st.write("이 앱을 통해 틀린 문제를 분석하고, 유사한 문제를 연습하여 실력을 향상시킬 수 있습니다.")
