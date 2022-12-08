import pandas as pd
import psycopg2
import streamlit as st


@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])


conn = init_connection()
df = pd.read_sql("SELECT * from coloradoski;", conn)
person_set = set(
    (v["first"].lower(), v["last"].lower()) for v in df.to_dict(orient="records")
)

st.dataframe(df)

col1, col2 = st.columns([1, 1])
with col1:
    first = st.text_input("First Name", value="", max_chars=80)
with col2:
    last = st.text_input("Last Initial", value="", max_chars=1)

disabled = False
help_ = ""
if not first:
    help_ = "First name missing"
    disabled = True
if not last:
    help_ = (
        "Last initial missing"
        if not help_
        else "First name and last initial are missing"
    )
    disabled = True
if (first.lower(), last.lower()) in person_set:
    help_ = "Already signed up"
    disabled = True


def sign_up(first, last, conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO coloradoski (first, last) VALUES (%s, %s)", (first, last))
    conn.commit()
    st.snow()


st.button(
    "Sign up",
    on_click=sign_up,
    disabled=disabled,
    help=help_,
    kwargs={"first": first.title().strip(), "last": last.title().strip(), "conn": conn},
)
