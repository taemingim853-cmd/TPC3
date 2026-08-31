import streamlit as st

st.set_page_config(page_title="블링블링 무한 투두 & 캐릭터 꾸미기 💖", page_icon="🦄", layout="centered")

st.markdown("""
    <style>
    .title-font {
        background: linear-gradient(to right, #ff9a9e, #fecfef, #a18cd1, #fbc2eb, #8fd3f4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 38px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        font-size: 17px;
    }
    .character-box {
        background-color: #fff0f6;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        border: 3px dashed #ffadd2;
    }
    </style>
    <div class="title-font">✨🦄 환상의 블링블링 목표 & 캐릭터 🦄✨</div>
    <div class="subtitle">할 일을 완료하고 코인을 모아 전설의 아바타를 완성하세요! 🌟💖🎀</div>
    <br>
""", unsafe_allow_html=True)

if "todos" not in st.session_state:
    st.session_state.todos = []
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "inventory" not in st.session_state:
    st.session_state.inventory = ["기본 옷 👕"]
if "equipped" not in st.session_state:
    st.session_state.equipped = "기본 옷 👕"
if "avatar" not in st.session_state:
    st.session_state.avatar = "🐱 아기 고양이"

AVATARS = {
    "🐱 아기 고양이": "🐱",
    "🐶 활발한 강아지": "🐶",
    "🐰 깡총 토끼": "🐰",
    "🧸 귀여운 곰돌이": "🧸",
    "🦊 영리한 여우": "🦊"
}

SHOP_ITEMS = {
    "👑 반짝이는 왕관": {"price": 100, "icon": "👑"},
    "🕶️ 힙스터 선글라스": {"price": 150, "icon": "🕶️"},
    "🎒 귀여운 책가방": {"price": 200, "icon": "🎒"},
    "🎀 러블리 리본": {"price": 250, "icon": "🎀"},
    "🪄 마법 요술봉": {"price": 300, "icon": "🪄"},
    "🚀 우주 비행 수트": {"price": 500, "icon": "🚀"},
    "🔥 [최종목표] 원피스 해적왕 루피": {"price": 2000, "icon": "👒🍖"},
    "⚡ [최종목표] 나루토 호카게 전설": {"price": 2500, "icon": "🍥🌀"},
    "⚔️ [최종목표] 귀멸의 칼날 귀살대": {"price": 3000, "icon": "⚔️👘"}
}

equipped_icon = SHOP_ITEMS.get(st.session_state.equipped, {}).get("icon", "👕") if st.session_state.equipped != "기본 옷 👕" else "👕"
current_avatar_icon = AVATARS.get(st.session_state.avatar, "🐱")

st.sidebar.header("💖 내 정보 & 아바타 💖")
st.sidebar.markdown(f"### 💰 **{st.session_state.coins} 코인** 보유 중!")

st.sidebar.subheader("👤 아바타 선택")
selected_avatar = st.sidebar.selectbox("나만의 기본 아바타를 골라보세요!", list(AVATARS.keys()))
if selected_avatar != st.session_state.avatar:
    st.session_state.avatar = selected_avatar
    st.rerun()

st.sidebar.markdown(f"""
<div class="character-box">
    <h4>{st.session_state.avatar}</h4>
    <h1 style="font-size: 65px; margin: 10px 0;">{equipped_icon}{current_avatar_icon}</h1>
    <p style="margin:0;"><b>착용 아이템:</b><br>{st.session_state.equipped}</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.subheader("👗 옷장 (아이템 착용)")
selected_item = st.sidebar.selectbox(
    "보유 중인 아이템을 착용해보세요!",
    st.session_state.inventory,
    index=st.session_state.inventory.index(st.session_state.equipped) if st.session_state.equipped in st.session_state.inventory else 0
)
if selected_item != st.session_state.equipped:
    st.session_state.equipped = selected_item
    st.rerun()

tab1, tab2 = st.tabs(["📝 무한 투두리스트", "🛍️ 전설의 옷상점"])

with tab1:
    st.subheader("🌈 새로운 목표 추가하기 ✍️")
    
    with st.form("add_todo_form", clear_on_submit=True):
        new_task = st.text_input("목표를 적고 엔터를 누르거나 버튼을 클릭하세요!", placeholder="예: 파이썬 코딩 공부하기 💻🔥")
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
        st.info("아직 추가된 목표가 없어요! 위에서 목표를 마음껏 추가해보세요 🎯")
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
    st.subheader("🛍️ 코인을 모아 전설의 아이템을 구매해보세요! 🪙")
    st.write(f"💵 현재 잔액: **{st.session_state.coins} 코인** (목표 1개 완료 시 +50 코인)")
    st.write("---")
    
    cols = st.columns(2)
    for i, (item_name, item_info) in enumerate(SHOP_ITEMS.items()):
        with cols[i % 2]:
            st.markdown(f"#### {item_info['icon']} {item_name}")
            st.write(f"가격: **{item_info['price']} 코인** 🪙")
            
            if item_name in st.session_state.inventory:
                st.success("✅ 이미 보유함")
            else:
                if st.button(f"구매하기 ({item_info['price']}💰)", key=f"buy_{item_name}"):
                    if st.session_state.coins >= item_info["price"]:
                        st.session_state.coins -= item_info["price"]
                        st.session_state.inventory.append(item_name)
                        st.toast(f"🎉 '{item_name}' 구매 성공!", icon="🛍️")
                        st.rerun()
                    else:
                        st.error("코인이 부족해요! 목표를 더 완료해보세요 💪")
