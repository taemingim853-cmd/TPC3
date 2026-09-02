```python
import streamlit as st
from datetime import datetime, date, timedelta
from PIL import Image, ImageDraw
import os
import base64

# =========================================================
# 기본 설정
# =========================================================
st.set_page_config(
    page_title="갓생 투두 & 다마고치",
    page_icon="🐣",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
.title-box {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 30px;
    font-weight: 900;
    margin-bottom: 20px;
}

.stat-box {
    background: #f3f4f6;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.pet-box {
    background: linear-gradient(135deg, #fff7ed, #fef3c7);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.pet-name {
    font-size: 28px;
    font-weight: 900;
}

.pet-level {
    font-size: 18px;
    font-weight: 700;
}

.task-text {
    font-size: 16px;
    font-weight: 600;
}

.task-date {
    font-size: 12px;
    color: #6b7280;
}
</style>

<div class="title-box">
🐣 갓생 투두 & 다마고치
</div>
""", unsafe_allow_html=True)

# =========================================================
# 세션 데이터
# =========================================================
if "todos" not in st.session_state:
    st.session_state.todos = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "completed_count" not in st.session_state:
    st.session_state.completed_count = 0

# =========================================================
# 날짜
# =========================================================
today = date.today()
week_start = today - timedelta(days=today.weekday())
week_end = week_start + timedelta(days=6)


def get_todo_date(todo):
    try:
        return datetime.strptime(
            todo["date"],
            "%Y-%m-%d %H:%M"
        ).date()
    except (ValueError, TypeError, KeyError):
        return today


# =========================================================
# 다마고치 레벨
# =========================================================
score = st.session_state.score

if score < 30:
    level = 1
    pet = "🐣"
    pet_name = "알"
    message = "아직 작은 알이에요!"
elif score < 70:
    level = 2
    pet = "🐥"
    pet_name = "아기"
    message = "조금씩 성장하고 있어요!"
elif score < 120:
    level = 3
    pet = "🐤"
    pet_name = "어린이"
    message = "열심히 성장 중!"
elif score < 200:
    level = 4
    pet = "🐦"
    pet_name = "청소년"
    message = "갓생력이 상당합니다!"
else:
    level = 5
    pet = "🦅"
    pet_name = "최종 진화"
    message = "갓생의 신이 되었습니다!"

# =========================================================
# GIF 생성
# =========================================================
gif_path = "tamagotchi.gif"


def create_gif(path):
    frames = []
    width = 220
    height = 220

    for i in range(8):
        image = Image.new("RGB", (width, height), (255, 248, 235))
        draw = ImageDraw.Draw(image)

        # 위아래 움직임
        if i in (1, 2):
            y = 100
        elif i in (5, 6):
            y = 108
        else:
            y = 104

        x = 110

        # 몸
        draw.ellipse(
            (x - 55, y - 55, x + 55, y + 55),
            fill=(255, 220, 100),
            outline=(100, 80, 40),
            width=4
        )

        # 눈
        if i in (3, 4):
            draw.line(
                (x - 28, y - 8, x - 12, y - 8),
                fill=(30, 30, 30),
                width=4
            )
            draw.line(
                (x + 12, y - 8, x + 28, y - 8),
                fill=(30, 30, 30),
                width=4
            )
        else:
            draw.ellipse(
                (x - 30, y - 16, x - 12, y + 4),
                fill=(30, 30, 30)
            )
            draw.ellipse(
                (x + 12, y - 16, x + 30, y + 4),
                fill=(30, 30, 30)
            )

        # 입
        draw.arc(
            (x - 18, y + 5, x + 18, y + 28),
            0,
            180,
            fill=(80, 50, 50),
            width=3
        )

        # 볼
        draw.ellipse(
            (x - 48, y + 10, x - 32, y + 25),
            fill=(255, 150, 150)
        )
        draw.ellipse(
            (x + 32, y + 10, x + 48, y + 25),
            fill=(255, 150, 150)
        )

        frames.append(image)

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=180,
        loop=0
    )


if not os.path.exists(gif_path):
    create_gif(gif_path)

# =========================================================
# 다마고치 표시
# =========================================================
try:
    with open(gif_path, "rb") as file:
        gif_data = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <div class="pet-box">
            <img src="data:image/gif;base64,{gif_data}" width="180">
            <div class="pet-name">{pet} {pet_name}</div>
            <div class="pet-level">Lv.{level}</div>
            <div>{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
except Exception:
    st.markdown(
        f"""
        <div class="pet-box">
            <div style="font-size:90px;">{pet}</div>
            <div class="pet-name">{pet_name}</div>
            <div class="pet-level">Lv.{level}</div>
            <div>{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 경험치
# =========================================================
if level == 1:
    current = 0
    target = 30
elif level == 2:
    current = 30
    target = 70
elif level == 3:
    current = 70
    target = 120
elif level == 4:
    current = 120
    target = 200
else:
    current = 200
    target = 200

if level < 5:
    progress = (score - current) / (target - current)
    progress = max(0.0, min(1.0, progress))
    st.progress(progress)
    st.caption(f"⭐ {score}점 / 다음 진화 {target}점")
else:
    st.success("🏆 최종 진화 완료!")

# =========================================================
# 스탯
# =========================================================
st.markdown(
    f"""
    <div class="stat-box">
        🌟 <b>생산성 점수:</b> {st.session_state.score}점
        &nbsp;&nbsp;|&nbsp;&nbsp;
        ✅ <b>완료:</b> {st.session_state.completed_count}개
        &nbsp;&nbsp;|&nbsp;&nbsp;
        🐣 <b>Lv.{level}</b>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 목표 추가
# =========================================================
with st.form("add_todo_form", clear_on_submit=True):
    col1, col2 = st.columns([0.8, 0.2])

    with col1:
        new_task = st.text_input(
            "목표",
            placeholder="예: 수학 공부 1시간",
            label_visibility="collapsed"
        )

    with col2:
        submit = st.form_submit_button("➕ 추가")

    if submit:
        task = new_task.strip()

        if task:
            st.session_state.todos.append({
                "task": task,
                "done": False,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.toast("목표가 추가되었습니다! 🚀")
            st.rerun()

# =========================================================
# 기간 선택
# =========================================================
st.subheader("📅 목표 기간")

period = st.radio(
    "기간",
    ["오늘", "이번 주", "전체"],
    horizontal=True,
    label_visibility="collapsed"
)

# =========================================================
# 기간 필터
# =========================================================
if period == "오늘":
    filtered_todos = [
        todo for todo in st.session_state.todos
        if get_todo_date(todo) == today
    ]

elif period == "이번 주":
    filtered_todos = [
        todo for todo in st.session_state.todos
        if week_start <= get_todo_date(todo) <= week_end
    ]

else:
    filtered_todos = list(st.session_state.todos)

active_todos = [
    todo for todo in filtered_todos
    if not todo["done"]
]

done_todos = [
    todo for todo in filtered_todos
    if todo["done"]
]

# =========================================================
# 기간 통계
# =========================================================
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🎯 전체", len(filtered_todos))

with c2:
    st.metric("🚀 진행 중", len(active_todos))

with c3:
    st.metric("🎉 완료", len(done_todos))

# =========================================================
# 탭
# =========================================================
tab1, tab2 = st.tabs([
    f"🚀 진행 중 ({len(active_todos)})",
    f"🎉 완료 ({len(done_todos)})"
])

# =========================================================
# 진행 중
# =========================================================
with tab1:
    if not active_todos:
        st.info("진행 중인 목표가 없습니다! 🎯")

    for idx, todo in enumerate(st.session_state.todos):

        if todo["done"]:
            continue

        if todo not in filtered_todos:
            continue

        c1, c2, c3 = st.columns([0.12, 0.73, 0.15])

        with c1:
            if st.button(
                "⭕",
                key=f"check_{idx}"
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
                <div class="task-text">
                    {todo['task']}
                </div>
                <div class="task-date">
                    {todo['date']} 추가됨
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            if st.button(
                "🗑️",
                key=f"delete_active_{idx}"
            ):
                st.session_state.todos.pop(idx)
                st.rerun()

# =========================================================
# 완료
# =========================================================
with tab2:
    if not done_todos:
        st.info("완료된 목표가 없습니다. 🔥")

    for idx, todo in enumerate(st.session_state.todos):

        if not todo["done"]:
            continue

        if todo not in filtered_todos:
            continue

        c1, c2, c3 = st.columns([0.12, 0.73, 0.15])

        with c1:
            if st.button(
                "↩️",
                key=f"undo_{idx}"
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
                <del style="color:gray; font-size:16px;">
                    {todo['task']}
                </del>
                <div class="task-date">
                    {todo['date']}
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            if st.button(
                "🗑️",
                key=f"delete_done_{idx}"
            ):
                st.session_state.todos.pop(idx)
                st.rerun()

# =========================================================
# 성장 정보
# =========================================================
st.write("---")
st.subheader("🐣 다마고치 성장 단계")

growth = [
    ("Lv.1", "🐣 알", "0점"),
    ("Lv.2", "🐥 아기", "30점"),
    ("Lv.3", "🐤 어린이", "70점"),
    ("Lv.4", "🐦 청소년", "120점"),
    ("Lv.5", "🦅 최종 진화", "200점"),
]

for lv, name, required in growth:
    st.write(f"**{lv} — {name}** · {required}")
```
