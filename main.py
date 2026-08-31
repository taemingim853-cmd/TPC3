import streamlit as st

st.set_page_config(page_title="입체 아바타 옷 입히기 & 무한 투두 💖", page_icon="👗", layout="centered")

st.markdown("""
    <style>
    .title-font {
        background: linear-gradient(to right, #ff9a9e, #fecfef, #a18cd1, #fbc2eb, #8fd3f4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 36px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #666;
    }
    .avatar-container {
        background: #f0f4f8;
        background-image: linear-gradient(#e1e8ed 1px, transparent 1px), linear-gradient(90deg, #e1e8ed 1px, transparent 1px);
        background-size: 20px 20px;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        border: 3px solid #bde0fe;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
    }
    </style>
    <div class="title-font">✨👗 입체 아바타 옷 입히기 투두 👗✨</div>
    <div class="subtitle">할 일을 완료하고 코인을 모아 머리와 몸에 실제 옷을 입혀주세요! 🌟</div>
    <br>
""", unsafe_allow_html=True)

if "todos" not in st.session_state:
    st.session_state.todos = []
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "inventory" not in st.session_state:
    st.session_state.inventory = ["기본 속옷 🩳"]
if "equipped" not in st.session_state:
    st.session_state.equipped = "기본 속옷 🩳"

SHOP_ITEMS = {
    "👑 반짝이는 황금 왕관": {"price": 100, "slot": "head", "desc": "머리 위에 딱 맞는 황금 왕관"},
    "🕶️ 힙스터 선글라스": {"price": 150, "slot": "eyes", "desc": "눈에 스타일리시하게 착용"},
    "👕 캐주얼 파란 티셔츠": {"price": 200, "slot": "body", "desc": "상체에 입는 깔끔한 티셔츠"},
    "🔥 [최종목표] 원피스 루피 밀짚모자": {"price": 2000, "slot": "head", "desc": "머리에 착용하는 전설의 밀짚모자"},
    "⚡ [최종목표] 나루토 써클렛": {"price": 2500, "slot": "head", "desc": "이마에 착용하는 닌자 써클렛"},
    "⚔️ [최종목표] 귀멸의 칼날 귀살대 하오리": {"price": 3000, "slot": "body", "desc": "몸에 두르는 전통 하오리"}
}

def render_avatar_svg(equipped_item):
    head_layer = ""
    eyes_layer = ""
    body_layer = ""

    if equipped_item == "👑 반짝이는 황금 왕관":
        head_layer = """
            <polygon points="95,48 105,25 125,38 145,25 155,48" fill="#FFD700" stroke="#B8860B" stroke-width="2"/>
            <circle cx="105" cy="25" r="3.5" fill="#FF0000"/>
            <circle cx="125" cy="38" r="3.5" fill="#0000FF"/>
            <circle cx="145" cy="25" r="3.5" fill="#FF0000"/>
            <rect x="95" y="46" width="60" height="7" fill="#B8860B" rx="2"/>
        """
    elif equipped_item == "🔥 [최종목표] 원피스 루피 밀짚모자":
        head_layer = """
            <ellipse cx="125" cy="48" rx="60" ry="12" fill="#E6C280" stroke="#9E7B35" stroke-width="2"/>
            <path d="M 98 48 Q 125 12 152 48 Z" fill="#E6C280" stroke="#9E7B35" stroke-width="2"/>
            <path d="M 98 45 Q 125 38 152 45 L 152 49 Q 125 42 98 49 Z" fill="#D32F2F"/>
        """
    elif equipped_item == "⚡ [최종목표] 나루토 써클렛":
        head_layer = """
            <path d="M 92 52 Q 125 48 158 52 L 158 64 Q 125 60 92 64 Z" fill="#2C3E50"/>
            <rect x="108" y="53" width="34" height="11" fill="#BDC3C7" stroke="#7F8C8D" stroke-width="1.5" rx="2"/>
            <circle cx="125" cy="58" r="3" fill="none" stroke="#2C3E50" stroke-width="1.5"/>
        """
    elif equipped_item == "🕶️ 힙스터 선글라스":
        eyes_layer = """
            <rect x="102" y="66" width="20" height="12" fill="#111111" rx="3"/>
            <rect x="128" y="66" width="20" height="12" fill="#111111" rx="3"/>
            <line x1="122" y1="70" x2="128" y2="70" stroke="#111111" stroke-width="3"/>
        """
    elif equipped_item == "👕 캐주얼 파란 티셔츠":
        body_layer = """
            <path d="M 85 120 L 165 120 L 175 160 L 155 165 L 150 200 L 100 200 L 95 165 L 75 160 Z" fill="#3498DB" stroke="#2980B9" stroke-width="2"/>
            <path d="M 115 120 Q 125 130 135 120 Z" fill="#F5CBA7"/>
        """
    elif equipped_item == "⚔️ [최종목표] 귀멸의 칼날 귀살대 하오리":
        body_layer = """
            <path d="M 80 118 L 170 118 L 180 230 L 155 230 L 150 140 L 100 140 L 95 230 L 70 230 Z" fill="#16A085" stroke="#111111" stroke-width="2"/>
            <rect x="80" y="130" width="15" height="15" fill="#111111"/>
            <rect x="155" y="130" width="15" height="15" fill="#111111"/>
            <rect x="75" y="160" width="15" height="15" fill="#111111"/>
            <rect x="160" y="160" width="15" height="15" fill="#111111"/>
            <rect x="70" y="190" width="15" height="15" fill="#111111"/>
            <rect x="165" y="190" width="15" height="15" fill="#111111"/>
        """

    svg_code = f"""
    <svg width="250" height="360" viewBox="0 0 250 360" xmlns="http://www.w3.org/2000/svg">
        <ellipse cx="125" cy="340" rx="65" ry="12" fill="#d0d7de"/>
        <g id="base-body">
            <rect x="100" y="235" width="22" height="100" rx="9" fill="#F5CBA7"/>
            <rect x="128" y="235" width="22" height="100" rx="9" fill="#F5CBA7"/>
            <path d="M 92 200 L 158 200 L 158 240 L 126 240 L 126 215 L 124 215 L 124 240 L 92 240 Z" fill="#7F8C8D"/>
            <rect x="117" y="100" width="16" height="25" fill="#E5B993"/>
            <path d="M 88 120 L 162 120 L 155 205 L 95 205 Z" fill="#F5CBA7"/>
            <path d="M 94 120 L 156 120 L 150 175 L 100 175 Z" fill="#FFFFFF" stroke="#BDC3C7" stroke-width="1.5"/>
            <rect x="74" y="120" width="16" height="90" rx="8" fill="#F5CBA7"/>
            <rect x="160" y="120" width="16" height="90" rx="8" fill="#F5CBA7"/>
            <ellipse cx="125" cy="72" rx="32" ry="38" fill="#F5CBA7"/>
            <path d="M 93 68 Q 125 32 157 68 Q 142 48 125 50 Q 108 48 93 68 Z" fill="#5D4037"/>
            <circle cx="112" cy="72" r="3.5" fill="#2C3E50"/>
            <circle cx="138" cy="72" r="3.5" fill="#2C3E50"/>
            <path d="M 118 88 Q 125 94 132 88" stroke="#C0392B" stroke-width="2.5" fill="none"/>
        </g>
        {body_layer}
        {eyes_layer}
        {head_layer}
    </svg>
    """
    return svg_code

st.sidebar.header("💖 내 아바타 베이스 💖")
st.sidebar.markdown(f"### 💰 **{st.session_state.coins} 코인** 보유 중!")

st.sidebar.markdown('<div class="avatar-container">', unsafe_allow_html=True)
st.sidebar.markdown(render_avatar_svg(st.session_state.equipped), unsafe_allow_html=True)
st.sidebar.markdown(f"<b>현재 착용:</b> {st.session_state.equipped}", unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.subheader("👗 옷장 (아이템 장착)")
selected_item = st.sidebar.selectbox(
    "옷장에서 선택하여 아바타에 입혀보세요!",
    st.session_state.inventory,
    index=st.session_state.inventory.index(st.session_state.equipped) if st.session_state.equipped in st.session_state.inventory else 0
)
if selected_item != st.session_state.equipped:
    st.session_state.equipped = selected_item
    st.rerun()

tab1, tab2 = st.tabs(["📝 무한 투두리스트", "🛍️ 옷 & 코스튬 상점"])

with tab1:
    st.subheader("🌈 새로운 목표 추가하기 ✍️")
    with st.form("add_todo_form", clear_on_submit=True):
        new_task = st.text_input("목표를 적고 등록하세요!", placeholder="예: 파이썬 공부하기 💻")
        submitted = st.form_submit_button("➕ 목표 등록하기 ✨")
        if submitted and new_task.strip():
            st.session_state.todos.append({
                "task": new_task.strip(),
                "done": False,
                "rewarded": False
            })
            st.rerun()

    st.write("---")
    st.subheader("📋 오늘의 목표 목록")

    if not st.session_state.todos:
        st.info("목표를 추가하고 완료하여 코인을 모아보세요! 🎯")
    else:
        for idx, todo in enumerate(st.session_state.todos):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                display_text = f"~~{todo['task']}~~ (완료! 🎉)" if todo['done'] else todo['task']
                is_done = st.checkbox(display_text, value=todo["done"], key=f"todo_{idx}")
            with col2:
                if st.button("🗑️ 삭제", key=f"del_{idx}"):
                    st.session_state.todos.pop(idx)
                    st.rerun()

            if is_done != todo["done"]:
                todo["done"] = is_done
                if is_done and not todo["rewarded"]:
                    todo["rewarded"] = True
                    st.session_state.coins += 50
                    st.balloons()
                    st.toast("🎉 미션 클리어! 50 코인을 획득했습니다! 💰", icon="🪙")
                    st.rerun()
                elif not is_done and todo["rewarded"]:
                    todo["rewarded"] = False
                    st.session_state.coins = max(0, st.session_state.coins - 50)
                    st.rerun()

with tab2:
    st.subheader("🛍️ 상점에서 옷과 모자를 구매하세요! 🪙")
    st.write(f"💵 현재 잔액: **{st.session_state.coins} 코인** (목표 1개 완료 시 +50 코인)")
    st.write("---")
    
    cols = st.columns(2)
    for i, (item_name, item_info) in enumerate(SHOP_ITEMS.items()):
        with cols[i % 2]:
            st.markdown(f"#### {item_name}")
            st.caption(item_info["desc"])
            st.write(f"가격: **{item_info['price']} 코인** 🪙")
            
            if item_name in st.session_state.inventory:
                st.success("✅ 보유 중")
            else:
                if st.button(f"구매하기 ({item_info['price']}💰)", key=f"buy_{item_name}"):
                    if st.session_state.coins >= item_info["price"]:
                        st.session_state.coins -= item_info["price"]
                        st.session_state.inventory.append(item_name)
                        st.toast(f"🎉 '{item_name}' 구매 성공! 옷장에서 입혀보세요.", icon="🛍️")
                        st.rerun()
                    else:
                        st.error("코인이 부족합니다! 목표를 더 완료해보세요 💪")
