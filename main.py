```python
import streamlit as st
from datetime import datetime, date, timedelta
from PIL import Image, ImageDraw
import os
import base64

st.set_page_config(
    page_title="갓생 투두 & 다마고치",
    page_icon="🐣",
    layout="centered"
)

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
.pet-box {
    background: linear-gradient(135deg, #fff7ed, #fef3c7);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
.pet-name {
    font-size: 28px;
    font-weight: 900;
}
.pet-level {
    font-size: 18px;
    font-weight: bold;
}
.task-text {
    font-size: 16px;
    font-weight: 500;
}
.task-date {
    font-size: 12px;
    color: #6b7280;
}
.progress-text {
    font-size: 14px;
    color: #4b5563;
}
</style>

<div class="title-box">
🐣 갓생 투두 & 다마고치
</div>
""", unsafe_allow_html=True)

if "todos" not in st.session_state:
    st.session_state.todos = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "completed_count" not in st.session_state:
    st.session_state.completed_count = 0

today = date.today()
week_start = today - timedelta(days=today.weekday())
week_end = week_start + timedelta(days=6)

def todo_date(todo):
    return datetime.strptime(todo["date"], "%Y-%m-%d %H:%M").date()

score = st.session_state.score

if score < 30:
    pet_level = 1
    pet_stage = "🐣 알"
    pet_message = "아직 작은 알이에요!"
elif score < 70:
    pet_level = 2
    pet_stage = "🐥 아기"
    pet_message = "조금씩 성장하고 있어요!"
elif score < 120:
    pet_level = 3
    pet_stage = "🐤 어린이"
    pet_message = "열심히 성장 중!"
elif score < 200:
    pet_level = 4
    pet_stage = "🐦 청소년"
    pet_message = "갓생력이 상당합니다!"
else:
    pet_level = 5
    pet_stage = "🦅 최종 진화"
    pet_message = "당신은 갓생의 신입니다!"

next_level_scores = {
    1: 30,
    2: 70,
    3: 120,
    4: 200,
    5: 200
}

if pet_level < 5:
    current_min = {
        1: 0,
        2: 30,
        3: 70,
        4: 120
    }[pet_level]

    next_score = next_level_scores[pet_level]
    progress = (score - current_min) / (next_score - current_min)
    progress = max(0, min(progress, 1))
else:
    progress = 1
    next_score = score

GIF_PATH = "tamagotchi.gif"

def create_tamagotchi_gif(path):
    frames = []
    size = (260, 260)

    for i in range(8):
        img = Image.new("RGB", size, (255, 248, 235))
        draw = ImageDraw.Draw(img)

        offset_y = 0

        if i in [1, 2]:
            offset_y = -5
        elif i in [5, 6]:
            offset_y = 5

        cx = 130
        cy = 125 + offset_y

        draw.ellipse(
            (cx - 70, cy - 60, cx + 70, cy + 75),
            fill=(255, 217, 102),
            outline=(120, 90, 40),
            width=4
        )

        if i in [3, 4]:
            draw.line(
                (cx - 35, cy - 5, cx - 15, cy - 5),
                fill=(40, 40, 40),
                width=5
            )
            draw.line(
                (cx + 15, cy - 5, cx + 35, cy - 5),
                fill=(40, 40, 40),
                width=5
            )
        else:
            draw.ellipse(
                (cx - 35, cy - 15, cx - 15, cy + 8),
                fill=(40, 40, 40)
            )
            draw.ellipse(
                (cx + 15, cy - 15, cx + 35, cy + 8),
                fill=(40, 40, 40)
            )

        if i in [0, 1, 7]:
            draw.arc(
                (cx - 20, cy + 5, cx + 20, cy + 35),
                0,
                180,
                fill=(60, 40, 40),
                width=4
            )
        else:
            draw.ellipse(
                (cx - 7, cy + 10, cx + 7, cy + 24),
                fill=(80, 50, 50)
            )

        draw.ellipse(
            (cx - 58, cy + 10, cx - 40, cy + 28),
            fill=(255, 150, 150)
        )
        draw.ellipse(
            (cx + 40, cy + 10, cx + 58, cy + 28),
            fill=(255, 150, 150)
        )

        frames.append(img)

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=180,
        loop=0
    )

if not os.path.exists(GIF_PATH):
    create_tamagotchi_gif(GIF_PATH)

with open(GIF_PATH, "rb") as f:
    gif_bytes = f.read()

gif_base64 = base64.b64encode(gif_bytes).decode()

st.markdown(
    f"""
    <div class="pet-box">
        <img src="data:image/gif;base64,{gif_base64}" width="210">
        <div class="pet-name">{pet_stage}</div>
        <div class="pet-level">Lv.{pet_level}</div>
        <p>{pet_message}</p>
    </div>
    """,
    unsafe_allow_html=True
)

if pet_level < 5:
    st.progress(progress)
    st.markdown(
        f"""
        <div class="progress-text">
        ⭐ 현재 점수: <b>{score}</b> / 다음 진화: <b>{next_score}</b>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.success("🏆 최종 진화 완료!")

st.write("---")

st.markdown(
    f"""
    <div class="stat-box">
        🌟 <b>생산성 점수:</b> {st.session_state.score} 점
        &nbsp; | &nbsp;
        ✅ <b>완료한 목표:</b> {st.session_state.completed_count} 개
        &nbsp; | &nbsp;
        🐣 <b>다마고치:</b> Lv.{pet_level}
    </div>
    """,
    unsafe_allow_html=True
)

with st.form("add_todo_form", clear_on_submit=True):
    col1, col2 = st.columns([0.8, 0.2])

    with col1:
        new_task = st.text_input(
            "새로운 목표",
            label_visibility="collapsed",
            placeholder="예: 수학 문제 20개 풀기 📚"
        )

    with col2:
        submitted = st.form_submit_button("➕ 추가")

    if submitted and new_task.strip():
        st.session_state.todos.append({
            "task": new_task.strip(),
            "done": False,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        st.toast("새로운 목표가 추가되었습니다! 🚀", icon="✅")
        st.rerun()

st.write("---")

st.subheader("📅 목표 기간")

period = st.radio(
    "목표 보기",
    ["오늘", "이번 주", "전체"],
    horizontal=True
)

if period == "오늘":
    filtered_todos = [
        todo for todo in st.session_state.todos
        if todo_date(todo) == today
    ]
    period_description = f"{today.strftime('%Y-%m-%d')} 목표"

elif period == "이번 주":
    filtered_todos = [
        todo for todo in st.session_state.todos
        if week_start <= todo_date(todo) <= week_end
    ]
    period_description = (
        f"{week_start.strftime('%m/%d')} ~ "
        f"{week_end.strftime('%m/%d')} 목표"
    )

else:
    filtered_todos = st.session_state.todos.copy()
    period_description = "전체 목표"

active_todos = [
    todo for todo in filtered_todos
    if not todo["done"]
]

done_todos = [
    todo for todo in filtered_todos
    if todo["done"]
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎯 전체 목표", len(filtered_todos))

with col2:
    st.metric("🚀 진행 중", len(active_todos))

with col3:
    st.metric("🎉 완료", len(done_todos))

st.caption(period_description)
st.write("---")

tab1, tab2 = st.tabs([
    f"🚀 진행 중 ({len(active_todos)})",
    f"🎉 완료됨 ({len(done_todos)})"
])

with tab1:
    if not active_todos:
        st.info("현재 기간에 진행 중인 목표가 없습니다! 🎯")
    else:
        for idx, todo in enumerate(st.session_state.todos):
            if todo["done"]:
                continue

            if todo not in filtered_todos:
                continue

            c1, c2, c3 = st.columns([0.1, 0.75, 0.15])

            with c1:
                if st.button(
                    "⭕",
                    key=f"check_{idx}",
                    help="목표 완료하기"
                ):
                    todo["done"] = True
                    st.session_state.score += 10
                    st.session_state.completed_count += 1

                    st.toast(
                        "목표 달성! 다마고치가 기뻐합니다! 🎉",
                        icon="🐣"
                    )

                    st.balloons()
                    st.rerun()

            with c2:
                st.markdown(
                    f"""
                    <div class='task-text'>{todo['task']}</div>
                    <div class='task-date'>{todo['date']} 추가됨</div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:
                if st.button(
                    "🗑️",
                    key=f"del_active_{idx}"
                ):
                    st.session_state.todos.pop(idx)
                    st.rerun()

with tab2:
    if not done_todos:
        st.info("아직 완료된 목표가 없습니다. 첫 목표를 달성해 보세요! 🔥")
    else:
        for idx, todo in enumerate(st.session_state.todos):
            if not todo["done"]:
                continue

            if todo not in filtered_todos:
                continue

            c1, c2, c3 = st.columns([0.1, 0.75, 0.15])

            with c1:
                if st.button(
                    "↩️",
                    key=f"undo_{idx}",
                    help="진행 중으로 되돌리기"
                ):
                    todo["done"] = False

                    st.session_state.score = max(
                        0,
                        st.session_state.score - 10
                    )

                    st.session_state.completed_count = max(
                        0,
                        st.session_state.completed_count - 1
                    )

                    st.rerun()

            with c2:
                st.markdown(
                    f"""
                    <del style='color:gray; font-size:16px;'>
                    {todo['task']}
                    </del>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class='task-date'>
                    {todo['date']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:
                if st.button(
                    "🗑️",
                    key=f"del_done_{idx}"
                ):
                    st.session_state.todos.pop(idx)
                    st.rerun()

st.write("---")
st.subheader("🐣 다마고치 성장 정보")

growth_data = [
    ("Lv.1", "🐣 알", "0점"),
    ("Lv.2", "🐥 아기", "30점"),
    ("Lv.3", "🐤 어린이", "70점"),
    ("Lv.4", "🐦 청소년", "120점"),
    ("Lv.5", "🦅 최종 진화", "200점")
]

for level, name, required in growth_data:
    st.write(f"**{level} — {name}** · {required}")
```
