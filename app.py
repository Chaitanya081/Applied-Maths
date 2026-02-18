import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Delivery Scheduling using Z-Transforms", layout="wide")

st.title("🚚 Delivery Scheduling Analysis Using Z-Transforms")
st.write("A web application to analyze regular and delayed delivery schedules using discrete-time models.")

menu = ["Introduction", "Regular Delivery Model", "Delayed Delivery Model", "Real Data Demo"]
choice = st.sidebar.selectbox("Select Section", menu)

# -------------------------
# Introduction
# -------------------------
if choice == "Introduction":
    st.header("Introduction")
    st.write("""
    Efficient delivery scheduling is important in modern logistics.  
    Delivery processes occur in step-by-step discrete stages.  
    Z-Transforms are effective tools for analyzing such discrete-time systems.
    
    This web app demonstrates:
    - Regular (Periodic) Delivery Scheduling Model
    - Delayed Delivery Scheduling Model
    - Effect of delay using Z-Transform concept
    """)

# -------------------------
# Regular Delivery Model
# -------------------------
elif choice == "Regular Delivery Model":
    st.header("Model 1: Regular (Periodic) Delivery Scheduling")

    N = st.slider("Select number of time steps (N)", 10, 100, 20)
    n = np.arange(N)
    x = np.ones(N)

    st.write("Discrete-time sequence: x[n] = 1 (constant delivery each time step)")

    fig, ax = plt.subplots()
    ax.stem(n, x, use_line_collection=True)
    ax.set_xlabel("n (time steps)")
    ax.set_ylabel("x[n] (deliveries)")
    ax.set_title("Regular Delivery Sequence")
    st.pyplot(fig)

    st.latex(r"X(z) = \sum_{n=0}^{\infty} x[n] z^{-n}")
    st.write("Interpretation: The system is stable and represents planned, periodic delivery schedules.")

# -------------------------
# Delayed Delivery Model
# -------------------------
elif choice == "Delayed Delivery Model":
    st.header("Model 2: Delayed Delivery Scheduling")

    N = st.slider("Select number of time steps (N)", 10, 100, 20)
    k = st.slider("Select delay k", 0, 20, 3)

    n = np.arange(N)
    x = np.ones(N)

    y = np.zeros(N)
    if k < N:
        y[k:] = x[:N-k]

    st.write(f"Delayed sequence: y[n] = x[n - {k}]")

    fig, ax = plt.subplots()
    ax.stem(n, x, linefmt='b-', markerfmt='bo', basefmt=" ", label="Original x[n]", use_line_collection=True)
    ax.stem(n, y, linefmt='r-', markerfmt='ro', basefmt=" ", label="Delayed y[n]", use_line_collection=True)
    ax.set_xlabel("n (time steps)")
    ax.set_ylabel("Deliveries")
    ax.set_title("Original vs Delayed Delivery Sequence")
    ax.legend()
    st.pyplot(fig)

    st.latex(r"Y(z) = z^{-k} X(z)")
    st.write("Interpretation: z^{-k} represents delay. Larger k means more delivery delay.")

# -------------------------
# Real Data Demo
# -------------------------
elif choice == "Real Data Demo":
    st.header("Real Data Demonstration")

    uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Dataset Preview:")
        st.dataframe(df.head())

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) == 0:
            st.warning("No numeric columns found in dataset.")
        else:
            col = st.selectbox("Select a numeric column as sequence", numeric_cols)
            k = st.slider("Select delay k", 0, 50, 5)

            data = df[col].values
            N = min(len(data), 200)  # limit for display
            x = data[:N]

            y = np.zeros(N)
            if k < N:
                y[k:] = x[:N-k]

            n = np.arange(N)

            fig, ax = plt.subplots()
            ax.plot(n, x, label="Original Sequence")
            ax.plot(n, y, label="Delayed Sequence")
            ax.set_xlabel("n (time steps)")
            ax.set_ylabel(col)
            ax.set_title("Original vs Delayed Real Data Sequence")
            ax.legend()
            st.pyplot(fig)

            st.write("This shows how real delivery-related data behaves under delay.")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.write("Developed for Applied Mathematics Project: Delivery Scheduling Analysis Using Z-Transforms")
