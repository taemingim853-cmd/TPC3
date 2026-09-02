import streamlit as st
from datetime import datetime

st.set_page_config(page_title="갓생 투두 & 생산성 트래커", page_icon="✅", layout="centered")

# --- UI 스타일링 ---
st.markdown("""
    <style>
    .title-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: 900;
        font-size: 32px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-box {
        background-color: #f3f4f6;
        border-left: 5px solid #667eea;
        padding: 15px;
        border-radius: 8px;
        font-size: 18px;
        margin-bottom: 20px;
    }
    .task-text {
        font-size: 16px;
        font-weight: 500;
    }
    .task-date {
        font-size: 12px;
        color: #6b7280;
    }
    </style>
    <div class="title-box">✅ 갓생 투두 & 생산성 트래커</div>
""", unsafe_allow_html=True)

# --- 1. 초기 데이터 세팅 ---
if "todos" not in st.session_state:
    st.session_state.todos = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "completed_count" not in st.session_state:
    st.session_state.completed_count = 0

# --- 2. 상단 스탯 표시 ---
st.markdown(f"""
    <div class="stat-box">
        🌟 <b>나의 생산성 점수:</b> {st.session_state.score} 점 &nbsp; | &nbsp; 
        ✅ <b>완료한 목표:</b> {st.session_state.completed_count} 개
    </div>
""", unsafe_allow_html=True)

# --- 3. 투두 추가 폼 ---
with st.form("add_todo_form", clear_on_submit=True):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        new_task = st.text_input("새로운 목표를 입력하세요", label_visibility="collapsed", placeholder="예: 매일 아침 물 한 잔 마시기 💧")
    with col2:
        submitted = st.form_submit_button("➕ 추가")
        
    if submitted and new_task.strip():
        st.session_state.todos.append({
            "task": new_task.strip(),
            "done": False,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        st.rerun()

st.write("---")

# --- 4. 투두 리스트 표시 (진행 중 / 완료 분리) ---
active_todos = [t for t in st.session_state.todos if not t["done"]]
done_todos = [t for t in st.session_state.todos if t["done"]]

tab1, tab2 = st.tabs([f"🚀 진행 중 ({len(active_todos)})", f"🎉 완료됨 ({len(done_todos)})"])

# [탭 1] 진행 중인 목록
with tab1:
    if not active_todos:
        st.info("현재 진행 중인 목표가 없습니다. 새로운 목표를 추가해 보세요!")
    else:
        for idx, todo in enumerate(st.session_state.todos):
            if not todo["done"]:
                c1, c2, c3 = st.columns([0.1, 0.75, 0.15])
                with c1:
                    # 완료 버튼
                    if st.button("⭕", key=f"check_{idx}", help="목표 완료하기"):
                        todo["done"] = True
                        st.session_state.score += 10
                        st.session_state.completed_count += 1
                        st.toast("목표 달성! +10점 획득 🎉", icon="✅")
                        st.balloons()
                        st.rerun()
                with c2:
                    st.markdown(f"<div class='task-text'>{todo['task']}</div><div class='task-date'>{todo['date']} 추가됨</div>", unsafe_allow_html=True)
                with c3:
                    # 삭제 버튼
                    if st.button("🗑️", key=f"del_active_{idx}"):
                        st.session_state.todos.pop(idx)
                        st.rerun()

# [탭 2] 완료된 목록
with tab2:
    if not done_todos:
        st.info("아직 완료된 목표가 없습니다. 첫 목표를 달성해 보세요!")
    else:
        for idx, todo in enumerate(st.session_state.todos):
            if todo["done"]:
                c1, c2, c3 = st.columns([0.1, 0.75, 0.15])
                with c1:
                    # 되돌리기 버튼
                    if st.button("↩️", key=f"undo_{idx}", help="진행 중으로 되돌리기"):
                        todo["done"] = False
                        st.session_state.score = max(0, st.session_state.score - 10)
                        st.session_state.completed_count = max(0, st.session_state.completed_count - 1)
                        st.rerun()
                with c2:
                    st.markdown(f"<del style='color:gray; font-size:16px;'>{todo['task']}</del>", unsafe_allow_html=True)
                with c3:
                    if st.button("🗑️", key=f"del_done_{idx}"):
                        st.session_state.todos.pop(idx)
                        st.rerun()
