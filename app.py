import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Gold Loan Analytics Dashboard", layout="wide")

st.markdown("""
<style>

.main {
    background-color: #F4F6FB;
}

h1, h2, h3 {
    color: #1E4FA1;
}

/* KPI LABEL TEXT */
[data-testid="stMetricLabel"] {
    color: #333333 !important;
    font-weight: 600;
}

/* KPI VALUE */
[data-testid="stMetricValue"] {
    color: #E53935 !important;
}

/* KPI CARD STYLE */
[data-testid="stMetric"] {
    background-color: #F5F5F5;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #1E4FA1;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

px.defaults.template = "plotly_dark"

st.title("Gold Loan Data Analytics Dashboard")
# -----------------------------
# DATA LOADING FUNCTIONS
# -----------------------------

@st.cache_data
def load_loan_data():

    df = pd.read_excel("JAN-FEB Disbursement Data.xlsx")

    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.upper()

    return df


@st.cache_data
def load_branch_data():

    df = pd.read_excel("Branch_Level_Performance_Updated.xlsx")

    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.upper()

    return df


@st.cache_data
def load_cluster_data():

    df = pd.read_excel("Branch_Clusters.xlsx")

    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.upper()

    return df


# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

page = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Project Overview",
        "Loan Level Dashboard",
        "Branch Level Dashboard",
        "Cluster Analysis Dashboard"
    ]
)

# -----------------------------
# PROJECT OVERVIEW
# -----------------------------

if page == "Project Overview":

    st.header("Project Overview")

    st.markdown("""
### Gold Loan Data Analytics Platform

This analytics platform evaluates the performance of gold loan branches across multiple states using advanced data analytics and machine learning.

The objective of this project is to generate insights into operational performance and identify strategic improvement opportunities.
""")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
### Loan Analytics

Analyze loan disbursement patterns across branches, schemes, and states.
""")

    with col2:
        st.success("""
### Branch Performance

Evaluate operational efficiency using performance metrics such as ROI, LTV and disbursement volume.
""")

    with col3:
        st.warning("""
### Machine Learning Segmentation

Cluster branches into performance groups to identify high-performing and risk-heavy branches.
""")

    st.divider()

    st.subheader("Project Objectives")

    st.markdown("""
• Analyze loan disbursement distribution  
• Evaluate branch-level performance metrics  
• Identify high-performing and underperforming branches  
• Measure risk exposure using LTV ratios  
• Apply clustering techniques to segment branch performance
""")

    st.divider()

    st.subheader("Analytics Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Loan Records", "190K+")

    with col2:
        st.metric("Branches", "366")

    with col3:
        st.metric("States", "12")
# -----------------------------
# LOAN LEVEL DASHBOARD
# -----------------------------

elif page == "Loan Level Dashboard":

    st.header("Loan Level Disbursement Analysis")

    loan_df = load_loan_data()

    # -----------------------------
    # KPI CARDS
    # -----------------------------

    st.subheader("Key Loan Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    total_disbursement = loan_df["DISBURSED_AMOUNT"].sum()
    avg_disbursement = loan_df["DISBURSED_AMOUNT"].mean()

    branch_count = loan_df["BRANCH_NAME"].nunique()
    scheme_count = loan_df["SCHEME"].nunique()
    state_count = loan_df["ZONE"].nunique()

    col1.metric("Total Disbursement", f"₹{total_disbursement:,.0f}")
    col2.metric("Average Loan Size", f"₹{avg_disbursement:,.0f}")
    col3.metric("Branches", branch_count)
    col4.metric("Schemes", scheme_count)
    col5.metric("States", state_count)

    # -----------------------------
    # FULL DATASET
    # -----------------------------

    with st.expander("View Full Loan Dataset"):
        st.dataframe(loan_df, use_container_width=True)

    # -----------------------------
    # LOAN EXPLORER
    # -----------------------------

    st.subheader("Explore Loans by Scheme")

    selected_scheme = st.selectbox(
        "Select Scheme",
        loan_df["SCHEME"].unique()
    )

    filtered_data = loan_df[
        loan_df["SCHEME"] == selected_scheme
    ]

    st.dataframe(filtered_data, use_container_width=True)

    # -----------------------------
    # STATE LEVEL DISBURSEMENT
    # -----------------------------

    st.subheader("Top States by Disbursement")

    state_data = loan_df.groupby("ZONE")["DISBURSED_AMOUNT"].sum().reset_index()
    state_data = state_data.sort_values("DISBURSED_AMOUNT", ascending=False)

    fig = px.bar(
        state_data,
        x="DISBURSED_AMOUNT",
        y="ZONE",
        orientation="h",
        color="DISBURSED_AMOUNT",
        text="DISBURSED_AMOUNT",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        xaxis_title="Total Disbursement",
        yaxis_title="State",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # SCHEME DISTRIBUTION
    # -----------------------------

    st.subheader("Disbursement by Scheme")

    scheme_data = loan_df.groupby("SCHEME")["DISBURSED_AMOUNT"].sum().reset_index()

    fig = px.pie(
        scheme_data,
        names="SCHEME",
        values="DISBURSED_AMOUNT",
        hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # LOAN ACTIVITY BY SCHEME
    # -----------------------------

    st.subheader("Number of Loans by Scheme")

    scheme_loans = loan_df.groupby("SCHEME").size().reset_index(name="Loan_Count")

    fig = px.bar(
        scheme_loans,
        x="SCHEME",
        y="Loan_Count",
        color="SCHEME",
        text="Loan_Count"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True, key="scheme_loan_chart")

    # -----------------------------
    # STATE CONTRIBUTION TREEMAP
    # -----------------------------

    st.subheader("State Contribution to Total Disbursement")

    state_tree = loan_df.groupby("ZONE")["DISBURSED_AMOUNT"].sum().reset_index()

    fig = px.treemap(
        state_tree,
        path=["ZONE"],
        values="DISBURSED_AMOUNT",
        color="DISBURSED_AMOUNT",
        color_continuous_scale="Teal"
    )

    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # STATE VS SCHEME ACTIVITY
    # -----------------------------

    st.subheader("Loan Distribution by State and Scheme")

    state_scheme = loan_df.groupby(["ZONE", "SCHEME"]).size().reset_index(name="Loan_Count")

    fig = px.bar(
        state_scheme,
        x="ZONE",
        y="Loan_Count",
        color="SCHEME",
        barmode="stack"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # AVERAGE LOAN SIZE BY SCHEME
    # -----------------------------

    st.subheader("Average Loan Size by Scheme")

    scheme_avg = loan_df.groupby("SCHEME")["DISBURSED_AMOUNT"].mean().reset_index()

    fig = px.bar(
        scheme_avg,
        x="DISBURSED_AMOUNT",
        y="SCHEME",
        orientation="h",
        text="DISBURSED_AMOUNT",
        color="DISBURSED_AMOUNT",
        color_continuous_scale="Teal"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

   
    # -----------------------------
    # TOP BRANCHES BY LOAN COUNT
    # -----------------------------

    st.subheader("Top Branches by Loan Count")

    loan_count_top = branch_df.sort_values(
        "LOAN_COUNT",
        ascending=False
    ).head(15)

    fig = px.bar(
        loan_count_top,
        x="LOAN_COUNT",
        y="BRANCH_NAME",
        orientation="h",
        text="LOAN_COUNT",
        color="LOAN_COUNT",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)


    # -----------------------------
    # ROI DISTRIBUTION
    # -----------------------------

    st.subheader("ROI Distribution Across Branches")

    fig = px.histogram(
        branch_df,
        x="AVG_ROI",
        nbins=25,
        color_discrete_sequence=["#00C49F"]
    )

    fig.update_layout(
        xaxis_title="Average ROI",
        yaxis_title="Number of Branches",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)


    # -----------------------------
    # LTV DISTRIBUTION
    # -----------------------------

    st.subheader("LTV Distribution Across Branches")

    fig = px.histogram(
        branch_df,
        x="AVG_LTV",
        nbins=25,
        color_discrete_sequence=["#FFA15A"]
    )

    fig.update_layout(
        xaxis_title="Average LTV",
        yaxis_title="Number of Branches",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)


    # -----------------------------
    # GOLD WEIGHT VS DISBURSEMENT
    # -----------------------------

    st.subheader("Gold Weight vs Disbursement")

    fig = px.scatter(
        branch_df,
        x="AVG_GOLD_WEIGHT",
        y="TOTAL_DISBURSEMENT",
        size="LOAN_COUNT",
        color="AVG_ROI",
        hover_name="BRANCH_NAME",
        color_continuous_scale="Turbo"
    )

    fig.update_layout(
        xaxis_title="Average Gold Weight",
        yaxis_title="Total Disbursement",
        height=550
    )

    st.plotly_chart(fig, use_container_width=True)


    # -----------------------------
    # LOAN COUNT VS ROI
    # -----------------------------

    st.subheader("Loan Count vs Profitability")

    fig = px.scatter(
        branch_df,
        x="LOAN_COUNT",
        y="AVG_ROI",
        size="TOTAL_DISBURSEMENT",
        color="AVG_LTV",
        hover_name="BRANCH_NAME",
        color_continuous_scale="Plasma"
    )

    fig.update_layout(
        xaxis_title="Loan Count",
        yaxis_title="Average ROI",
        height=550
    )

    st.plotly_chart(fig, use_container_width=True)


    # -----------------------------
    # TOP BRANCHES BY ROI
    # -----------------------------

    st.subheader("Top Branches by ROI")

    roi_top = branch_df.sort_values(
        "AVG_ROI",
        ascending=False
    ).head(10)

    fig = px.bar(
        roi_top,
        x="AVG_ROI",
        y="BRANCH_NAME",
        orientation="h",
        text="AVG_ROI",
        color="AVG_ROI",
        color_continuous_scale="Greens"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)


    # -----------------------------
    # CORRELATION HEATMAP
    # -----------------------------

    st.subheader("Branch Performance Correlation")

    corr = branch_df[
        ["TOTAL_DISBURSEMENT","AVG_LTV","AVG_ROI","LOAN_COUNT","AVG_GOLD_WEIGHT"]
    ].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Blues"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# BRANCH LEVEL DASHBOARD
# -----------------------------

elif page == "Branch Level Dashboard":

    st.header("Branch Performance Analysis")

    branch_df = load_branch_data()

    # -----------------------------
    # KPI CARDS
    # -----------------------------

    st.subheader("Branch Performance Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    total_disbursement = branch_df["TOTAL_DISBURSEMENT"].sum()
    avg_ltv = branch_df["AVG_LTV"].mean()
    avg_roi = branch_df["AVG_ROI"].mean()
    branch_count = branch_df["BRANCH_CODE"].nunique()
    avg_gold_weight = branch_df["AVG_GOLD_WEIGHT"].mean()

    col1.metric("Total Disbursement", f"₹{total_disbursement:,.0f}")
    col2.metric("Average LTV", f"{avg_ltv:.2f}")
    col3.metric("Average ROI", f"{avg_roi:.2f}")
    col4.metric("Branches", branch_count)
    col5.metric("Average Gold Weight", f"{avg_gold_weight:.2f}")

    # -----------------------------
    # BEST / WORST BRANCH
    # -----------------------------

    col6, col7 = st.columns(2)

    top_branch = branch_df.loc[
        branch_df["TOTAL_DISBURSEMENT"].idxmax(),
        "BRANCH_NAME"
    ]

    low_branch = branch_df.loc[
        branch_df["TOTAL_DISBURSEMENT"].idxmin(),
        "BRANCH_NAME"
    ]

    col6.metric("Highest Performing Branch", top_branch)
    col7.metric("Lowest Performing Branch", low_branch)


    # -----------------------------
    # DATASET EXPLORER
    # -----------------------------

    st.subheader("Dataset Explorer")

    selected_columns = st.multiselect(
        "Select columns to view",
        branch_df.columns,
        default=list(branch_df.columns)
    )

    st.dataframe(branch_df[selected_columns], use_container_width=True)

    # -----------------------------
    # SEARCH BRANCH
    # -----------------------------

    st.subheader("Search Branch")

    branch_search = st.selectbox(
        "Select Branch",
        branch_df["BRANCH_NAME"].unique()
    )

    filtered_branch = branch_df[
        branch_df["BRANCH_NAME"] == branch_search
    ]

    st.dataframe(filtered_branch, use_container_width=True)

    # -----------------------------
    # TOP 10 BRANCHES BY DISBURSEMENT
    # -----------------------------

    st.subheader("Top 10 Branches by Disbursement")

    top10 = branch_df.sort_values(
        "TOTAL_DISBURSEMENT",
        ascending=False
    ).head(10)

    fig = px.bar(
        top10,
        x="TOTAL_DISBURSEMENT",
        y="BRANCH_NAME",
        orientation="h",
        text="TOTAL_DISBURSEMENT",
        color="TOTAL_DISBURSEMENT",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # RISK VS PERFORMANCE
    # -----------------------------

    st.subheader("Branch Risk vs Performance")

    fig = px.scatter(
        branch_df,
        x="AVG_LTV",
        y="TOTAL_DISBURSEMENT",
        size="LOAN_COUNT",
        color="AVG_ROI",
        hover_name="BRANCH_NAME",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)

 
    # =====================================================
    # NEW VISUALIZATIONS
    # =====================================================

    # -----------------------------
    # TOP BRANCHES BY LOAN COUNT
    # -----------------------------

    st.subheader("Top Branches by Loan Count")

    loan_count_top = branch_df.sort_values(
        "LOAN_COUNT",
        ascending=False
    ).head(15)

    fig = px.bar(
        loan_count_top,
        x="LOAN_COUNT",
        y="BRANCH_NAME",
        orientation="h",
        color="LOAN_COUNT",
        text="LOAN_COUNT",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # ROI DISTRIBUTION
    # -----------------------------

    st.subheader("ROI Distribution Across Branches")

    fig = px.histogram(
        branch_df,
        x="AVG_ROI",
        nbins=25,
        color_discrete_sequence=["#00C49F"]
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # LTV DISTRIBUTION
    # -----------------------------

    st.subheader("LTV Distribution Across Branches")

    fig = px.histogram(
        branch_df,
        x="AVG_LTV",
        nbins=25,
        color_discrete_sequence=["#FFA15A"]
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # GOLD WEIGHT VS DISBURSEMENT
    # -----------------------------

    st.subheader("Gold Weight vs Disbursement")

    fig = px.scatter(
        branch_df,
        x="AVG_GOLD_WEIGHT",
        y="TOTAL_DISBURSEMENT",
        size="LOAN_COUNT",
        color="AVG_ROI",
        hover_name="BRANCH_NAME",
        color_continuous_scale="Turbo"
    )

    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # LOAN COUNT VS ROI
    # -----------------------------

    st.subheader("Loan Count vs ROI")

    fig = px.scatter(
        branch_df,
        x="LOAN_COUNT",
        y="AVG_ROI",
        size="TOTAL_DISBURSEMENT",
        color="AVG_LTV",
        hover_name="BRANCH_NAME",
        color_continuous_scale="Plasma"
    )

    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # TOP BRANCHES BY ROI
    # -----------------------------

    st.subheader("Top Branches by ROI")

    roi_top = branch_df.sort_values(
        "AVG_ROI",
        ascending=False
    ).head(10)

    fig = px.bar(
        roi_top,
        x="AVG_ROI",
        y="BRANCH_NAME",
        orientation="h",
        text="AVG_ROI",
        color="AVG_ROI",
        color_continuous_scale="Greens"
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

  
# -----------------------------
# CLUSTER ANALYSIS DASHBOARD
# -----------------------------

elif page == "Cluster Analysis Dashboard":

    st.header("Branch Segmentation using Machine Learning")

    # -----------------------------
    # LOAD CLUSTER DATA
    # -----------------------------

    file_path = "Branch_Clusters.xlsx"

    cluster0 = pd.read_excel(file_path, sheet_name=0)
    cluster1 = pd.read_excel(file_path, sheet_name=1)
    cluster2 = pd.read_excel(file_path, sheet_name=2)
    cluster3 = pd.read_excel(file_path, sheet_name=3)

    cluster0["Cluster"] = 0
    cluster1["Cluster"] = 1
    cluster2["Cluster"] = 2
    cluster3["Cluster"] = 3

    cluster_df = pd.concat([cluster0, cluster1, cluster2, cluster3])

    # -----------------------------
    # RENAME CLUSTERS
    # -----------------------------

    cluster_df["Cluster_Name"] = cluster_df["Cluster"].map({
        0: "High Performance - Low Risk",
        1: "High Performance - High Risk",
        2: "Stable Branches",
        3: "Underperforming Branches"
    })

    # -----------------------------
    # KPI CARDS
    # -----------------------------

    st.subheader("Cluster Overview")

    col1, col2, col3, col4 = st.columns(4)

    total_clusters = cluster_df["Cluster_Name"].nunique()
    total_branches = len(cluster_df)

    largest_segment = cluster_df["Cluster_Name"].value_counts().idxmax()
    smallest_segment = cluster_df["Cluster_Name"].value_counts().idxmin()

    col1.metric("Clusters Created", total_clusters)
    col2.metric("Branches Segmented", total_branches)
    col3.metric("Largest Segment", largest_segment)
    col4.metric("Smallest Segment", smallest_segment)

    # -----------------------------
    # CLUSTER MEANING (IMPORTANT FOR VIEWERS)
    # -----------------------------

    st.subheader("Segment Meaning")

    st.markdown("""
    **Cluster Segments Explained**

    • **High Performance - Low Risk** → Branches with strong disbursement and safe lending levels  
    • **High Performance - High Risk** → High volume branches but with higher LTV risk  
    • **Stable Branches** → Moderate volume and controlled risk levels  
    • **Underperforming Branches** → Low disbursement and weaker performance
    """)

    # -----------------------------
    # SEGMENT EXPLORER
    # -----------------------------

    st.subheader("Explore Branches by Segment")

    selected_cluster = st.selectbox(
        "Select Segment",
        cluster_df["Cluster_Name"].unique()
    )

    filtered_cluster = cluster_df[
        cluster_df["Cluster_Name"] == selected_cluster
    ]

    st.dataframe(filtered_cluster, use_container_width=True)

    # -----------------------------
    # CLUSTER DISTRIBUTION
    # -----------------------------

    st.subheader("Branch Distribution Across Segments")

    cluster_counts = cluster_df["Cluster_Name"].value_counts().reset_index()
    cluster_counts.columns = ["Segment", "Branches"]

    fig = px.pie(
        cluster_counts,
        names="Segment",
        values="Branches",
        color="Segment",
        hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # RISK VS PERFORMANCE MAP
    # -----------------------------

    st.subheader("Branch Risk vs Performance Segmentation")

    fig = px.scatter(
        cluster_df,
        x="AVG_LTV",
        y="TOTAL_DISBURSEMENT",
        color="Cluster_Name",
        size="LOAN_COUNT",
        hover_name="BRANCH_NAME"
    )

    fig.update_layout(
        xaxis_title="Average LTV (Risk Level)",
        yaxis_title="Total Disbursement (Business Volume)",
        height=550
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # CLUSTER PERFORMANCE COMPARISON
    # -----------------------------

    st.subheader("Average Business Volume by Segment")

    cluster_perf = cluster_df.groupby("Cluster_Name").agg({
        "TOTAL_DISBURSEMENT":"mean",
        "AVG_LTV":"mean",
        "AVG_ROI":"mean",
        "LOAN_COUNT":"mean"
    }).reset_index()

    fig = px.bar(
        cluster_perf,
        x="Cluster_Name",
        y="TOTAL_DISBURSEMENT",
        color="Cluster_Name",
        text="TOTAL_DISBURSEMENT",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_layout(
        xaxis_title="Branch Segment",
        yaxis_title="Average Disbursement",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
 # -----------------------------
    # ROI COMPARISON (IMPROVED)
    # -----------------------------

    st.subheader("Average Profitability by Segment")

    fig = px.bar(
        cluster_perf.sort_values("AVG_ROI"),
        x="AVG_ROI",
        y="Cluster_Name",
        orientation="h",
        color="Cluster_Name",
        text="AVG_ROI",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig.update_layout(
        xaxis_title="Average ROI",
        yaxis_title="Segment",
        height=500
    )

    fig.update_traces(
        texttemplate='%{text:.2f}',
        textposition='outside'
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # RISK LEVEL COMPARISON
    # -----------------------------

    st.subheader("Average Risk Level by Segment")

    fig = px.bar(
        cluster_perf,
        x="Cluster_Name",
        y="AVG_LTV",
        color="Cluster_Name",
        text="AVG_LTV"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

   