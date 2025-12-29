import streamlit as st
import pandas as pd
import numpy as np
import io

def generate_row_counts(mean_val, num_plants=25):
    """Generates 25 whole numbers that sum up to (mean * 25)."""
    total_sum = int(round(mean_val * num_plants))
    
    # Generate random weights
    weights = np.random.dirichlet(np.ones(num_plants), size=1)[0]
    # Initial integer distribution
    counts = np.floor(weights * total_sum).astype(int)
    
    # Fill the remainder to ensure the sum is exactly total_sum
    remainder = total_sum - counts.sum()
    indices = np.random.choice(range(num_plants), size=remainder, replace=False)
    for idx in indices:
        counts[idx] += 1
        
    return counts

st.set_page_config(page_title="Plant Data Generator", layout="wide")

st.title("🌱 Insect Count Generator")
st.write("Upload a CSV with mean values to generate a 25-plant whole number grid.")

# 1. File Uploader
uploaded_file = st.file_uploader("Upload your CSV file (Mean values column)", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV
    df_input = pd.read_csv(uploaded_file)
    st.write("### Preview of Uploaded Means", df_input.head())
    
    # Assume the first column contains the mean values
    mean_column = df_input.columns[0]
    
    if st.button("Generate Plant Grid"):
        all_rows = []
        
        for mean in df_input[mean_column]:
            # Generate the 25 whole numbers for this mean
            plant_data = generate_row_counts(float(mean))
            # Append the mean at the end to match your image format
            row = list(plant_data) + [mean]
            all_rows.append(row)
        
        # Create column names: 1 to 25 and 'Mean'
        columns = [str(i) for i in range(1, 26)] + ["Target Mean"]
        result_df = pd.DataFrame(all_rows, columns=columns)
        
        st.success("Grid Generated Successfully!")
        st.dataframe(result_df)
        
        # 2. Export/Download Button
        csv_buffer = io.StringIO()
        result_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Generated Grid as CSV",
            data=csv_buffer.getvalue(),
            file_name="generated_plant_counts.csv",
            mime="text/csv"
        )
