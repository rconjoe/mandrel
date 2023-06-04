import json
import os

import streamlit as st
from jina import Client, Document, DocumentArray
import io

st.set_page_config(
    page_title="Auction Bidding Executor",
    page_icon=":money_with_wings:",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Auction Bidding Executor")
st.markdown(
    "A microservice for managing auctions. To generate and deploy your own microservice, click [here](https://github.com/jina-ai/dev-gpt)."
)
st.subheader(":pencil: Input Parameters")
with st.form(key="input_form"):
    auction_id = st.number_input("Auction ID", min_value=0, step=1)
    item_name = st.text_input("Item Name")
    minimum_bid = st.number_input("Minimum Bid", min_value=0.0, step=0.01)
    start_time = st.number_input("Start Time (Unix Timestamp)", min_value=0, step=1)
    end_time = st.number_input("End Time (Unix Timestamp)", min_value=0, step=1)
    bids = st.text_area("Bids (JSON Array)", "[]")

    try:
        bids = json.loads(bids)
    except json.JSONDecodeError:
        st.error("Invalid JSON format for bids")

    if not isinstance(bids, list):
        st.error("Bids must be a JSON array")

    for bid in bids:
        if not isinstance(bid, dict):
            st.error("Each bid must be a JSON object")
        elif "user_id" not in bid or "bid_amount" not in bid:
            st.error("Each bid must have a user_id and bid_amount")

    input_dict = {
        "auction_id": auction_id,
        "item_name": item_name,
        "minimum_bid": minimum_bid,
        "start_time": start_time,
        "end_time": end_time,
        "bids": bids,
    }

    input_json_dict_string = json.dumps(input_dict)
    submitted = st.form_submit_button("Submit")

if submitted:
    with st.spinner("Processing input..."):
        client = Client(host="http://localhost:8080")
        d = Document(text=input_json_dict_string)
        response = client.post("/", inputs=DocumentArray([d]))

        if not response:
            st.error("No response from microservice")
        elif not response[0].text:
            st.error("Empty response from microservice")
        else:
            try:
                output_data = json.loads(response[0].text)
            except json.JSONDecodeError:
                st.error("Invalid JSON format for output")

            if "status" not in output_data or "message" not in output_data:
                st.error("Invalid output format")
            elif output_data["status"] == "failure":
                st.error(output_data["message"])
            else:
                st.subheader(":clipboard: Output")
                st.success(output_data["message"])

deployment_id = os.environ.get("K8S_NAMESPACE_NAME", "")
api_endpoint = (
    f"https://dev-gpt-{deployment_id.split('-')[1]}.wolf.jina.ai/post"
    if deployment_id
    else "http://localhost:8080/post"
)

with st.expander("See curl command"):
    st.markdown("You can use the following curl command to send a request to the microservice from the command line:")
    escaped_input_json_dict_string = input_json_dict_string.replace('"', '\\"')

    st.code(
        f'curl -X "POST" "{api_endpoint}" -H "accept: application/json" -H "Content-Type: application/json" -d \'{{"data": [{{"text": "{escaped_input_json_dict_string}"}}]}}\'',
        language="bash",
    )