"""
Guess My Color - Streamlit 웹앱 버전
RGB 색상 학습을 위한 교육용 게임 애플리케이션
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

# 커스텀 CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f0f0;
        padding-top: 0.5rem !important;
    }
    .block-container {
        padding-top: 0.3rem !important;
        padding-bottom: 0.3rem !important;
        max-width: 750px;
    }
    .stButton>button {
        width: 100%;
        height: 26px !important;
        font-size: 10px !important;
        font-weight: bold;
        border-radius: 4px;
        margin: 0 !important;
        padding: 0.15rem 0.3rem !important;
        border: 1px solid rgba(0,0,0,0.2) !important;
        transition: all 0.2s !important;
    }
    /* RGB 조정 버튼만 더 작게 */
    div[data-testid="column"] button {
        height: 18px !important;
        min-height: 18px !important;
        font-size: 9px !important;
        padding: 0.05rem 0.15rem !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    div[data-testid="column"] {
        padding: 0 1px !important;
    }
    /* 색상 패널 간격 최소화 */
    div[data-testid="stHorizontalBlock"] {
        gap: 2px !important;
    }
    .color-box {
        width: 90px !important;
        height: 90px !important;
        border-radius: 5px;
        border: 2px solid #333;
        margin: 1px auto !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stats-box {
        background-color: white;
        padding: 4px;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1px 0 !important;
    }
    h1 {
        color: #333333;
        text-align: center;
        margin: 0 0 2px 0 !important;
        font-size: 18px !important;
        padding: 0;
    }
    .rgb-label {
        font-size: 12px !important;
        font-weight: bold;
        text-align: center;
        margin: 1px 0 !important;
        line-height: 1;
    }
    hr {
        margin: 2px 0 !important;
    }
    
    /* 액션 버튼 색상 */
    button[key="check_color"], div[data-testid="stButton"]:has(button:contains("색상 확인")) button {
        background-color: #4CAF50 !important;
        color: white !important;
        height: 32px !important;
        font-size: 12px !important;
    }
    button[key="get_hint"], div[data-testid="stButton"]:has(button:contains("힌트")) button {
        background-color: #9C27B0 !important;
        color: white !important;
        height: 32px !important;
        font-size: 12px !important;
    }
    button[key="new_game"], div[data-testid="stButton"]:has(button:contains("새 게임")) button {
        background-color: #2196F3 !important;
        color: white !important;
        height: 32px !important;
        font-size: 12px !important;
    }
</style>
""", unsafe_allow_html=True)


def generate_random_color():
    """랜덤 RGB 색상 생성"""
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


def rgb_to_hex(color):
    """RGB를 HEX로 변환"""
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"


def calculate_color_difference(current, target):
    """Manhattan distance 계산"""
    return sum(abs(current[i] - target[i]) for i in range(3))


def initialize_game():
    """게임 초기화"""
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
    """새 게임 시작"""
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
    """RGB 값 조정"""
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    
    new_value = st.session_state.current_color[channel_idx] + delta
    st.session_state.current_color[channel_idx] = max(0, min(255, new_value))


def check_color():
    """색상 확인"""
    st.session_state.attempts += 1
    if st.session_state.current_color == st.session_state.target_color:
        st.session_state.game_won = True
        st.session_state.end_time = time.time()


def get_hint():
    """힌트 제공"""
    st.session_state.hints_used += 1
    st.session_state.hint_difference = calculate_color_difference(st.session_state.current_color, st.session_state.target_color)
    st.session_state.hint_popup_shown = True


def calculate_play_time():
    """플레이 시간 계산"""
    if st.session_state.start_time is None or not hasattr(st.session_state, 'end_time'):
        return "00:00"
    
    elapsed = int(st.session_state.end_time - st.session_state.start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    return f"{minutes:02d}:{seconds:02d}"


@st.dialog("🎉 축하합니다!")
def show_winner_dialog():
    play_time = calculate_play_time()
    st.balloons()
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #4CAF50;">정답을 맞추셨습니다!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"""
    **게임 통계**
    - 🎯 **목표 색상:** RGB({st.session_state.target_color[0]}, {st.session_state.target_color[1]}, {st.session_state.target_color[2]})
    - 🔄 **시도 횟수:** {st.session_state.attempts}회
    - 💡 **힌트 사용:** {st.session_state.hints_used}회
    - ⏱️ **플레이 시간:** {play_time}
    """)
    
    if st.button("확인", key="winner_ok_btn", use_container_width=True, type="primary"):
        st.session_state.game_won_checked = True
        st.rerun()


@st.dialog("💡 힌트")
def show_hint_dialog(difference):
    st.markdown(f"""
    <div style="text-align: center;">
        <p style="font-size: 16px; margin-bottom: 10px;">
            <strong>현재 색상과 목표 색상의 총 차이값</strong>
        </p>
        <p style="font-size: 40px; font-weight: bold; color: #1976D2; margin: 10px 0;">
            {difference}
        </p>
        <p style="font-size: 14px; color: #666; margin-top: 10px;">
            차이값이 <strong>0</strong>이면 정답입니다! 🎯
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("확인", key="hint_ok_btn", use_container_width=True, type="primary"):
        st.session_state.hint_popup_shown = False
        st.rerun()


# 게임 초기화
initialize_game()

# 팝업 표시 로직
if st.session_state.game_won and not st.session_state.game_won_checked:
    show_winner_dialog()

if st.session_state.get('hint_popup_shown', False) and st.session_state.hint_difference is not None:
    show_hint_dialog(st.session_state.hint_difference)


# UI 구성
st.markdown("<h1 style='margin: 0 0 2px 0;'>🎨 Guess My Color</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 11px; color: #666; margin: 2px 0 5px 0;'>RGB 값을 조정해서 목표 색상과 일치시켜보세요!</p>", unsafe_allow_html=True)

# 색상 패널
col1, col2 = st.columns(2, gap="small")

with col1:
    st.markdown("<p style='text-align: center; font-weight: bold; font-size: 11px; margin: 0 0 1px 0;'>현재 색상</p>", unsafe_allow_html=True)
    current_hex = rgb_to_hex(st.session_state.current_color)
    st.markdown(f"""
    <div class="color-box" style="background-color: {current_hex};"></div>
    """, unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 9px; margin: 1px 0 0 0;'>RGB: ({st.session_state.current_color[0]}, {st.session_state.current_color[1]}, {st.session_state.current_color[2]})</p>", unsafe_allow_html=True)

with col2:
    st.markdown("<p style='text-align: center; font-weight: bold; font-size: 11px; margin: 0 0 1px 0;'>목표 색상</p>", unsafe_allow_html=True)
    target_hex = rgb_to_hex(st.session_state.target_color)
    st.markdown(f"""
    <div class="color-box" style="background-color: {target_hex};"></div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 9px; margin: 1px 0 0 0; color: #666;'>목표를 맞춰보세요!</p>", unsafe_allow_html=True)

# RGB 조정 컨트롤
# 버튼 색상 정의
button_styles = {
    ("Red", -100): ("#990000", "white"), ("Red", -10): ("#CC0000", "white"), ("Red", -1): ("#FF3333", "white"),
    ("Red", 1): ("#FFE6E6", "black"), ("Red", 10): ("#FFCCCC", "black"), ("Red", 100): ("#FF9999", "black"),
    ("Green", -100): ("#006600", "white"), ("Green", -10): ("#009900", "white"), ("Green", -1): ("#00CC00", "white"),
    ("Green", 1): ("#E6FFE6", "black"), ("Green", 10): ("#CCFFCC", "black"), ("Green", 100): ("#99FF99", "black"),
    ("Blue", -100): ("#000099", "white"), ("Blue", -10): ("#0000CC", "white"), ("Blue", -1): ("#3333FF", "white"),
    ("Blue", 1): ("#E6E6FF", "black"), ("Blue", 10): ("#CCCCFF", "black"), ("Blue", 100): ("#9999FF", "black"),
}

channels = [("Red", 0), ("Green", 1), ("Blue", 2)]
deltas = [-100, -10, -1, +1, +10, +100]

# CSS 주입을 위한 리스트
css_rules = []
for channel_name, _ in channels:
    for delta in deltas:
        bg_color, text_color = button_styles[(channel_name, delta)]
        button_key = f"{channel_name}_{delta}"
        css_rules.append(f"""
        button[data-testid="baseButton-secondary"][aria-label*="{button_key}"],
        div[data-testid="stButton"]:has(button[key="{button_key}"]) button {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}""")
st.markdown(f"<style>{''.join(css_rules)}</style>", unsafe_allow_html=True)

for channel_name, channel_idx in channels:
    label_colors = {"Red": "#CC0000", "Green": "#009900", "Blue": "#0000CC"}
    current_value = st.session_state.current_color[channel_idx]
    
    cols = st.columns([1, 1, 1, 0.5, 1, 1, 1], gap="small")
    
    # 왼쪽 버튼들 (-100, -10, -1)
    for i, delta in enumerate([-100, -10, -1]):
        with cols[i]:
            button_key = f"{channel_name}_{delta}"
            bg_color, text_color = button_styles[(channel_name, delta)]
            # 인라인 스타일로 확실하게 적용
            st.markdown(f"""
            <style>
            div:has(button[key="{button_key}"]) button {{
                background-color: {bg_color} !important;
                color: {text_color} !important;
            }}
            </style>
            """, unsafe_allow_html=True)
            
            if st.button(f"{delta:+d}", key=button_key, disabled=st.session_state.game_won, use_container_width=True):
                adjust_rgb(channel_idx, delta)
                st.rerun()
    
    # 중앙에 현재 값 표시
    with cols[3]:
        st.markdown(f"""
        <div style="text-align: center; padding: 2px 0;">
            <p style='color: {label_colors[channel_name]}; font-size: 15px; font-weight: bold; margin: 0;'>{current_value}</p>
            <p style='color: {label_colors[channel_name]}; font-size: 9px; margin: 0;'>{channel_name}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 오른쪽 버튼들 (+1, +10, +100)
    for i, delta in enumerate([1, 10, 100]):
        with cols[i + 4]:
            button_key = f"{channel_name}_{delta}"
            bg_color, text_color = button_styles[(channel_name, delta)]
            st.markdown(f"""
            <style>
            div:has(button[key="{button_key}"]) button {{
                background-color: {bg_color} !important;
                color: {text_color} !important;
            }}
            </style>
            """, unsafe_allow_html=True)
            
            if st.button(f"{delta:+d}", key=button_key, disabled=st.session_state.game_won, use_container_width=True):
                adjust_rgb(channel_idx, delta)
                st.rerun()

st.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

# 액션 버튼
col1, col2, col3 = st.columns(3)

with col1:
    check_btn = st.button("색상 확인", key="check_color", disabled=st.session_state.game_won, use_container_width=True)
    if check_btn:
        check_color()
        st.rerun()

with col2:
    hint_btn = st.button("힌트", key="get_hint", disabled=st.session_state.game_won, use_container_width=True)
    if hint_btn:
        get_hint()
        st.rerun()

with col3:
    new_game_btn = st.button("새 게임", key="new_game", use_container_width=True)
    if new_game_btn:
        reset_game()
        st.rerun()

# 통계 표시
st.markdown(f"""
<div class="stats-box">
    <p style='text-align: center; font-size: 10px; margin: 0;'>
        <strong>시도:</strong> {st.session_state.attempts}회 &nbsp;&nbsp;|&nbsp;&nbsp; 
        <strong>힌트:</strong> {st.session_state.hints_used}회
    </p>
</div>
""", unsafe_allow_html=True)

# JavaScript로 버튼 스타일 강제 적용 (백업용)
st.markdown("""
<script>
function styleButtons() {
    const colors = {
        'Red_-100': {bg: '#990000', text: 'white'}, 'Red_-10': {bg: '#CC0000', text: 'white'}, 'Red_-1': {bg: '#FF3333', text: 'white'},
        'Red_1': {bg: '#FFE6E6', text: 'black'}, 'Red_10': {bg: '#FFCCCC', text: 'black'}, 'Red_100': {bg: '#FF9999', text: 'black'},
        'Green_-100': {bg: '#006600', text: 'white'}, 'Green_-10': {bg: '#009900', text: 'white'}, 'Green_-1': {bg: '#00CC00', text: 'white'},
        'Green_1': {bg: '#E6FFE6', text: 'black'}, 'Green_10': {bg: '#CCFFCC', text: 'black'}, 'Green_100': {bg: '#99FF99', text: 'black'},
        'Blue_-100': {bg: '#000099', text: 'white'}, 'Blue_-10': {bg: '#0000CC', text: 'white'}, 'Blue_-1': {bg: '#3333FF', text: 'white'},
        'Blue_1': {bg: '#E6E6FF', text: 'black'}, 'Blue_10': {bg: '#CCCCFF', text: 'black'}, 'Blue_100': {bg: '#9999FF', text: 'black'}
    };
    
    document.querySelectorAll('button[data-testid="baseButton-secondary"]').forEach(btn => {
        const btnText = btn.textContent.trim();
        const parent = btn.closest('div');
        let key = null;
        
        if (parent) {
            if (parent.parentElement && parent.parentElement.textContent.includes('Red')) key = 'Red_' + btnText.replace(/[+]/g, '');
            else if (parent.parentElement && parent.parentElement.textContent.includes('Green')) key = 'Green_' + btnText.replace(/[+]/g, '');
            else if (parent.parentElement && parent.parentElement.textContent.includes('Blue')) key = 'Blue_' + btnText.replace(/[+]/g, '');
        }
        
        if (key && colors[key]) {
            btn.style.setProperty('background-color', colors[key].bg, 'important');
            btn.style.setProperty('color', colors[key].text, 'important');
            // RGB 버튼 크기 강제
            btn.style.setProperty('height', '18px', 'important');
            btn.style.setProperty('min-height', '18px', 'important');
            btn.style.setProperty('font-size', '9px', 'important');
            btn.style.setProperty('padding', '0.05rem 0.15rem', 'important');
        }
    });
}

// 주기적으로 실행
setInterval(styleButtons, 500);
</script>
""", unsafe_allow_html=True)

# 게임 설명 (사이드바)
with st.sidebar:
    st.markdown("### 📖 게임 방법")
    st.markdown("""
    1. 오른쪽의 **목표 색상**을 보세요
    2. RGB 값을 조정하여 **현재 색상**을 목표 색상과 일치시키세요
    3. **색상 확인** 버튼으로 정답을 확인하세요
    4. 막히면 **힌트** 버튼을 사용하세요
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 팁")
    st.markdown("""
    - 큰 값(±100, ±10)으로 빠르게 조정
    - 작은 값(±1)으로 미세 조정
    - 힌트의 차이값이 작을수록 정답에 가까움
    """)
