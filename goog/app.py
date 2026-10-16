import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Multi-Currency Wallet", page_icon="💰", layout="centered")

st.title("💰 Multi-Currency Wallet")
st.write("Convert and calculate multiple currencies to USD")

@st.cache_data(ttl=3600)
def get_exchange_rates():
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode()
            data = json.loads(html_content)
            if data["result"] == "success":
                return data["rates"]
    except Exception as e:
        return None
    return None

rates = get_exchange_rates()

if rates is None:
    st.error("Unable to download data or connect to API")
else:
    st.success("Successfully downloaded data")

    if 'user_list' not in st.session_state:
        st.session_state.user_list = []

    with st.form("wallet_form", clear_on_submit=True):
        st.subheader("Add currency item")
        
        user_input = st.number_input("Please input amount for calculation below:", min_value=0.0, value=100.0, step=10.0)
        
        currency_list = sorted(list(rates.keys()))
        default_idx = currency_list.index("THB") if "THB" in currency_list else 0
        
        curr_key = st.selectbox("Please input currency for calculation below:", currency_list, index=default_idx)
        
        submitted = st.form_submit_button("Add Item")
        
        if submitted:
            rate_value = rates[curr_key]
            amount_usd = user_input / rate_value
            
            st.session_state.user_list.append({
                "amount": user_input,
                "currency": curr_key,
                "usd": amount_usd
            })
            st.success(f"Added {user_input:,.2f} {curr_key} successfully!")

    if st.session_state.user_list:
        st.divider()
        st.subheader("Your Wallet Items:")
        
        total_sum = 0
        for i, item in enumerate(st.session_state.user_list):
            st.write(f"**{i+1}.** {item['amount']:,.2f} {item['currency']} ➔ **${item['usd']:,.2f} USD**")
            total_sum += item['usd']
            
        st.divider()
        st.metric(label="Total Sum", value=f"${total_sum:,.2f} USD")
        
        if st.button("Reset / Clear All"):
            st.session_state.user_list = []
            st.rerun()