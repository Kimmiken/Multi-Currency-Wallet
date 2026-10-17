import json
import urllib.request
import streamlit as st

st.title(" Multi-Currency Wallet ")

@st.cache_data
def fetch_rates():
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if data["result"] == "success":
                return data["rates"]
    except Exception as e:
        st.error(f"Error occurred: {e}")
    return {}

rates = fetch_rates()

if not rates:
    st.error("Cannot load exchange rates. Please check your internet connection.")
    st.stop()

if 'user_list' not in st.session_state:
    st.session_state.user_list = []

currency_list = sorted(list(rates.keys()))

with st.form("wallet_form", clear_on_submit=True):
    st.subheader("Input ypur amount and currebcy below")
    user_input = st.number_input("Add amount:", min_value=0.0, step=1.0)
    curr_key = st.selectbox("Add currency:", currency_list)
    
    submitted = st.form_submit_button("➕ Added to wallet (Continue)")
    
    if submitted:
        if user_input > 0:
            rate_value = rates[curr_key]
            amount_usd = user_input / rate_value
            st.session_state.user_list.append({
                "amount": user_input,
                "currency": curr_key,
                "usd": amount_usd
            })
            st.success(f"Successfully added: {user_input:,.2f} {curr_key} ")
        else:
            st.warning("Please input amount greater than 0")

if st.session_state.user_list:
    st.markdown("---")
    st.subheader("List fo your wallet")
    
    total_usd = sum(item['usd'] for item in st.session_state.user_list)
    
    for i, item in enumerate(st.session_state.user_list):
        st.write(f"**{i+1}.** {item['amount']:,.2f} {item['currency']} $\rightarrow$ **${item['usd']:,.2f} USD**")

    st.markdown("---")
    st.subheader("Calculate")
    
    total_curr = st.selectbox("Select output currency:", currency_list, key="total_curr_select")
    
    if st.button("Calculate Total"):
        if total_curr == "USD":
            total_sum = total_usd
        else:
            total_sum = total_usd * rates[total_curr]
            
        st.success(f"Your total will be **{total_sum:,.2f} {total_curr}**")

    if st.button("Clear all"):
        st.session_state.user_list = []
        st.rerun()
