```python
import streamlit as st
from datetime import datetime, date, timedelta

# =========================================================
# 기본 설정
# =========================================================
st.set_page_config(
    page_title="갓생 투두 & 다마고치",
    page_icon="🐣",
    layout="centered"
)

# =========================================================
# 스타일
# =========================================================
st.markdown("""
<style>
.title-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-weight: 900;
    font-size: 30px;
    margin-bottom: 20px;
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
    background-color: #fff7ed;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
}

.pet {
    font-size: 90px;
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
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title-box">🐣 갓생 투두 & 다마고치</div>',
    unsafe_allow_html=True
)

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


def get_date(todo):
    return datetime.strptime(
        todo["date"],
        "%Y-%m-%d %H:%M"
    ).date()


# =========================================================
# 다마고치
# =========================================================
score = st.session_state.score

if score < 30:
    pet = "🥚"
    pet_name = "알"
    level = 1
    message = "열심히 목표를 달성해서 다마고치를 키워보세요!"

elif score < 70:
    pet = "🐣"
    pet_name = "아기"
    level = 2
    message = "조금씩 성장하고 있어요!"

elif score < 120:
    pet = "🐥"
    pet_name = "어린이"
    level = 3
    message = "아주 잘하고 있어요!"

elif score < 200:
    pet = "🐤"
    pet_name = "청소년"
    level = 4
    message = "갓생력이 올라가고 있습니다!"

else:
    pet = "🦅"
    pet_name = "최종 진화"
    level = 5
    message = "최고의 갓생러입니다!"

st.markdown(
    f"""
    <div class="pet-box">
        <div class="pet">{pet}</div>
        <h2>{pet_name}</h2>
        <h3>Lv.{level}</h3>
        <p>{message}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 경험치
# =========================================================
if level == 1:
    current_score = 0
    next_score = 30
elif level == 2:
    current_score = 30
    next_score = 70
elif level == 3:
    current_score = 70
    next_score = 120
elif level == 4:
    current_score = 120
    next_score = 200
else:
    current_score = 200
    next_score = 200

if level < 5:
    progress = (
        (score - current_score)
        / (next_score - current_score)
    )

    progress = max(0.0, min(1.0, progress))

    st.progress(progress)
    st.caption(
        f"⭐ {score}점 / 다음 진화 {next_score}점"
    )
else:
    st.success("🏆 최종 진화 완료!")

# =========================================================
# 상단 스탯
# =========================================================
st.markdown(
    f"""
    <div class="stat-box">
        🌟 <b>생산성 점수:</b> {st.session_state.score}점
        &nbsp;&nbsp;|&nbsp;&nbsp;
        ✅ <b>완료한 목표:</b> {st.session_state.completed_count}개
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 목표 추가
# =========================================================
with st.form("add_todo_form", clear_on_submit=True):

    new_task = st.text_input(
        "새로운 목표",
        placeholder="예: 수학 공부 1시간",
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button(
        "➕ 목표 추가"
    )

    if submitted and new_task.strip():

        st.session_state.todos.append({
            "task": new_task.strip(),
            "done": False,
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        })

        st.rerun()

st.write("---")

# =========================================================
# 목표 기간
# =========================================================
st.subheader("📅 목표 보기")

period = st.radio(
    "기간 선택",
    ["오늘", "이번 주", "전체"],
    horizontal=True
)

# =========================================================
# 필터
# =========================================================
if period == "오늘":

    filtered_indices = []

    for i, todo in enumerate(st.session_state.todos):
        if get_date(todo) == today:
            filtered_indices.append(i)

elif period == "이번 주":

    filtered_indices = []

    for i, todo in enumerate(st.session_state.todos):
        todo_day = get_date(todo)

        if week_start <= todo_day <= week_end:
            filtered_indices.append(i)

else:

    filtered_indices = list(
        range(len(st.session_state.todos))
    )

# =========================================================
# 통계
# =========================================================
active_count = 0
done_count = 0

for i in filtered_indices:

    if st.session_state.todos[i]["done"]:
        done_count += 1
    else:
        active_count += 1

total_count = len(filtered_indices)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎯 전체", total_count)

with col2:
    st.metric("🚀 진행 중", active_count)

with col3:
    st.metric("🎉 완료", done_count)

st.write("---")

# =========================================================
# 탭
# =========================================================
tab1, tab2 = st.tabs([
    f"🚀 진행 중 ({active_count})",
    f"🎉 완료 ({done_count})"
])

# =========================================================
# 진행 중
# =========================================================
with tab1:

    if active_count == 0:

        st.info(
            "진행 중인 목표가 없습니다!"
        )

    else:

        for i in filtered_indices:

            todo = st.session_state.todos[i]

            if todo["done"]:
                continue

            c1, c2, c3 = st.columns(
                [0.12, 0.73, 0.15]
            )

            with c1:

                if st.button(
                    "⭕",
                    key=f"check_{i}"
                ):

                    st.session_state.todos[i]["done"] = True

                    st.session_state.score += 10

                    st.session_state.completed_count += 1

                    st.toast(
                        "목표 달성! +10점 🎉"
                    )

                    st.rerun()

            with c2:

                st.markdown(
                    f"""
                    <div class="task-text">
                        {todo["task"]}
                    </div>

                    <div class="task-date">
                        {todo["date"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:

                if st.button(
                    "🗑️",
                    key=f"delete_{i}"
                ):

                    st.session_state.todos.pop(i)

                    st.rerun()


# =========================================================
# 완료
# =========================================================
with tab2:

    if done_count == 0:

        st.info(
            "아직 완료된 목표가 없습니다."
        )

    else:

        for i in filtered_indices:

            todo = st.session_state.todos[i]

            if not todo["done"]:
                continue

            c1, c2, c3 = st.columns(
                [0.12, 0.73, 0.15]
            )

            with c1:

                if st.button(
                    "↩️",
                    key=f"undo_{i}"
                ):

                    st.session_state.todos[i]["done"] = False

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
                    <del style="color: gray; font-size: 16px;">
                        {todo["task"]}
                    </del>

                    <div class="task-date">
                        {todo["date"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:

                if st.button(
                    "🗑️",
                    key=f"delete_done_{i}"
                ):

                    st.session_state.todos.pop(i)

                    st.rerun()

# =========================================================
# 성장 단계
# =========================================================
st.write("---")

st.subheader("🐣 다마고치 성장 단계")

st.write("🥚 Lv.1 — 알 — 0점")
st.write("🐣 Lv.2 — 아기 — 30점")
st.write("🐥 Lv.3 — 어린이 — 70점")
st.write("🐤 Lv.4 — 청소년 — 120점")
st.write("🦅 Lv.5 — 최종 진화 — 200점")
```
