from streamlit_searchbox import st_searchbox
from geopy.geocoders import Nominatim
import streamlit as st
import json, os

if "upload_mode" not in st.session_state:
    st.session_state.upload_mode = False
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

# 3.
with col2:
        st.write("📷 **Trail View**")
        
        # 1. Find all reviews for this specific trail that include an image
        photos = [r["img"] for r in reviews if r.get("img")]
        
        if photos:
            # If photos exist, display the most recent one submitted
            import base64
            st.image(
                base64.b64decode(photos[-1]), 
                caption=f"Shared by the community", 
                use_container_width=True
            )
            
            # If there are multiple photos, let the user know there are more below
            if len(photos) > 1:
                st.caption(f"Plus {len(photos)-1} more photos in the reviews below!")
        
        else:
            # 2. If no photos exist, show the placeholder and the trigger button
            st.info("Ooops, no photos yet. Be the first to share this trail!")
            
            if st.button("📤 Upload photos"):
                # This sets the session state to True so the expander opens
                st.session_state.upload_mode = True
                st.rerun()

# 4. Display
if tn and tn in data["trails"]:
    reviews = data["trails"][tn]
    st.subheader(f"Explore {tn}")

    # This creates the two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.write("📍 **Trail Location**")
        geolocator = Nominatim(user_agent="hike_app")
        loc = geolocator.geocode(tn)
        if loc:
            st.map({"lat": [loc.latitude], "lon": [loc.longitude]})

    with col2:
        st.write("📷 **Trail View**")
        
        # Logic to find images in the reviews
        photos = [r["img"] for r in reviews if r.get("img")]
        
        if photos:
            import base64
            st.image(base64.b64decode(photos[-1]), caption="Shared by the community", use_container_width=True)
            if len(photos) > 1:
                st.caption(f"Plus {len(photos)-1} more photos below!")
        else:
            st.info("Ooops, no photos yet. Be the first to share this trail!")
            if st.button("📤 Upload photos"):
                st.session_state.upload_mode = True
                st.rerun()

    st.divider()
    
    # --- RATING METRIC & REVIEWS ---
    if reviews:
        avg_score = sum(r["s"] for r in reviews) / len(reviews)
        st.metric(label="Overall Rating", value=f"{avg_score:.1f} / 5.0")
        
        for r in reviews:
            st.write(f"**{r['u']}** | ⭐ {r['s']}")
            if r.get('img'):
                st.image(base64.b64decode(r['img']), width=150)
            st.caption(f"Level: {r['d']}")
            st.divider()
