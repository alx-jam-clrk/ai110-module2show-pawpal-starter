import streamlit as st
from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# ── 1. OWNER ─────────────────────────────────────────────────────────────────
st.subheader("Owner")

if st.session_state.owner is None:
    owner_name = st.text_input("Owner name", value="Jordan")
    owner_id   = st.text_input("Owner ID",   value="owner_001")
    if st.button("Create Owner"):
        st.session_state.owner = Owner(owner_name=owner_name, owner_id=owner_id)
        st.rerun()
else:
    owner: Owner = st.session_state.owner
    st.success(f"Owner: **{owner.owner_name}** (ID: {owner.owner_id})")

    with st.expander("Edit preferences"):
        pref_key   = st.text_input("Preference key",   value="morning_priority", key="pref_k")
        pref_value = st.text_input("Preference value", value="True",             key="pref_v")
        if st.button("Save preference"):
            owner.edit_preferences({pref_key: pref_value})
            st.success(f"Saved: {pref_key} = {pref_value}")

st.divider()

# ── 2. PETS ──────────────────────────────────────────────────────────────────
st.subheader("Pets")

if st.session_state.owner is None:
    st.info("Create an owner first.")
else:
    owner: Owner = st.session_state.owner

    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        pet_id = st.text_input("Pet ID", value="pet_001")

    if st.button("Add Pet"):
        owner.pets.append(Pet(pet_name=pet_name, owner_name=owner.owner_name, pet_id=pet_id))
        st.rerun()

    if owner.pets:
        st.write(f"Pets on file ({', '.join(owner.scheduler.pet_names) or 'none scheduled yet'}):")
        st.table([{"name": p.pet_name, "id": p.pet_id} for p in owner.pets])
    else:
        st.info("No pets yet. Add one above.")

st.divider()

# ── 3. TASKS ─────────────────────────────────────────────────────────────────
st.subheader("Tasks")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.info("Create an owner and at least one pet before adding tasks.")
else:
    owner: Owner = st.session_state.owner
    pet_names    = [p.pet_name for p in owner.pets]

    # Add task
    with st.expander("Add a task", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title  = st.text_input("Title", value="Morning walk")
        with col2:
            start_time  = st.number_input("Start time (hour 0-23)", min_value=0, max_value=23, value=8)
        with col3:
            duration    = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)

        col4, col5 = st.columns(2)
        with col4:
            frequency    = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
        with col5:
            assigned_pet = st.selectbox("Assign to pet", pet_names)

        constraints_raw = st.text_input("Constraints (comma-separated, optional)", value="")

        if st.button("Add Task"):
            constraints = [c.strip() for c in constraints_raw.split(",") if c.strip()]
            new_task = Task(
                title=task_title,
                pet_name=assigned_pet,
                start_time=int(start_time),
                duration=int(duration),
                frequency=frequency,
                constraints=constraints,
            )
            try:
                owner.add_task(new_task)
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    # Task table
    all_tasks = owner.view_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table([
            {
                "title":           t.title,
                "pet":             t.pet_name,
                "start":           f"{t.start_time}:00",
                "duration (min)":  t.duration,
                "frequency":       t.frequency,
                "constraints":     ", ".join(t.constraints) if t.constraints else "—",
                "done":            t.completed,
            }
            for t in all_tasks
        ])

        # Mark complete
        with st.expander("Mark a task complete"):
            task_titles  = [t.title for t in all_tasks]
            selected     = st.selectbox("Select task", task_titles, key="complete_sel")
            if st.button("Mark complete"):
                target = next(t for t in all_tasks if t.title == selected)
                owner.complete_task(target)
                st.rerun()

        # Delete task
        with st.expander("Delete a task"):
            del_titles = [t.title for t in all_tasks]
            del_sel    = st.selectbox("Select task to delete", del_titles, key="delete_sel")
            if st.button("Delete task"):
                target = next(t for t in all_tasks if t.title == del_sel)
                try:
                    owner.delete_task(target)
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ── 4. SCHEDULE ───────────────────────────────────────────────────────────────
st.subheader("Schedule")

if st.session_state.owner is None or not st.session_state.owner.view_tasks():
    st.info("Add tasks before building a schedule.")
else:
    owner: Owner = st.session_state.owner

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Build & View Schedule"):
            try:
                owner.build_schedule()
                st.text(owner.view_schedule())
            except ValueError as e:
                st.error(str(e))
    with col2:
        if st.button("Explain Schedule"):
            try:
                owner.build_schedule()
                st.text(owner.scheduler.explain_schedule(preferences=owner.preferences))
            except ValueError as e:
                st.error(str(e))
