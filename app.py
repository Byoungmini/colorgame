"""
Guess My Color - Streamlit 웹앱 버전
"""
import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(
    page_title="Guess My Color",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 정의
st.markdown("""
<style>
    /* 메인 컨테이너 패딩 축소 */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 750px;
    }
    
    /* 기본 버튼 스타일 */
    .stButton > button {
        width: 100%;
        border-radius: 4px;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.2s !important;
        white-space: nowrap !important; /* 텍스트 줄바꿈 방지 */
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        z-index: 100;
    }
    
    /* 색상 상자 축소 */
    .color-box {
        width: 70px !important;
        height: 70px !important;
        border-radius: 6px;
        border: 2px solid #333;
        margin: 0 auto !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 수직 정렬 */
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* h1 태그 기본 마진 제거 */
    h1 {
        padding: 0 !important;
    }

    /* --- 모바일 반응형 처리 (핵심) --- */
    @media (max-width: 640px) {
        /* 가로 배치 강제 유지 */
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 2px !important;
            overflow-x: hidden !important;
        }
        
        /* 컬럼 너비 유동적 조정 */
        div[data-testid="column"] {
            width: auto !important;
            flex: 1 1 auto !important;
            min-width: 0 !important;
            padding: 0 1px !important;
        }
        
        /* 제목 마진 조정 (모바일에서는 덜 띄움) */
        .app-title {
            margin-top: 40px !important; 
            font-size: 20px !important;
        }
        
        /* 버튼 텍스트 크기 축소 */
        .stButton > button {
            font-size: 9px !important;
            padding: 0 !important;
            height: 24px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 상태 초기화 함수들
def generate_random_color():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

def rgb_to_hex(color):
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

def calculate_color_difference(current, target):
    return sum(abs(current[i] - target[i]) for i in range(3))

def initialize_game():
    if 'target_color' not in st.session_state:
        st.session_state.target_color = generate_random_color()
        st.session_state.current_color = [0, 0, 0]
        st.session_state.attempts = 0
        st.session_state.hints_used = 0
        st.session_state.start_time = None
        st.session_state.game_won = False
        st.session_state.game_won_checked = False
        st.session_state.hint_popup_shown = False
        st.session_state.hint_difference = None

def reset_game():
    st.session_state.target_color = generate_random_color()
    st.session_state.current_color = [0, 0, 0]
    st.session_state.attempts = 0
    st.session_state.hints_used = 0
    st.session_state.start_time = None
    st.session_state.game_won = False
    st.session_state.game_won_checked = False
    st.session_state.hint_popup_shown = False
    st.session_state.hint_difference = None

def adjust_rgb(channel_idx, delta):
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    new_value = st.session_state.current_color[channel_idx] + delta
    st.session_state.current_color[channel_idx] = max(0, min(255, new_value))

def check_color():
    st.session_state.attempts += 1
    if st.session_state.current_color == st.session_state.target_color:
        st.session_state.game_won = True
        st.session_state.end_time = time.time()

def get_hint():
    st.session_state.hints_used += 1
    st.session_state.hint_difference = calculate_color_difference(st.session_state.current_color, st.session_state.target_color)
    st.session_state.hint_popup_shown = True

def calculate_play_time():
    if st.session_state.start_time is None or not hasattr(st.session_state, 'end_time'):
        return "00:00"
    elapsed = int(st.session_state.end_time - st.session_state.start_time)
    return f"{elapsed // 60:02d}:{elapsed % 60:02d}"

# 게임 초기화
initialize_game()

# 팝업
@st.dialog("🎉 축하합니다!")
def show_winner_dialog():
    play_time = calculate_play_time()
    st.balloons()
    st.markdown("""<div style="text-align: center; margin-bottom: 10px;"><h3 style="margin: 0; font-size: 18px; color: #4CAF50;">정답을 맞추셨습니다!</h3></div>""", unsafe_allow_html=True)
    st.info(f"**게임 통계**\n- 🎯 목표: RGB{tuple(st.session_state.target_color)}\n- 🔄 시도: {st.session_state.attempts}회\n- 💡 힌트: {st.session_state.hints_used}회\n- ⏱️ 시간: {play_time}")
    if st.button("확인", key="winner_ok", type="primary", use_container_width=True):
        st.session_state.game_won_checked = True
        st.rerun()

@st.dialog("💡 힌트")
def show_hint_dialog(diff):
    st.markdown(f"""<div style="text-align: center;"><p style="margin-bottom:5px; font-size:14px;">현재 색상과 차이값</p><p style="font-size: 30px; font-weight: bold; color: #1976D2; margin: 5px 0;">{diff}</p><p style="color: #666; font-size: 12px;">0이면 정답입니다! 🎯</p></div>""", unsafe_allow_html=True)
    if st.button("확인", key="hint_ok", type="primary", use_container_width=True):
        st.session_state.hint_popup_shown = False
        st.rerun()

if st.session_state.game_won and not st.session_state.game_won_checked:
    show_winner_dialog()
if st.session_state.get('hint_popup_shown', False):
    show_hint_dialog(st.session_state.hint_difference)


# --- UI 구성 ---

# 1. 제목 (클래스 추가하여 CSS 제어)
st.markdown("""
<div class="app-title" style="text-align: center; margin-top: 60px; margin-bottom: 15px;">
    <h1 style="margin: 0; padding: 0; font-size: 24px !important; color: #333 !important; font-weight: 800;">🎨 Guess My Color</h1>
    <p style="margin: 4px 0 0 0; font-size: 12px; color: #666;">RGB 값을 조정해서 목표 색상과 일치시켜보세요!</p>
</div>
""", unsafe_allow_html=True)

# 2. 색상 패널
c_hex = rgb_to_hex(st.session_state.current_color)
t_hex = rgb_to_hex(st.session_state.target_color)
st.markdown(f"""
<div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 20px;">
    <div style="text-align: center;">
        <div style="font-weight: bold; font-size: 11px; margin-bottom: 3px;">현재 색상</div>
        <div class="color-box" style="background-color: {c_hex};"></div>
        <div style="font-size: 10px; margin-top: 3px;">RGB: {tuple(st.session_state.current_color)}</div>
    </div>
    <div style="text-align: center;">
        <div style="font-weight: bold; font-size: 11px; margin-bottom: 3px;">목표 색상</div>
        <div class="color-box" style="background-color: {t_hex};"></div>
        <div style="font-size: 10px; margin-top: 3px; color: #666;">맞춰보세요!</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. RGB 컨트롤
channels = [("Red", 0, "#D32F2F"), ("Green", 1, "#388E3C"), ("Blue", 2, "#1976D2")]
deltas = [-100, -10, -1, 1, 10, 100]

for name, idx, color_code in channels:
    cols = st.columns([1.1, 1.1, 1.1, 0.7, 1.1, 1.1, 1.1], gap="small")
    
    # 왼쪽 (- 버튼)
    for i, d in enumerate([-100, -10, -1]):
        with cols[i]:
            if st.button(f"{d}", key=f"{name}_{d}", use_container_width=True):
                adjust_rgb(idx, d)
                st.rerun()
    
    # 중앙 값
    with cols[3]:
        st.markdown(f"""
        <div style="text-align: center; line-height: 1; margin-top: 6px;">
            <div style="color: {color_code}; font-size: 14px; font-weight: bold;">{st.session_state.current_color[idx]}</div>
            <div style="color: {color_code}; font-size: 9px; font-weight: bold; margin-top:-1px;">{name}</div>
        </div>
        """, unsafe_allow_html=True)
        
    # 오른쪽 (+ 버튼)
    for i, d in enumerate([1, 10, 100]):
        with cols[i+4]:
            if st.button(f"+{d}", key=f"{name}_{d}", use_container_width=True):
                adjust_rgb(idx, d)
                st.rerun()

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# 4. 액션 버튼
ac1, ac2, ac3 = st.columns(3)
with ac1:
    if st.button("색상 확인", key="btn_check", use_container_width=True):
        check_color()
        st.rerun()
with ac2:
    if st.button("힌트", key="btn_hint", use_container_width=True):
        get_hint()
        st.rerun()
with ac3:
    if st.button("새 게임", key="btn_new", use_container_width=True):
        reset_game()
        st.rerun()

# 5. 통계
st.markdown(f"""
<div style="text-align: center; margin-top: 15px; padding: 5px; background-color: white; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <span style="margin-right: 15px; font-size: 11px;"><strong>시도:</strong> {st.session_state.attempts}회</span>
    <span style="font-size: 11px;"><strong>힌트:</strong> {st.session_state.hints_used}회</span>
</div>
""", unsafe_allow_html=True)


# CSS로 버튼 색상 강제 지정 (nth-of-type 유지)
st.markdown("""
<style>
    /* Red Buttons */
    div[data-testid="column"]:nth-of-type(1) .stButton button { background-color: #990000 !important; color: white !important; }
    div[data-testid="column"]:nth-of-type(2) .stButton button { background-color: #CC0000 !important; color: white !important; }
    div[data-testid="column"]:nth-of-type(3) .stButton button { background-color: #FF3333 !important; color: white !important; }
    
    div[data-testid="column"]:nth-of-type(5) .stButton button { background-color: #FFE6E6 !important; color: black !important; }
    div[data-testid="column"]:nth-of-type(6) .stButton button { background-color: #FFCCCC !important; color: black !important; }
    div[data-testid="column"]:nth-of-type(7) .stButton button { background-color: #FF9999 !important; color: black !important; }

    /* Green Buttons */
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"]:nth-child(1) button { background-color: #990000 !important; color: white !important; border: 1px solid #990000 !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"]:nth-child(2) button { background-color: #CC0000 !important; color: white !important; border: 1px solid #CC0000 !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"]:nth-child(3) button { background-color: #FF3333 !important; color: white !important; border: 1px solid #FF3333 !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"]:nth-child(5) button { background-color: #FFE6E6 !important; color: black !important; border: 1px solid #FFCCCC !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"]:nth-child(6) button { background-color: #FFCCCC !important; color: black !important; border: 1px solid #FF9999 !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) div[data-testid="column"]:nth-child(7) button { background-color: #FF9999 !important; color: black !important; border: 1px solid #FF6666 !important; }

    div[data-testid="stHorizontalBlock"]:nth-of-type(4) div[data-testid="column"]:nth-child(1) button { background-color: #006600 !important; color: white !important; border: 1px solid #006600 !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) div[data-testid="column"]:nth-child(2) button { background-color: #009900 !important; color: white !important; border: 1px solid #009900 !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) div[data-testid="column"]:nth-child(3) button { background-color: #00CC00 !important; color: white !important; border: 1px solid #00CC00 !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) div[data-testid="column"]:nth-child(5) button { background-color: #E6FFE6 !important; color: black !important; border: 1px solid #CCFFCC !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) div[data-testid="column"]:nth-child(6) button { background-color: #CCFFCC !important; color: black !important; border: 1px solid #99FF99 !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) div[data-testid="column"]:nth-child(7) button { background-color: #99FF99 !important; color: black !important; border: 1px solid #66FF66 !important; }

    div[data-testid="stHorizontalBlock"]:nth-of-type(5) div[data-testid="column"]:nth-child(1) button { background-color: #000099 !important; color: white !important; border: 1px solid #000099 !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(5) div[data-testid="column"]:nth-child(2) button { background-color: #0000CC !important; color: white !important; border: 1px solid #0000CC !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(5) div[data-testid="column"]:nth-child(3) button { background-color: #3333FF !important; color: white !important; border: 1px solid #3333FF !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(5) div[data-testid="column"]:nth-child(5) button { background-color: #E6E6FF !important; color: black !important; border: 1px solid #CCCCFF !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(5) div[data-testid="column"]:nth-child(6) button { background-color: #CCCCFF !important; color: black !important; border: 1px solid #9999FF !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(5) div[data-testid="column"]:nth-child(7) button { background-color: #9999FF !important; color: black !important; border: 1px solid #6666FF !important; }

    /* 공통 RGB 버튼 사이즈 */
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) button,
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) button,
    div[data-testid="stHorizontalBlock"]:nth-of-type(5) button {
        height: 20px !important;
        min-height: 0px !important;
        padding: 0 !important;
        font-size: 10px !important;
        line-height: 1 !important;
    }

    /* 액션 버튼 */
    div[data-testid="stHorizontalBlock"]:nth-of-type(7) div[data-testid="column"]:nth-child(1) button { background-color: #4CAF50 !important; color: white !important; height: 32px !important; min-height: 32px !important; font-size: 12px !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(7) div[data-testid="column"]:nth-child(2) button { background-color: #9C27B0 !important; color: white !important; height: 32px !important; min-height: 32px !important; font-size: 12px !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(7) div[data-testid="column"]:nth-child(3) button { background-color: #2196F3 !important; color: white !important; height: 32px !important; min-height: 32px !important; font-size: 12px !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.write("Guide")
