import streamlit as st

KIMARITE_DEFINITIONS = {
    "kotenage": (
        "An arm-lock throw. The winner wraps an arm around the opponent's "
        "extended arm and throws them without gripping the belt."
    ),
    "yorikiri": (
        "A frontal force-out. The winner maintains body contact and drives "
        "the opponent backward and out of the ring."
    ),
    "oshidashi": (
        "A frontal push-out. The winner pushes the opponent out without "
        "maintaining a belt grip."
    ),
    "hatakikomi": (
        "A slap-down. The winner pulls or slaps the opponent downward as "
        "they move forward."
    ),
    "shitatenage": (
        "An underarm throw performed using an inside grip on the opponent's belt."
    ),
    "uwatenage": (
        "An overarm throw performed using an outside grip on the opponent's belt."
    ),
    "tsukiotoshi": (
        "A thrust-down. The winner drives the opponent down with a thrust "
        "to the upper body."
    ),
    "yoritaoshi": (
        "A frontal crush-out. The winner drives the opponent backward and "
        "down while maintaining close contact."
    ),
}

def select_bout(index: int) -> None:
    """Select a bout from the sidebar."""
    st.session_state.selected_bout = index


def previous_bout() -> None:
    """Move back one bout."""
    if st.session_state.selected_bout > 0:
        st.session_state.selected_bout -= 1


def next_bout(total_bouts: int) -> None:
    """Move forward one bout."""
    if st.session_state.selected_bout < total_bouts - 1:
        st.session_state.selected_bout += 1


def render_sidebar(
    basho_name: str,
    division: str,
    day: int,
    torikumi: list[dict],
    selected_index: int,
) -> None:
    """Draw the daily bout list in the sidebar."""

    with st.sidebar:
        st.header(basho_name)
        st.subheader(division)
        st.write(f"Day {day}")
        st.caption(f"{len(torikumi)} bouts")

        for index, bout in enumerate(torikumi):
            match_no = bout.get("matchNo", index + 1)
            east_name = bout.get("eastShikona", "Unknown")
            west_name = bout.get("westShikona", "Unknown")
            winner = bout.get("winnerEn", "")

            symbol = "✓" if winner else "○"

            label = (
                f"{symbol} Bout {match_no}\n\n"
                f"{east_name} vs {west_name}"
            )

            st.button(
                label,
                key=f"sidebar_bout_{division}_{day}_{index}",
                use_container_width=True,
                type="primary" if index == selected_index else "secondary",
                on_click=select_bout,
                args=(index,),
            )


def render_navigation(
    selected_index: int,
    total_bouts: int,
) -> None:
    """Draw the previous and next bout buttons."""

    previous_col, counter_col, next_col = st.columns([1, 2, 1])

    with previous_col:
        st.button(
            "◀ Previous Bout",
            use_container_width=True,
            disabled=selected_index == 0,
            on_click=previous_bout,
        )

    with counter_col:
        st.markdown(
            (
                "<h3 style='text-align:center;'>"
                f"Bout {selected_index + 1} of {total_bouts}"
                "</h3>"
            ),
            unsafe_allow_html=True,
        )

    with next_col:
        st.button(
            "Next Bout ▶",
            use_container_width=True,
            disabled=selected_index == total_bouts - 1,
            on_click=next_bout,
            args=(total_bouts,),
        )


def render_match_card(bout: dict) -> None:
    """Draw the selected bout."""

    match_no = bout.get("matchNo", "—")

    east_name = bout.get("eastShikona", "Unknown")
    east_rank = bout.get("eastRank", "Rank unavailable")

    west_name = bout.get("westShikona", "Unknown")
    west_rank = bout.get("westRank", "Rank unavailable")

    winner = bout.get("winnerEn", "")
    kimarite = bout.get("kimarite", "")

    with st.container(border=True):
        st.markdown(
            f"<h2 style='text-align:center;'>Bout {match_no}</h2>",
            unsafe_allow_html=True,
        )

        east_col, versus_col, west_col = st.columns([4, 1, 4])

        with east_col:
            st.caption("EAST")
            st.markdown(
                f"<h2 style='text-align:center;'>{east_name}</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align:center;'>{east_rank}</p>",
                unsafe_allow_html=True,
            )

        with versus_col:
            st.markdown(
                "<h2 style='text-align:center;padding-top:35px;'>VS</h2>",
                unsafe_allow_html=True,
            )

        with west_col:
            st.caption("WEST")
            st.markdown(
                f"<h2 style='text-align:center;'>{west_name}</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align:center;'>{west_rank}</p>",
                unsafe_allow_html=True,
            )

        st.divider()

        if winner:
            normalized_kimarite = kimarite.strip().lower()

            st.success(
                f"🏆 {winner} won by **{normalized_kimarite.title()}**"
            )

            definition = KIMARITE_DEFINITIONS.get(normalized_kimarite)

            if definition:
                st.markdown("### Winning Technique")

                st.info(
                    f"**{normalized_kimarite.title()}**\n\n{definition}"
                )
            else:
                st.info(
                    f"**{normalized_kimarite.title()}**\n\n"
                    "Definition coming soon."
                )

        else:
            st.info("The result is not available yet.")
