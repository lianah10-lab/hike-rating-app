from streamlit_searchbox import st_searchbox
from geopy.geocoders import Nominatim
import streamlit as st
import json, os

# 1. Setup Data
DB = "hiking.json"
if not os.path.exists(DB):
    init = {"trails": {"Sunset Peak": [], "Emerald Lake": []}, "friends": 
["Alex"]}
    with open(DB, "w") as f: json.dump(init, f)

with open(DB, "r") as f:
    data = json.load(f)

# 2. Main UI
st.title("HikeRate App")
show_friends = st.checkbox("Only Show Friends")
# Helper for searching
def search_trails(searchterm: str):
    if not searchterm or len(searchterm) < 3: return []
    geolocator = Nominatim(user_agent="hike_app")
    results = geolocator.geocode(searchterm, exactly_one=False, limit=5)
    return [(r.address, r.address) for r in results] if results else []

# The new search bar
tn = st_searchbox(search_trails, placeholder="Search for any hiking trail...")

if tn and tn not in data["trails"]:
    data["trails"][tn] = []

# 3. Form
with st.expander("Write a Review"):
    name = st.text_input("Name", "User1")
    score = st.slider("Rating", 1.0, 5.0, 4.0, 0.1)
    lvls = ["Beginner", "Easy", "Medium", "Hard", "Expert"]
    diff = st.select_slider("Difficulty Level", options=lvls)
    tags = st.multiselect("Tags", ["Flowers", "Views", "Wildlife"])
    note = st.text_input("Comment")
    
    if st.button("Submit"):
        new = {"u": name, "s": score, "d": diff, "h": tags, "c": note}
        data["trails"][tn].append(new)
        with open(DB, "w") as f: json.dump(data, f)
        st.rerun()

# 4. Display
if tn and tn in data["trails"]:
    for r in data["trails"][tn]:
    is_f = r["u"] in data["friends"]
    if show_friends and not is_f: continue
    st.write(f"User: {r['u']} | Score: {r['s']}")
    st.caption(f"Level: {r['d']} | Tags: {r['h']}")
    if r['c']: st.text(r['c'])
    st.divider()
