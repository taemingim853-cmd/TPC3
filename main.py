import streamlit as st

st.set_page_config(page_title="일러스트 아바타 무한 투두앱 💖", page_icon="🎨", layout="centered")

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
    .character-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #ffadd2;
    }
    </style>
    <div class="title-font">✨🦄 일러스트 목표 & 캐릭터 꾸미기 🦄✨</div>
    <div class="subtitle">목표를 달성해 코인을 모으고 전설의 코스튬을 완성하세요! 🌟💖🎀</div>
    <br>
""", unsafe_allow_html=True)

if "todos" not in st.session_state:
    st.session_state.todos = []
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "inventory" not in st.session_state:
    st.session_state.inventory = ["기본 아바타 👕"]
if "equipped" not in st.session_state:
    st.session_state.equipped = "기본 아바타 👕"

CHARACTER_IMAGES = {
    "기본 아바타 👕": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&auto=format&fit=crop&q=60",
    "👑 반짝이는 왕관 코스튬": "https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=500&auto=format&fit=crop&q=60",
    "🕶️ 힙스터 스타일": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&auto=format&fit=crop&q=60",
    "🚀 우주 비행 수트": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=500&auto=format&fit=crop&q=60",
    "🔥 [최종목표] 원피스 해적왕 루피": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=500&auto=format&fit=crop&q=60",
    "⚡ [최종목표] 나루토 호카게 전설": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=500&auto=format&fit=crop&q=60",
    "⚔️ [최종목표] 귀멸의 칼날 귀살대": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&auto=format&fit=crop&q=60"
}

SHOP_ITEMS = {
    "👑 반짝이는 왕관 코스튬": {"price": 100, "desc": "화려한 왕관 스타일링"},
    "🕶️ 힙스터 스타일": {"price": 150, "desc": "멋진 선글라스와 캐주얼 룩"},
    "🚀 우주 비행 수트": {"price": 500, "desc": "SF 느낌의 신비로운 수트"},
    "🔥 [최종목표] 원피스 해적왕 루피": {"price": 2000, "desc": "전설의 해적왕 스타일!"},
    "⚡ [최종목표] 나루토 호카게 전설": {"price": 2500, "desc": "불의 의지를 이은 호카게!"},
    "⚔️ [최종목표] 귀멸의 칼날 귀살대": {"price": 3000, "desc": "혈귀를 베는 전설의 검사!"}
}

st.sidebar.header("💖 내 아바타 & 정보 💖")
st.sidebar.markdown(f"### 💰 **{st.session_state.coins} 코인** 보유 중!")

st.sidebar.markdown('<div class="character-card">', unsafe_allow_html=True)
current_img_url = CHARACTER_IMAGES.get(st.session_state.equipped, CHARACTER_IMAGES["기본 아바타 👕"])
st.sidebar.image(current_img_url, caption=f"현재 착용: {st.session_state.equipped}", use_container_width=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.subheader("👗 옷장 (코스튬 교체)")
selected_item = st.sidebar.selectbox(
    "착용할 코스튬을 선택하세요!",
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
        new_task = st.text_input("목표를 입력하세요!", placeholder="예: 운동 30분 하기 🏃‍♂️")
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
        st.info("아직 등록된 목표가 없습니다. 위에서 목표를 등록해보세요! 🎯")
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
    st.subheader("🛍️ 코인을 모아 일러스트 코스튬을 구매하세요! 🪙")
    st.write(f"💵 현재 잔액: **{st.session_state.coins} 코인** (목표 1개 완료 시 +50 코인)")
    st.write("---")
    
    cols = st.columns(2)
    for i, (item_name, item_info) in enumerate(SHOP_ITEMS.items()):
        with cols[i % 2]:
            st.image(CHARACTER_IMAGES[item_name], use_container_width=True)
            st.markdown(f"#### {item_name}")
            st.caption(item_info["desc"])
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
                        st.error("코인이 부족합니다! 목표를 더 완료해보세요 💪")
