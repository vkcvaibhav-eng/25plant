import streamlit as st
import pandas as pd
import numpy as np
import io

def generate_row_counts(mean_val, num_plants):
    """Generates whole numbers that sum up to (mean * num_plants)."""
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
st.write("Set your experimental design parameters and paste means to generate the grid.")

# --- Sidebar Inputs (Matching the Screenshot Layout) ---
with st.sidebar:
    st.header("1. Experimental Design")
    num_reps = st.number_input("Number of Replications", min_value=1, value=4, step=1)
    plants_per_rep = st.number_input("Plants per Replication", min_value=1, value=3, step=1)
    
    # Total columns to generate per mean
    total_plants = num_reps * plants_per_rep
    
    st.markdown("---")
    
    st.header("2. Input Means")
    st.info("Paste Treatment Means (comma separated)")
    means_input = st.text_area("Treatment Means", value="10, 12, 14, 13, 15, 11", height=100)

# --- Main Page Output ---
st.write(f"**Current Configuration:** {num_reps} Replications × {plants_per_rep} Plants/Rep = **{total_plants} total columns per treatment**.")

if st.button("Generate Plant Grid"):
    try:
        # Parse the comma-separated means into a list of floats
        # .strip() removes any accidental spaces the user might type
        means_list = [float(m.strip()) for m in means_input.split(",") if m.strip()]
        
        if not means_list:
            st.warning("Please enter valid numeric means.")
        else:
            all_rows = []
            
            for mean in means_list:
                # Generate the whole numbers for this mean
                plant_data = generate_row_counts(mean, total_plants)
                # Append the mean at the end
                row = list(plant_data) + [mean]
                all_rows.append(row)
            
            # Create column names: 1 to total_plants and 'Target Mean'
            columns = [str(i) for i in range(1, total_plants + 1)] + ["Target Mean"]
            result_df = pd.DataFrame(all_rows, columns=columns)
            
            st.success("Grid Generated Successfully!")
            st.dataframe(result_df)
            
            # Export/Download Button
            csv_buffer = io.StringIO()
            result_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download Generated Grid as CSV",
                data=csv_buffer.getvalue(),
                file_name="generated_plant_counts.csv",
                mime="text/csv"
            )
            
    except ValueError:
        # Triggers if the user types letters instead of numbers
        st.error("Invalid input. Please ensure all means are numbers separated by commas (e.g. 10, 12.5, 14).")
