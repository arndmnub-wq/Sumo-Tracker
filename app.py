import inspect

import streamlit as st

from api import get_bouts
from components import (
    render_match_card,
    render_navigation,
    render_sidebar,
)


st.set_page_config(
    page_title="Sumo Tracker",
    layout="wide",
)


BASHO_OPTIONS = {
    "July 2026 (Nagoya)": "202607",
}

DIVISION_OPTIONS = [
    "Makuuchi",
    "Juryo",
    "Makushita",
    "Sandanme",
    "Jonidan",
    "Jonokuchi",
]

st.title("Sumo Tracker")
st.caption("Personal Watch Along Dashboard")

st.divider()

selector_col1, selector_col2, selector_col3 = st.columns(3)

# Create margins on the left and right
left_margin, center, right_margin = st.columns([1, 4, 1])

with center:
    selector_col1, selector_col2, selector_col3 = st.columns(3)

    with selector_col1:
        basho_name = st.selectbox(
            "Tournament",
            list(BASHO_OPTIONS.keys()),
        )

    with selector_col2:
        division = st.selectbox(
            "Division",
            DIVISION_OPTIONS,
        )

    with selector_col3:
        day = st.selectbox(
            "Day",
            range(1, 16),
        )

basho_id = BASHO_OPTIONS[basho_name]

st.divider()

try:
    bout_data = get_bouts(basho_id, division, day)
    torikumi = bout_data.get("torikumi", [])

    if not torikumi:
        st.warning("No bouts were found for this day.")
        st.stop()

    if "selected_bout" not in st.session_state:
        st.session_state.selected_bout = 0

    current_selection = (
        basho_id,
        division,
        day,
    )

    if st.session_state.get("current_selection") != current_selection:
        st.session_state.selected_bout = 0
        st.session_state.current_selection = current_selection

    if st.session_state.selected_bout >= len(torikumi):
        st.session_state.selected_bout = 0

    selected_index = st.session_state.selected_bout
    selected_bout = torikumi[selected_index]

    render_sidebar(
        basho_name=basho_name,
        division=division,
        day=day,
        torikumi=torikumi,
        selected_index=selected_index,
    )

    st.subheader(f"{basho_name} — {division} — Day {day}")

    render_navigation(
        selected_index=selected_index,
        total_bouts=len(torikumi),
    )

    render_match_card(selected_bout)

except Exception as error:
    st.error("The bout data could not be loaded.")
    st.exception(error)