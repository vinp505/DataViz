import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Add a title and some text
st.title("My Interactive Wave App")
st.write("Adjust the slider to change the frequency of the wave.")

# 2. Add an interactive slider widget
frequency = st.slider("Frequency", min_value=1.0, max_value=10.0, value=2.0)

# 3. Generate data based on the slider's value
x = np.linspace(0, 10, 500)
y = np.sin(x * frequency)

# 4. Draw the Matplotlib figure
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y, color="#4A9090", linewidth=2) # Using our warm teal color
ax.set_facecolor("#FAF9F6")                  # Using our off-white paper background
fig.patch.set_facecolor("#FAF9F6")

# 5. Display the plot in the web app
st.pyplot(fig)