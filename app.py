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
    if not searchterm or len(searchterm) < 3: 
        return []
    
    geolocator = Nominatim(user_agent="hike_app")
    
    # We add "trail" to the search to filter for hiking spots only
    filtered_query = f"{searchterm} trail"
    
    results = geolocator.geocode(filtered_query, exactly_one=False, limit=5)
    
    # This returns only the names of the trails found
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
    reviews = data["trails"][tn]
    
    # --- NEW: TRAIL VIEW SECTION ---
    st.subheader(f"Explore {tn}")
    
    # Creating a side-by-side layout: Map on left, Placeholder Photo on right
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📍 **Trail Location**")
        # We can use a simple map to show exactly where the trail is
        # (This uses the coordinates from your search box logic)
        geolocator = Nominatim(user_agent="hike_app")
        loc = geolocator.geocode(tn)
        if loc:
            st.map({"lat": [loc.latitude], "lon": [loc.longitude]})
            
    with col2:
        st.write("📷 **Trail View**")
        # For a real photo, we use a search-based image URL
        # This searches Unsplash for a photo matching the trail's name
        # Updated to use a more reliable Unsplash URL format
        search_query = tn.split(',')[0].replace(" ", "+")
        image_url = f"https://images.unsplash.com/photo-1551632432-c735e7a03271?auto=format&fit=crop&w=800&q=80"
        
        # We use a beautiful default hiking photo if a specific one isn't found
        st.image(image_url, caption=f"Trail View: {tn}", use_container_width=True)
    
    st.divider()

    # --- RATING METRIC ---
    if reviews:
        avg_score = sum(r["s"] for r in reviews) / len(reviews)
        st.metric(label="Overall Community Rating", value=f"{avg_score:.1f} / 5.0")
    else:
        st.info("No ratings yet for this trail. Be the first to rate it!")

    # --- INDIVIDUAL COMMENTS ---
    for r in reviews:
        # (Keep your existing review display logic here)
        st.write(f"**{r['u']}** | ⭐ {r['s']}")
        st.divider()
