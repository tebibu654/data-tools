import streamlit as st
import base64
from pathlib import Path
import urllib.parse


def encode_svg_for_css(svg):
    svg_one_line = svg.replace("\n", " ").replace('"', "'")
    return urllib.parse.quote(svg_one_line)


def sidebar_logo():
    LOGO_URL = "dashboards/static/logo.png"
    HEIGHT = 28
    logo = f"url(data:image/png;base64,{base64.b64encode(Path(LOGO_URL).read_bytes()).decode()})"

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarHeader"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {HEIGHT - 10}px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_icon():
    burger_svg = """<svg width="18" height="15" viewBox="0 0 18 15" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M0.512695 1.31128C0.512695 0.897066 0.848482 0.561279 1.2627 0.561279H16.2627C16.6769 0.561279 17.0127 0.897066 17.0127 1.31128C17.0127 1.72549 16.6769 2.06128 16.2627 2.06128H1.2627C0.848482 2.06128 0.512695 1.72549 0.512695 1.31128Z" fill="white"/>
<path d="M0.512695 7.31128C0.512695 6.89707 0.848482 6.56128 1.2627 6.56128H16.2627C16.6769 6.56128 17.0127 6.89707 17.0127 7.31128C17.0127 7.72549 16.6769 8.06128 16.2627 8.06128H1.2627C0.848482 8.06128 0.512695 7.72549 0.512695 7.31128Z" fill="white"/>
<path d="M1.2627 12.5613C0.848482 12.5613 0.512695 12.8971 0.512695 13.3113C0.512695 13.7255 0.848482 14.0613 1.2627 14.0613H16.2627C16.6769 14.0613 17.0127 13.7255 17.0127 13.3113C17.0127 12.8971 16.6769 12.5613 16.2627 12.5613H1.2627Z" fill="white"/>
</svg>
    """
    encoded_svg = encode_svg_for_css(burger_svg)
    custom_css = f"""
    <style>
        [data-testid="stSidebarCollapseButton"] button svg {{
            display: none;
        }}
        
        [data-testid="stSidebarCollapseButton"] button::after {{
            content: '';
            display: block;
            width: 24px;
            height: 24px;
            background-image: url("data:image/svg+xml,{encoded_svg}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center center;
        }}

        [data-testid="stSidebarCollapsedControl"] button svg {{
            display: none;
        }}
        
        [data-testid="stSidebarCollapsedControl"] button::after {{
            content: '';
            display: block;
            width: 24px;
            height: 24px;
            background-image: url("data:image/svg+xml,{encoded_svg}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center center;
        }}
        
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
