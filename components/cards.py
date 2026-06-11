import streamlit as st

from components.theme import ICON


def kpi_card(icon, title, value, sub_text=None, accent=None, delta_text=None, delta_type="up"):
    """Dense KPI card: a large coloured icon box on the left, metrics on the right.

    `icon` is a Material Symbols name (e.g. "groups"). `accent` is a hex colour;
    it tints the icon, the left border and the icon background.
    """
    accent = accent or ICON["dark"]
    delta_class = "kpi-up" if delta_type == "up" else "kpi-down"
    delta_html = f"<span class='{delta_class}'>{delta_text}</span>" if delta_text else ""

    sub_html = ""
    if (sub_text and str(sub_text).strip()) or delta_html:
        joiner = " &nbsp; " if (sub_text and delta_html) else ""
        sub_html = f'<div class="kpi-sub">{sub_text or ""}{joiner}{delta_html}</div>'

    icon_html = (
        f"<span style=\"font-family:'Material Symbols Rounded';font-size:30px;line-height:1;"
        f"color:{accent};font-variation-settings:'FILL' 0,'wght' 500,'GRAD' 0,'opsz' 24;\">{icon}</span>"
    )

    st.markdown(
        f"""
    <div class="kpi-card" style="border-left-color:{accent};">
        <div class="kpi-icon" style="background:{accent}1a;">{icon_html}</div>
        <div class="kpi-body">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            {sub_html}
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def comparison_card(icon, title, xyz_value, comp_value, unit="", higher_is_better=True, accent=None):
    """KPI card showing the Bank XYZ value with a delta vs the competitor."""
    try:
        gap = float(xyz_value) - float(comp_value)
    except (TypeError, ValueError):
        gap = None

    if gap is None:
        delta_text, delta_type = None, "up"
    else:
        ahead = (gap >= 0) if higher_is_better else (gap <= 0)
        arrow = "▲" if gap >= 0 else "▼"
        delta_text = f"{arrow} {abs(gap):.2f} vs comp."
        delta_type = "up" if ahead else "down"

    value_text = f"{xyz_value}{unit}" if xyz_value is not None else "-"
    sub = f"competitor: {comp_value}{unit}" if comp_value is not None else ""
    kpi_card(icon, title, value_text, sub_text=sub, accent=accent,
             delta_text=delta_text, delta_type=delta_type)
