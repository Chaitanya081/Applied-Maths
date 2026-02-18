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
# Helper: build sequences
# -------------------------
def build_sequence(N, pattern):
    n = np.arange(N)
    if pattern == "Constant (x[n]=1)":
        x = np.ones(N)
    else:
        # Pulse/Periodic pattern: 1 every 3 steps -> 1,0,0,1,0,0,...
        x = np.zeros(N)
        x[::3] = 1
    return n, x

# -------------------------
# Introduction
# -------------------------
if choice == "Introduction":
    st.header("Introduction")
    st.write("""
    This app models delivery schedules as discrete-time sequences and shows how delays affect them.
    You can view a regular (on-time) schedule and a delayed schedule, and visualize the effect of delay.
    """)

# -------------------------
# Regular Delivery Model
# -------------------------
elif choice == "Regular Delivery Model":
    st.header("Model 1: Regular (Periodic) Delivery Scheduling")

    N = st.slider("Select number of time steps (N)", 10, 100, 30)
    pattern = st.selectbox("Select pattern type", ["Constant (x[n]=1)", "Pulse / Periodic (1,0,0,...)"])

    n, x = build_sequence(N, pattern)

    if pattern == "Constant (x[n]=1)":
        st.write("Discrete-time sequence: x[n] = 1 (constant delivery each time step)")
    else:
        st.write("Discrete-time sequence: Pulse/Periodic (delivery occurs at some time steps)")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.step(n, x, where="mid", label="x[n] (Original)", linewidth=2)
    ax.scatter(n, x)
    ax.set_xlabel("n (time steps)")
    ax.set_ylabel("Deliveries")
    ax.set_title("Regular Delivery Sequence")
    ax.set_ylim(-0.2, 1.2)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    st.pyplot(fig)

    st.latex(r"X(z) = \sum_{n=0}^{\infty} x[n] z^{-n}")
    st.write("Interpretation: This shows the planned (on-time) delivery schedule.")

# -------------------------
# Delayed Delivery Model
# -------------------------
elif choice == "Delayed Delivery Model":
    st.header("Model 2: Delayed Delivery Scheduling")

    N = st.slider("Select number of time steps (N)", 10, 100, 30)
    k = st.slider("Select delay k", 0, 20, 3)
    pattern = st.selectbox("Select pattern type", ["Constant (x[n]=1)", "Pulse / Periodic (1,0,0,...)"])

    n, x = build_sequence(N, pattern)

    # Build delayed sequence y[n] = x[n-k]
    y = np.zeros(N)
    if k < N:
        y[k:] = x[:N-k]

    st.write(f"Delayed sequence: y[n] = x[n - {k}]")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.step(n, x, where="mid", label="x[n] (Original)", linewidth=2)
    ax.scatter(n, x)

    ax.step(n, y, where="mid", label="y[n] (Delayed)", linewidth=2)
    ax.scatter(n, y)

    ax.set_xlabel("n (time steps)")
    ax.set_ylabel("Deliveries")
    ax.set_title("Original vs Delayed Delivery Sequence")
    ax.set_ylim(-0.2, 1.2)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    st.pyplot(fig)

    st.latex(r"Y(z) = z^{-k} X(z)")
    st.write("Interpretation: Delay shifts the schedule in time by k steps without changing its shape.")

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
            N = min(len(data), 200)
            x = data[:N]

            y = np.zeros(N)
            if k < N:
                y[k:] = x[:N-k]

            n = np.arange(N)

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(n, x, label="Original Sequence", linewidth=2)
            ax.plot(n, y, label="Delayed Sequence", linewidth=2)
            ax.set_xlabel("n (time steps)")
            ax.set_ylabel(col)
            ax.set_title("Original vs Delayed Real Data Sequence")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend()
            st.pyplot(fig)

            st.write("This shows how real delivery-related data behaves under delay.")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.write("Developed for Applied Mathematics Project: Delivery Scheduling Analysis Using Z-Transforms")
