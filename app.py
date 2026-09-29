import streamlit as st
import pandas as pd
from pathlib import Path
import json

st.set_page_config(page_title="ContractLens", page_icon="🔎", layout="wide")

BASE = Path(__file__).parent
with open(BASE / "data" / "contract.json", "r", encoding="utf-8") as f:
    contract = json.load(f)
with open(BASE / "data" / "amendments.json", "r", encoding="utf-8") as f:
    amendments = json.load(f)

st.title("🔎 ContractLens")
st.caption("Evidence-based contract change tracking and cumulative deviation analysis")

with st.sidebar:
    st.header("Project")
    st.write(contract["project_name"])
    st.write(f"**Contract ID:** {contract['contract_id']}")
    st.write(f"**Baseline value:** ₹{contract['original_cost']:,.0f}")
    st.write(f"**Baseline duration:** {contract['original_duration_days']} days")
    st.divider()
    st.info("Demo data is synthetic and intended for hackathon demonstration.")

# Build current state
current = contract.copy()
for a in amendments:
    for key in ["cost", "duration_days", "contractor", "material", "scope"]:
        if key in a["changes"]:
            current[{"cost":"current_cost","duration_days":"current_duration_days",
                     "contractor":"current_contractor","material":"current_material",
                     "scope":"current_scope"}[key]] = a["changes"][key]

cost_delta = current["current_cost"] - contract["original_cost"]
duration_delta = current["current_duration_days"] - contract["original_duration_days"]
cost_pct = cost_delta / contract["original_cost"] * 100
duration_pct = duration_delta / contract["original_duration_days"] * 100

attention = 0
if abs(cost_pct) >= 10: attention += 35
elif abs(cost_pct) >= 5: attention += 20
if abs(duration_pct) >= 10: attention += 25
elif abs(duration_pct) >= 5: attention += 15
if current["current_contractor"] != contract["contractor"]: attention += 15
if current["current_material"] != contract["material"]: attention += 10
if current["current_scope"] != contract["scope"]: attention += 15
unsupported = sum(1 for a in amendments if not a["rationale"]["supported"])
attention = min(100, attention + unsupported * 10)

tabs = st.tabs(["📊 Overview", "🔄 Changes", "🧾 Rationale Register", "📎 Evidence"])

with tabs[0]:
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Current Cost", f"₹{current['current_cost']:,.0f}", f"{cost_pct:+.1f}%")
    c2.metric("Timeline", f"{current['current_duration_days']} days", f"{duration_delta:+d} days")
    c3.metric("Amendments", len(amendments))
    c4.metric("Review Attention", f"{attention}/100")

    st.subheader("Original vs Current State")
    comparison = pd.DataFrame([
        ["Cost", f"₹{contract['original_cost']:,.0f}", f"₹{current['current_cost']:,.0f}"],
        ["Duration", f"{contract['original_duration_days']} days", f"{current['current_duration_days']} days"],
        ["Contractor", contract["contractor"], current["current_contractor"]],
        ["Material", contract["material"], current["current_material"]],
        ["Scope", contract["scope"], current["current_scope"]],
    ], columns=["Factor","Original","Current"])
    st.dataframe(comparison, use_container_width=True, hide_index=True)

    st.subheader("Attention factors")
    factors = pd.DataFrame([
        ["Cost deviation", round(cost_pct,1), "High" if abs(cost_pct)>=10 else "Moderate" if abs(cost_pct)>=5 else "Low"],
        ["Timeline deviation", round(duration_pct,1), "High" if abs(duration_pct)>=10 else "Moderate" if abs(duration_pct)>=5 else "Low"],
        ["Contractor change", "Yes" if current["current_contractor"] != contract["contractor"] else "No", "Structural"],
        ["Material/specification change", "Yes" if current["current_material"] != contract["material"] else "No", "Structural"],
        ["Scope change", "Yes" if current["current_scope"] != contract["scope"] else "No", "Structural"],
        ["Unsupported rationale", unsupported, "Review" if unsupported else "Documented"],
    ], columns=["Factor","Deviation","Indicator"])
    st.dataframe(factors, use_container_width=True, hide_index=True)

with tabs[1]:
    st.subheader("Amendment timeline")
    for i,a in enumerate(amendments,1):
        with st.expander(f"Amendment {i} — {a['date']} — {a['title']}"):
            st.write(a["description"])
            rows=[]
            for k,v in a["changes"].items():
                original = contract.get({"cost":"original_cost","duration_days":"original_duration_days",
                                         "contractor":"contractor","material":"material","scope":"scope"}[k])
                rows.append([k.replace("_"," ").title(), original, v])
            st.dataframe(pd.DataFrame(rows, columns=["Field","Original baseline","Amended value"]),
                         use_container_width=True, hide_index=True)
            st.write("**Rationale:**", a["rationale"]["reason"])
            st.write("**Evidence:**", a["rationale"]["evidence"])
            st.write("**Evidence status:**", "Supported" if a["rationale"]["supported"] else "Needs review")

with tabs[2]:
    st.subheader("Rationale Register")
    rr=[]
    for i,a in enumerate(amendments,1):
        rr.append({
            "Amendment": f"A-{i:02d}",
            "Date": a["date"],
            "Change": a["title"],
            "Reason": a["rationale"]["reason"],
            "Evidence": a["rationale"]["evidence"],
            "Status": "Supported" if a["rationale"]["supported"] else "Needs review"
        })
    st.dataframe(pd.DataFrame(rr), use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("Supporting evidence")
    for a in amendments:
        st.markdown(f"**{a['title']}**")
        st.code(a["rationale"]["evidence"])
        st.divider()

st.caption("ContractLens helps identify changes requiring attention; it does not assume that a change is improper.")
