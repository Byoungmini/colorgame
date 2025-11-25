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

# 커스텀 CSS - 버튼 색상 포함
st.markdown("""
<style>
    .main {
        background-color: #f0f0f0;
        padding-top: 0.5rem !important;
    }
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
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
    /* RGB 조정 버튼만 더 작게 - 강력한 선택자 */
    button[data-testid="baseButton-secondary"][key*="Red_"],
    button[data-testid="baseButton-secondary"][key*="Green_"],
    button[data-testid="baseButton-secondary"][key*="Blue_"],
    div[data-testid="stButton"] button[key*="Red_"],
    div[data-testid="stButton"] button[key*="Green_"],
    div[data-testid="stButton"] button[key*="Blue_"] {
        height: 18px !important;
        min-height: 18px !important;
        max-height: 18px !important;
        font-size: 8px !important;
        padding: 0.05rem 0.15rem !important;
        line-height: 1 !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    div[data-testid="column"] {
        padding: 0 1px !important;
    }
    .color-box {
        width: 110px !important;
        height: 110px !important;
        border-radius: 6px;
        border: 2px solid #333;
        margin: 2px auto !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stats-box {
        background-color: white;
        padding: 5px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 2px 0 !important;
    }
    h1 {
        color: #333333;
        text-align: center;
        margin: 0 0 5px 0 !important;
        font-size: 22px !important;
        padding: 0;
    }
    .rgb-label {
        font-size: 13px !important;
        font-weight: bold;
        text-align: center;
        margin: 2px 0 !important;
        line-height: 1.1;
    }
    hr {
        margin: 3px 0 !important;
    }
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    h4 {
        font-size: 15px !important;
        margin: 5px 0 3px 0 !important;
        text-align: center;
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


def reset_game():
    """새 게임 시작"""
    st.session_state.target_color = generate_random_color()
    st.session_state.current_color = [0, 0, 0]
    st.session_state.attempts = 0
    st.session_state.hints_used = 0
    st.session_state.start_time = None
    st.session_state.game_won = False
    st.session_state.popup_shown = False


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


def calculate_play_time():
    """플레이 시간 계산"""
    if st.session_state.start_time is None or not hasattr(st.session_state, 'end_time'):
        return "00:00"
    
    elapsed = int(st.session_state.end_time - st.session_state.start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    return f"{minutes:02d}:{seconds:02d}"


# 게임 초기화
initialize_game()

# 팝업 모달 스타일 추가
st.markdown("""
<style>
    .modal-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 9999;
        justify-content: center;
        align-items: center;
    }
    .modal-overlay.show {
        display: flex;
    }
    .modal-content {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        max-width: 500px;
        width: 90%;
        animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn {
        from {
            transform: translateY(-50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    .modal-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .modal-title {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
        margin-bottom: 10px;
    }
    .modal-stats {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .modal-stats h3 {
        margin-top: 0;
        color: #1976D2;
        font-size: 18px;
    }
    .modal-stats p {
        margin: 8px 0;
        font-size: 14px;
        color: #333;
    }
    .modal-close {
        width: 100%;
        padding: 12px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .modal-close:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# 제목
st.markdown("<h1 style='margin: 0 0 3px 0;'>🎨 Guess My Color</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 13px; color: #666; margin: 5px 0 10px 0;'>RGB 값을 조정해서 목표 색상과 일치시켜보세요!</p>", unsafe_allow_html=True)

# 게임 승리 시 팝업 모달 표시
if st.session_state.game_won:
    play_time = calculate_play_time()
    
    # 팝업이 이미 표시되었는지 확인하는 플래그
    if 'popup_shown' not in st.session_state or not st.session_state.popup_shown:
        st.session_state.popup_shown = True
        
        popup_html = f"""
        <div class="modal-overlay show" id="gameStatsModal" style="display: flex; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 9999; justify-content: center; align-items: center;">
            <div class="modal-content" style="background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); max-width: 500px; width: 90%;" onclick="event.stopPropagation();">
                <div class="modal-header">
                    <div class="modal-title">🎉 축하합니다!</div>
                    <div style="font-size: 16px; color: #666;">정답을 맞추셨습니다!</div>
                </div>
                <div class="modal-stats">
                    <h3>게임 통계</h3>
                    <p><strong>목표 색상:</strong> RGB({st.session_state.target_color[0]}, {st.session_state.target_color[1]}, {st.session_state.target_color[2]})</p>
                    <p><strong>시도 횟수:</strong> {st.session_state.attempts}회</p>
                    <p><strong>힌트 사용:</strong> {st.session_state.hints_used}회</p>
                    <p><strong>플레이 시간:</strong> {play_time}</p>
                </div>
                <button class="modal-close" id="modalCloseBtn" type="button" style="width: 100%; padding: 12px; background-color: #4CAF50; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background-color 0.3s; margin-top: 10px;">
                    확인
                </button>
            </div>
        </div>
        <script>
            (function() {{
                function initModal() {{
                    const modal = document.getElementById('gameStatsModal');
                    const closeBtn = document.getElementById('modalCloseBtn');
                    
                    if (!modal) {{
                        setTimeout(initModal, 100);
                        return;
                    }}
                    
                    // 확인 버튼 클릭 이벤트 - 여러 방법으로 시도
                    if (closeBtn) {{
                        // onclick 속성 직접 설정
                        closeBtn.setAttribute('onclick', 'this.closest(".modal-overlay").style.display="none"; return false;');
                        
                        // addEventListener도 추가
                        closeBtn.addEventListener('click', function(e) {{
                            e.preventDefault();
                            e.stopPropagation();
                            e.cancelBubble = true;
                            if (modal) {{
                                modal.style.display = 'none';
                                modal.style.visibility = 'hidden';
                            }}
                            return false;
                        }}, true);
                        
                        // 마우스 이벤트도 추가
                        closeBtn.addEventListener('mousedown', function(e) {{
                            e.preventDefault();
                            e.stopPropagation();
                            if (modal) {{
                                modal.style.display = 'none';
                            }}
                            return false;
                        }}, true);
                    }}
                    
                    // 오버레이 클릭 시 닫기
                    modal.addEventListener('click', function(e) {{
                        if (e.target === modal || e.target.classList.contains('modal-overlay')) {{
                            modal.style.display = 'none';
                        }}
                    }}, true);
                    
                    // ESC 키로 닫기
                    function handleEscape(e) {{
                        if (e.key === 'Escape' && modal && modal.style.display === 'flex') {{
                            modal.style.display = 'none';
                        }}
                    }}
                    document.addEventListener('keydown', handleEscape);
                }}
                
                // 즉시 실행 + 지연 실행
                setTimeout(initModal, 50);
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', initModal);
                }} else {{
                    initModal();
                }
            }})();
        </script>
        """
        st.markdown(popup_html, unsafe_allow_html=True)

# 색상 패널
col1, col2 = st.columns(2)

with col1:
    st.markdown("<p style='text-align: center; font-weight: bold; font-size: 13px; margin: 0 0 2px 0;'>현재 색상</p>", unsafe_allow_html=True)
    current_hex = rgb_to_hex(st.session_state.current_color)
    st.markdown(f"""
    <div class="color-box" style="background-color: {current_hex};"></div>
    """, unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 10px; margin: 2px 0 0 0;'>RGB: ({st.session_state.current_color[0]}, {st.session_state.current_color[1]}, {st.session_state.current_color[2]})</p>", unsafe_allow_html=True)

with col2:
    st.markdown("<p style='text-align: center; font-weight: bold; font-size: 13px; margin: 0 0 2px 0;'>목표 색상</p>", unsafe_allow_html=True)
    target_hex = rgb_to_hex(st.session_state.target_color)
    st.markdown(f"""
    <div class="color-box" style="background-color: {target_hex};"></div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 10px; margin: 2px 0 0 0; color: #666;'>목표를 맞춰보세요!</p>", unsafe_allow_html=True)

# RGB 조정 컨트롤
st.markdown("#### 🎛️ RGB 값 조정")

# 버튼 색상 정의
button_styles = {
    ("Red", -100): ("#990000", "white"),
    ("Red", -10): ("#CC0000", "white"),
    ("Red", -1): ("#FF3333", "white"),
    ("Red", 1): ("#FFE6E6", "black"),
    ("Red", 10): ("#FFCCCC", "black"),
    ("Red", 100): ("#FF9999", "black"),
    ("Green", -100): ("#006600", "white"),
    ("Green", -10): ("#009900", "white"),
    ("Green", -1): ("#00CC00", "white"),
    ("Green", 1): ("#E6FFE6", "black"),
    ("Green", 10): ("#CCFFCC", "black"),
    ("Green", 100): ("#99FF99", "black"),
    ("Blue", -100): ("#000099", "white"),
    ("Blue", -10): ("#0000CC", "white"),
    ("Blue", -1): ("#3333FF", "white"),
    ("Blue", 1): ("#E6E6FF", "black"),
    ("Blue", 10): ("#CCCCFF", "black"),
    ("Blue", 100): ("#9999FF", "black"),
}

channels = [("Red", 0), ("Green", 1), ("Blue", 2)]
deltas = [-100, -10, -1, +1, +10, +100]

# 모든 버튼 스타일을 한 번에 생성
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

# CSS 주입
st.markdown(f"<style>{''.join(css_rules)}</style>", unsafe_allow_html=True)

for channel_name, channel_idx in channels:
    label_colors = {"Red": "#CC0000", "Green": "#009900", "Blue": "#0000CC"}
    current_value = st.session_state.current_color[channel_idx]
    
    # RGB 조정 컨트롤 레이아웃: 버튼들 - 중앙 값 표시 - 버튼들
    cols = st.columns([1, 1, 1, 0.5, 1, 1, 1], gap="small")
    
    # 왼쪽 버튼들 (-100, -10, -1)
    for i, delta in enumerate([-100, -10, -1]):
        with cols[i]:
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
    
    # 중앙에 현재 값 표시 (큰 숫자)
    with cols[3]:
        st.markdown(f"""
        <div style="text-align: center; padding: 5px 0;">
            <p style='color: {label_colors[channel_name]}; font-size: 18px; font-weight: bold; margin: 0;'>{current_value}</p>
            <p style='color: {label_colors[channel_name]}; font-size: 11px; margin: 0;'>{channel_name}</p>
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

st.markdown("---")

# 액션 버튼 스타일
st.markdown("""
<style>
button[key="check_color"],
button:has(+ div:contains("색상 확인")) {
    background-color: #4CAF50 !important;
    color: white !important;
}
button[key="get_hint"],
button:has(+ div:contains("힌트")) {
    background-color: #9C27B0 !important;
    color: white !important;
}
button[key="new_game"],
button:has(+ div:contains("새 게임")) {
    background-color: #2196F3 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

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
        difference = calculate_color_difference(st.session_state.current_color, st.session_state.target_color)
        st.info(f"현재 색상과 목표 색상의 총 차이값: **{difference}**\n\n(차이값이 0이면 정답입니다)")

with col3:
    new_game_btn = st.button("새 게임", key="new_game", use_container_width=True)
    if new_game_btn:
        reset_game()
        st.rerun()

# 통계 표시
st.markdown(f"""
<div class="stats-box">
    <p style='text-align: center; font-size: 11px; margin: 0;'>
        <strong>시도:</strong> {st.session_state.attempts}회 &nbsp;&nbsp;|&nbsp;&nbsp; 
        <strong>힌트:</strong> {st.session_state.hints_used}회
    </p>
</div>
""", unsafe_allow_html=True)

# JavaScript로 동적 색상 적용 (CSS가 작동하지 않을 경우를 대비)
st.markdown("""
<script>
function styleButtons() {
    const colors = {
        'Red_-100': {bg: '#990000', text: 'white'},
        'Red_-10': {bg: '#CC0000', text: 'white'},
        'Red_-1': {bg: '#FF3333', text: 'white'},
        'Red_1': {bg: '#FFE6E6', text: 'black'},
        'Red_10': {bg: '#FFCCCC', text: 'black'},
        'Red_100': {bg: '#FF9999', text: 'black'},
        'Green_-100': {bg: '#006600', text: 'white'},
        'Green_-10': {bg: '#009900', text: 'white'},
        'Green_-1': {bg: '#00CC00', text: 'white'},
        'Green_1': {bg: '#E6FFE6', text: 'black'},
        'Green_10': {bg: '#CCFFCC', text: 'black'},
        'Green_100': {bg: '#99FF99', text: 'black'},
        'Blue_-100': {bg: '#000099', text: 'white'},
        'Blue_-10': {bg: '#0000CC', text: 'white'},
        'Blue_-1': {bg: '#3333FF', text: 'white'},
        'Blue_1': {bg: '#E6E6FF', text: 'black'},
        'Blue_10': {bg: '#CCCCFF', text: 'black'},
        'Blue_100': {bg: '#9999FF', text: 'black'}
    };
    
    document.querySelectorAll('button[data-testid="baseButton-secondary"]').forEach(btn => {
        const btnText = btn.textContent.trim();
        const parent = btn.closest('div');
        let key = null;
        
        // 키 찾기
        ['Red', 'Green', 'Blue'].forEach(channel => {
            if (parent && parent.textContent.includes(channel)) {
                key = channel + '_' + btnText.replace(/[+]/g, '');
            }
        });
        
        if (key && colors[key]) {
            btn.style.setProperty('background-color', colors[key].bg, 'important');
            btn.style.setProperty('color', colors[key].text, 'important');
            // RGB 조정 버튼 크기 강제로 줄이기
            btn.style.setProperty('height', '18px', 'important');
            btn.style.setProperty('min-height', '18px', 'important');
            btn.style.setProperty('max-height', '18px', 'important');
            btn.style.setProperty('font-size', '8px', 'important');
            btn.style.setProperty('padding', '0.05rem 0.15rem', 'important');
            btn.style.setProperty('line-height', '1', 'important');
            // 모든 크기 관련 속성 강제 설정
            if (btn.parentElement) {
                btn.parentElement.style.height = '18px';
                btn.parentElement.style.minHeight = '18px';
            }
        }
    });
    
    // 액션 버튼
    document.querySelectorAll('button').forEach(btn => {
        const text = btn.textContent.trim();
        if (text === '색상 확인') {
            btn.style.setProperty('background-color', '#4CAF50', 'important');
            btn.style.setProperty('color', 'white', 'important');
        } else if (text === '힌트') {
            btn.style.setProperty('background-color', '#9C27B0', 'important');
            btn.style.setProperty('color', 'white', 'important');
        } else if (text === '새 게임') {
            btn.style.setProperty('background-color', '#2196F3', 'important');
            btn.style.setProperty('color', 'white', 'important');
        }
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', styleButtons);
} else {
    styleButtons();
}

// Streamlit 업데이트 감지
const observer = new MutationObserver(function(mutations) {
    styleButtons();
    // RGB 버튼 크기 강제 조정
    document.querySelectorAll('button[data-testid="baseButton-secondary"]').forEach(btn => {
        const btnText = btn.textContent.trim();
        if (btnText.match(/^[+-]?\d+$/)) {
            const parent = btn.closest('div');
            if (parent && (parent.textContent.includes('Red') || parent.textContent.includes('Green') || parent.textContent.includes('Blue'))) {
                btn.style.setProperty('height', '18px', 'important');
                btn.style.setProperty('min-height', '18px', 'important');
                btn.style.setProperty('max-height', '18px', 'important');
                btn.style.setProperty('font-size', '8px', 'important');
                btn.style.setProperty('padding', '0.05rem 0.15rem', 'important');
                btn.style.setProperty('line-height', '1', 'important');
            }
        }
    });
});
observer.observe(document.body, { childList: true, subtree: true });

// 추가로 주기적으로 체크 (더블 체크)
setInterval(function() {
    document.querySelectorAll('button').forEach(btn => {
        const btnText = btn.textContent.trim();
        if (btnText.match(/^[+-]?\d+$/)) {
            const parent = btn.closest('div');
            if (parent && (parent.textContent.includes('Red') || parent.textContent.includes('Green') || parent.textContent.includes('Blue'))) {
                if (parseInt(getComputedStyle(btn).height) > 20) {
                    btn.style.setProperty('height', '18px', 'important');
                    btn.style.setProperty('min-height', '18px', 'important');
                    btn.style.setProperty('max-height', '18px', 'important');
                    btn.style.setProperty('font-size', '8px', 'important');
                    btn.style.setProperty('padding', '0.05rem 0.15rem', 'important');
                }
            }
        }
    });
}, 300);
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
    
    **RGB란?**
    - Red(빨강), Green(초록), Blue(파랑)
    - 각 값은 0~255 범위입니다
    - 세 색을 섞어 모든 색을 만들 수 있습니다
    
    **버튼 색상 의미:**
    - 진한 색 버튼(-100, -10, -1): 값을 빼기
    - 밝은 색 버튼(+1, +10, +100): 값을 더하기
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 팁")
    st.markdown("""
    - 큰 값(±100, ±10)으로 빠르게 조정
    - 작은 값(±1)으로 미세 조정
    - 힌트의 차이값이 작을수록 정답에 가까움
    """)
