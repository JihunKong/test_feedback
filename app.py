import streamlit as st
from openai import OpenAI
import base64

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def analyze_image_with_gpt4(image, user_answer, correct_answer):
    base64_image = encode_image(image)
    
    prompt = f"""
    이 이미지는 학생이 틀린 문제입니다. 이미지를 분석하고 다음 작업을 수행해주세요:
    1. 이미지에서 문제 내용을 추출해주세요.
    2. 추출한 문제에 대한 상세한 해설을 제공해주세요.
    3. 학생의 답변({user_answer})이 정답({correct_answer})과 다른 이유를 분석해주세요.
    4. 이 문제와 유사하지만 난이도가 약간 높은 새로운 문제를 만들어주세요.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

st.title("문제 분석 및 학습 도우미")

uploaded_file = st.file_uploader("문제 이미지를 업로드하세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='업로드된 이미지', use_column_width=True)
    
    # 사용자 입력 받기
    user_answer = st.text_input("당신이 선택한 답을 입력하세요:")
    correct_answer = st.text_input("정답을 입력하세요:")
    
    if st.button("분석 및 해설 생성"):
        if user_answer and correct_answer:
            gpt_response = analyze_image_with_gpt4(uploaded_file, user_answer, correct_answer)
            
            st.write("### GPT 분석 및 해설:")
            st.write(gpt_response)
        else:
            st.warning("답변과 정답을 모두 입력해주세요.")

st.write("이 앱을 통해 틀린 문제를 분석하고, 유사한 문제를 연습하여 실력을 향상시킬 수 있습니다.")
