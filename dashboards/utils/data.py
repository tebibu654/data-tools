import streamlit as st


def export_data(title, df):
    csv = df.to_csv(index=False).encode("utf-8")

    st.write(f"### {title}")
    st.download_button(
        f"Download CSV", csv, "export.csv", "text/csv", key=f"{title}-csv"
    )
    st.write(df.head(25))
