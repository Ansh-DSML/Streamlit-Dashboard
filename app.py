import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Churn Prediction Dashboard", layout="wide", page_icon="📊")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Customer_Data.csv")

df = load_data()

# Choose dashboard view
option = st.selectbox(
    "Choose Dashboard View",
    ["Select Option", "View Raw Data Dashboard", "View Predicted Churn Customers Dashboard"],
    index=0
)

# ========== DARK MODE LANDING PAGE ==========
if option == "Select Option":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #2c2c2c;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("👋 Welcome to the Churn Prediction Dashboard")
    st.markdown("Please select an option above to get started.")

# ========== RAW DATA DASHBOARD ==========
elif option == "View Raw Data Dashboard":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #efebe0;
        }
        .big-font {
            font-size: 40px !important;
            color: #b19079;
        }
        .kpi {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }
        .kpi p {
            color: #4b3f36;
            margin-top: 5px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📊 Raw Data KPI Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="kpi"><div class="big-font">6,418</div><p>Total Customers</p></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kpi"><div class="big-font">411</div><p>New Joiners</p></div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="kpi"><div class="big-font">1,732</div><p>Total Churn</p></div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="kpi"><div class="big-font">27.0%</div><p>Churn Rate</p></div>', unsafe_allow_html=True)

    # ========== BAR CHART: Customers vs Churn by Tenure ==========
    st.markdown("### 📉 Total Customers and Total Churn by Tenure Group")

    # Static chart data
    tenure_groups = ["< 6 Months", "6–12 Months", "12–18 Months", "18–24 Months", ">= 24 Months"]
    total_customers = [1.1, 1.3, 1.0, 1.0, 2.1]
    total_churn = [0.3, 0.4, 0.3, 0.3, 0.6]

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    x = range(len(tenure_groups))

    ax.bar(x, total_customers, width=bar_width, label='Total Customers', color='#b19079')
    ax.bar([i + bar_width for i in x], total_churn, width=bar_width, label='Total Churn', color='#b7c6b1')

    ax.set_xlabel('Tenure Group')
    ax.set_ylabel('Count (in K)')
    ax.set_title('Total Customers and Total Churn by Tenure Group')
    ax.set_xticks([i + bar_width / 2 for i in x])
    ax.set_xticklabels(tenure_groups)
    ax.legend()

    st.pyplot(fig)
   
   # ========== BAR + LINE CHART: Customers and Churn Rate by Age Group ==========
    st.markdown("### 👥 Total Customers and Churn Rate by Age Group")

    # Extracted values from image
    age_groups = ["< 20", "20–35", "35–50", "> 50"]
    total_customers_age = [0.1, 1.8, 1.8, 2.7]
    churn_rates = [23.08, 23.57, 23.68, 31.55]

    fig2, ax1 = plt.subplots(figsize=(10, 6))

    bar_width = 0.5
    x = range(len(age_groups))

    # Plotting the bar chart for Total Customers
    bars = ax1.bar(x, total_customers_age, bar_width, color="#b19079", label='Total Customers')
    ax1.set_xlabel('Age Group')
    ax1.set_ylabel('Total Customers (in K)', color="#b19079")
    ax1.tick_params(axis='y', labelcolor="#b19079")
    ax1.set_xticks(x)
    ax1.set_xticklabels(age_groups)
    
    # Adding value labels on top of bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, height + 0.05, f"{height:.1f}K\n{churn_rates[i]:.2f}%", ha='center', fontsize=9, color="#4b3f36")

    # Secondary y-axis for Churn Rate
    ax2 = ax1.twinx()
    ax2.plot(x, churn_rates, color='black', marker='o', linewidth=2, label='Churn Rate')
    ax2.set_ylabel('Churn Rate (%)', color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    ax2.set_ylim(20, 40)

    # Legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    st.pyplot(fig2)

    states = ["Jammu & K...", "Assam", "Jharkhand", "Chhattisgarh","Delhi"]
    churn_rates = [57.19, 38.13, 34.51, 30.51, 29.92]

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(states, churn_rates, color="#c4a489", edgecolor='black')

    # Add value labels on bars
    for bar in bars:
     width = bar.get_width()
     ax.text(width + 1, bar.get_y() + bar.get_height()/2,
            f'{width:.2f}%', va='center', ha='left', fontsize=9)

     # Title and labels
    ax.set_title("Churn Rate by State (Top 5)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Churn Rate")
    ax.set_ylabel("State")

     # Style tweaks
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlim(0, 60)
    plt.tight_layout()

     # Display in Streamlit
    st.pyplot(fig)

    categories = ["Compensation", "Attitude", "Dissatisfaction", "Price", "Other"]
    total_churn = [761, 301, 300, 196, 174]

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.barh(categories, total_churn, color="#c4a489", edgecolor='black')

    # Add value labels on bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 5, bar.get_y() + bar.get_height()/2,
                f'{int(width)}', va='center', ha='left', fontsize=9)

    # Title and labels
    ax.set_title("Total Churn by Churn Category", fontsize=14, fontweight='bold')
    ax.set_xlabel("Total Churn")
    ax.set_ylabel("Churn Category")

    # Style tweaks
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlim(0, 800)
    plt.tight_layout()

    # Display in Streamlit
    st.pyplot(fig)

    internet_types = ["None", "DSL", "Cable", "Fiber Optic"]
    churn_rates = [7.84, 19.37, 25.72, 41.10]

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.barh(internet_types, churn_rates, color="#c4a489", edgecolor='black')

    # Add value labels on bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                f'{width:.2f}%', va='center', ha='left', fontsize=9)

    # Title and labels
    ax.set_title("Churn Rate by Internet Type", fontsize=14, fontweight='bold')
    ax.set_xlabel("Churn Rate")
    ax.set_ylabel("Internet Type")

    # Style tweaks
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlim(0, 45)
    plt.tight_layout()

    # Display in Streamlit
    st.pyplot(fig)

    payment_methods = ["Credit Card", "Bank Withdraw", "Mailed to Address"]
    churn_rates = [14.80, 34.43, 37.82]

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.barh(payment_methods, churn_rates, color="#c4a489", edgecolor='black')

    # Add value labels on bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                f'{width:.2f}%', va='center', ha='left', fontsize=9)

    # Title and labels
    ax.set_title("Churn Rate by Payment Method", fontsize=14, fontweight='bold')
    ax.set_xlabel("Churn Rate")
    ax.set_ylabel("Payment Method")

    # Style tweaks
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlim(0, 45)
    plt.tight_layout()

    # Display in Streamlit
    st.pyplot(fig)

# ========== PREDICTED CHURN PLACEHOLDER ==========
elif option == "View Predicted Churn Customers Dashboard":
    st.subheader("🧠 Predicted Churn Customers")
    st.info("This section will show predictions based on ML models.")

    st.markdown("### 💳 Customer Count by Payment Method (Predicted)")

    # Static data extracted from image
    payment_methods = ["Credit Card", "Bank Withdrawal", "Mailed Check"]
    customer_counts = [190, 150, 40]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(payment_methods, customer_counts, color="#40a4ff", edgecolor='black')

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 5, f'{height}', ha='center', fontsize=9)

    ax.set_title("# by Payment Method", fontsize=14, fontweight='bold')
    ax.set_ylabel("Count of Customer_ID")
    ax.set_xlabel("Payment_Method")

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    st.pyplot(fig)
