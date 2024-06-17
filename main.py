import streamlit as st
import base64
from streamlit_option_menu import option_menu

import data
import recettes


st.set_page_config(
    page_title="PTEAH",
    page_icon="images/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


# mettre une image en fond d'écran
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = (
        """
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    """
        % bin_str
    )
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background("images/background.png")

with st.sidebar:
    st.sidebar.image(
        "images/logo_sidebar.png",
        width=250,
    )
    selected = option_menu(
        menu_title=None,
        options=[
            "ANALYSE",
            "RECETTES",
        ],
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#b5b5b5",
                "border-radius": "1px",
            },
            "nav-link": {
                "font-size": "12px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
                "color": "#ffffff",
            },
            "nav-link-selected": {"background-color": "#5f5f5f"},
        },
    )


def local_css(css_file_path):
    with open(css_file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")


if selected == "RECETTES":
    recettes.show()
    pass
elif selected == "ANALYSE":
    data.show()
