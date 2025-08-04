import streamlit as st

st.set_page_config(
    page_title="ROI Calculator for Remote Contrast Supervision",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("ROI Calculator")
st.markdown("Estimate cost savings and margin improvement for transitioning to remote contrast supervision.")

# --- INPUTS ---

st.subheader("Input Variables")

monthly_volume = st.slider(
    "Monthly Contrast Scan Volume",
    min_value=0,
    max_value=1000,
    value=250,
    step=10,
    help="Total contrast MRI/CT scans per month across all facilities."
)

md_comp_type = st.radio(
    "In-House Supervising MD Compensation Type",
    options=["Hourly Rate", "Annual Salary"],
    help="Choose how you pay supervising MDs."
)

if md_comp_type == "Hourly Rate":
    md_comp_hourly = st.number_input(
        "MD Hourly Rate ($/hr)", min_value=50, max_value=2000, value=200, step=10
    )
    md_comp_annual = None
else:
    md_comp_annual = st.number_input(
        "MD Annual Salary ($/yr)", min_value=100000, max_value=2000000, value=400000, step=10000
    )
    md_comp_hourly = None

per_diem = st.number_input(
    "Per Diem / Emergency / Locums Coverage Cost ($/shift)", min_value=0, max_value=5000, value=1800, step=100,
    help="Average temp coverage shift cost."
)

col1, col2 = st.columns(2)
with col1:
    weekday_start = st.text_input("Weekday Coverage Start", value="8:00 AM")
with col2:
    weekday_end = st.text_input("Weekday Coverage End", value="5:00 PM")

weekend_coverage = st.toggle("Weekend Coverage?", value=False)
if weekend_coverage:
    col3, col4 = st.columns(2)
    with col3:
        weekend_start = st.text_input("Weekend Coverage Start", value="8:00 AM")
    with col4:
        weekend_end = st.text_input("Weekend Coverage End", value="12:00 PM")
else:
    weekend_start = None
    weekend_end = None

after_hours = st.toggle("Evening / After-Hours Scanning (Post-5 PM)?", value=False)

avg_per_day = st.number_input(
    "Average # of Contrast Exams Per Day (Optional Override)", min_value=0, max_value=500, value=0, step=1,
    help="Optional. If set, overrides monthly volume."
)

avg_reimb = st.number_input(
    "Average Reimbursement per Scan (Optional)", min_value=0, max_value=10000, value=0, step=10,
    help="Used to estimate added revenue."
)

downtime = st.number_input(
    "Scanner Downtime % (Optional)", min_value=0.0, max_value=100.0, value=0.0, step=0.1,
    help="Operating hours lost due to lack of MD supervision."
)

num_centers = st.number_input(
    "# of Imaging Centers Needing Coverage", min_value=1, max_value=100, value=1, step=1
)

coverage_plan = st.selectbox(
    "Desired Coverage Plan",
    options=["Hourly", "Daily", "Monthly", "Annual"],
    index=0
)

# --- CALCULATIONS ---

# Helper to convert times like "8:00 AM" to float hours
import re

def parse_time(t):
    match = re.match(r"(\d{1,2}):?(\d{0,2})\s*([AP]M)", t.strip(), re.I)
    if not match:
        return 0
    h, m, ampm = match.groups()
    h = int(h)
    m = int(m or 0)
    if ampm.upper() == "PM" and h != 12:
        h += 12
    if ampm.upper() == "AM" and h == 12:
        h = 0
    return h + m/60

weekday_hours = (parse_time(weekday_end) - parse_time(weekday_start)) * 5
weekend_hours = 0
if weekend_coverage and weekend_start and weekend_end:
    weekend_hours = (parse_time(weekend_end) - parse_time(weekend_start)) * 2

total_weekly_hours = max(0, weekday_hours + weekend_hours)
total_centers = num_centers or 1

if avg_per_day > 0:
    scans_per_month = avg_per_day * 22 * total_centers
else:
    scans_per_month = monthly_volume * total_centers

annual_scans = scans_per_month * 12

# Plan pricing
plan_pricing = {
    "Hourly": 140,
    "Daily": 950,
    "Monthly": 18000,
    "Annual": 200000,
}

if md_comp_type == "Hourly Rate":
    md_annual_cost = md_comp_hourly * total_weekly_hours * 52 * total_centers
else:
    md_annual_cost = md_comp_annual * total_centers

if coverage_plan == "Hourly":
    plan_cost = plan_pricing["Hourly"] * total_weekly_hours * 52 * total_centers
elif coverage_plan == "Daily":
    plan_cost = plan_pricing["Daily"] * 5 * 52 * total_centers
elif coverage_plan == "Monthly":
    plan_cost = plan_pricing["Monthly"] * 12 * total_centers
elif coverage_plan == "Annual":
    plan_cost = plan_pricing["Annual"] * total_centers
else:
    plan_cost = 0

# Per-diem/locum cost: 4 weekends/month, 2 shifts/weekend
per_diem_shifts = 2 * 4 * total_centers if weekend_coverage else 0
locum_annual = per_diem * per_diem_shifts * 12

cost_savings = (md_annual_cost + locum_annual) - plan_cost

# FTEs saved (2080 hrs/FTE)
if md_comp_type == "Hourly Rate":
    single_fte_cost = md_comp_hourly * 2080
else:
    single_fte_cost = md_comp_annual

fte_saved = (md_annual_cost - plan_cost) / single_fte_cost if single_fte_cost else 0

# Added revenue (if after-hours or downtime, and reimbursement provided)
added_revenue = 0
if avg_reimb > 0 and (after_hours or downtime > 0):
    scan_increase = 0
    if after_hours:
        scan_increase += 0.08
    if downtime > 0:
        scan_increase += min(0.10, downtime/100)
    added_revenue = annual_scans * scan_increase * avg_reimb

total_margin = cost_savings + added_revenue
roi_pct = (total_margin / plan_cost * 100) if plan_cost > 0 else 0

plan_labels = {
    "Hourly": "hourly remote MD supervision plan",
    "Daily": "daily rate remote MD coverage",
    "Monthly": "monthly supervision contract",
    "Annual": "annual enterprise remote coverage",
}

# --- OUTPUTS ---

st.divider()
st.subheader("ROI Results")

col5, col6 = st.columns(2)
with col5:
    st.metric("Estimated Annual Cost Savings ($/year)", f"${cost_savings:,.0f}")
    st.metric("Potential Added Revenue ($/year)", f"${added_revenue:,.0f}")
with col6:
    st.metric("Reduction in Required MD FTEs", f"{fte_saved:,.2f}")
    st.metric("Total Margin Improvement ($/year)", f"${total_margin:,.0f}")

st.markdown(
    f"""
    <div style="margin-top:1.2em;padding:1.2em;border-radius:1em;background:rgba(0,80,255,0.09);font-size:1.15em;">
        <b>ROI %:</b> <span style="color:#2272fa;font-weight:700;font-size:1.5em;animation:pulse 2s infinite;">{roi_pct:,.1f}%</span>
        <br>
        Savings are calculated relative to your selected <b>{plan_labels.get(coverage_plan, coverage_plan.lower())}</b>.
    </div>
    """, unsafe_allow_html=True
)

# --- CTA & Disclaimer ---

st.markdown("---")
st.markdown("#### Want a custom ROI breakdown for your center?")
cta = st.button("Book Your ROI Call (Demo)", type="primary")
if cta:
    st.markdown("👉 [Contact us on Calendly](https://calendly.com/)")  # Replace with your real link

st.markdown(
    """
    <div style="margin-top:1em; color: #888; font-size:0.95em;">
    <i>This tool is for estimate purposes only. Actual results may vary. Contact us for a customized assessment.</i>
    </div>
    """,
    unsafe_allow_html=True,
)
