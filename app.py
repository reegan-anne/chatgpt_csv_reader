import streamlit as st
import pandas as pd
from file_utils import save_locally

uploaded_file = st.file_uploader("Choose a CSV file")

if uploaded_file is not None:
    # Display df
    df = pd.read_csv(uploaded_file)
    st.caption('File data recieved:')
    st.dataframe(df)

    # Save csv file locally
    data = uploaded_file.getvalue().decode('utf-8')
    file_location = save_locally(data, uploaded_file)
    st.write(file_location)

else:
    pass
