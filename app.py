import streamlit as st
import numpy as np

def generate_counts(num_plants, mean_val):
    total_sum = num_plants * mean_val
    
    # Generate random numbers
    random_vals = np.random.random(num_plants)
    # Scale them so they sum to the total_sum
    scaled_vals = (random_vals / random_vals.sum()) * total_sum
    
    # Round to whole numbers
    whole_numbers = np.round(scaled_vals).astype(int)
    
    # Adjust for rounding errors to ensure the sum is exact
    difference = total_sum - whole_numbers.sum()
    for i in range(abs(int(difference))):
        whole_numbers[i % num_plants] += 1 if difference > 0 else -1
        
    return whole_numbers

# Streamlit UI
st.title("🌱 Plant Insect Count Generator")
st.write("Generate whole number insect counts based on a target mean.")

col1, col2 = st.columns(2)

with col1:
    plants = st.number_input("Number of Plants", min_value=1, value=25, step=1)

with col2:
    mean_target = st.number_input("Target Mean Value", min_value=0, value=10, step=1)

if st.button("Generate Data"):
    results = generate_counts(plants, mean_target)
    
    st.success(f"Generated counts for {plants} plants with a mean of {mean_target}")
    
    # Display results in a grid or table
    st.table({"Plant ID": range(1, plants + 1), "Insect Count": results})
    
    # Show statistics
    st.info(f"**Total Insects:** {results.sum()}  |  **Actual Mean:** {results.mean():.2f}")