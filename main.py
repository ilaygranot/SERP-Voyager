import streamlit as st
import pandas as pd
from app import get_search_results, parse_search_results, extract_html_content, save_to_csv
from parameters import google_languages, google_countries, google_domains, devices, mobile_os

st.set_page_config(page_title="SpaceSerp App", layout="wide")

st.title("SpaceSerp App")
st.subheader("Extract search results using SpaceSerp API")

with st.sidebar:
    st.header("Parameters")
    api_key = st.text_input("API Key", value="", help="Enter your SpaceSerp API Key.", type="password")
    query = st.text_input("Query", value="", help="Enter a keyword to search.")
    domain = st.selectbox("Domain", [x["domain"] for x in google_domains])
    gl = st.selectbox("Country Code", [x["code"] for x in google_countries])
    hl = st.selectbox("Language Code", [x["code"] for x in google_languages])
    device = st.selectbox("Device", devices)
    mobile_os = st.selectbox("Mobile OS", mobile_os) if device != "desktop" else None
    page_size = st.number_input("Page Size", min_value=1, max_value=100, value=10, step=1)
    page_number = st.number_input("Page Number", min_value=1, value=1, step=1)

if st.button("Fetch Search Results"):
    if not api_key:
        st.error("Please provide an API key.")
    elif not query:
        st.error("Please provide a query.")
    else:
        response = get_search_results(
            api_key,
            query,
            domain=domain,
            gl=gl,
            hl=hl,
            device=device
        )

        search_results = parse_search_results(response)

        # Create a dataframe to display the results
        data = {
            "title": [],
            "link": [],
            "snippet": []
        }
        for result in search_results:
            data["title"].append(result["title"])
            data["link"].append(result["link"])
            data["snippet"].append(result["snippet"])

        df = pd.DataFrame(data)

        st.header("Search Results")
        st.write(df)

        # Save results and HTML content to a CSV file
        csv_file_name = "search_results.csv"
        all_results = []
        for result in search_results:
            url = result["link"]
            html_content = extract_html_content(url)
            result["keyword"] = query
            result["html_content"] = html_content
            all_results.append(result)

        save_to_csv(all_results, csv_file_name)
        st.success(f"Search results saved to {csv_file_name}")

