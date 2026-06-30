from pathlib import Path
from urllib.parse import quote_plus

import folium
from folium.plugins import Fullscreen, LocateControl

OUTPUT = Path("index.html")

ORIGIN = {
    "name": "Firestone Library",
    "address": "1 Washington Rd, Princeton, NJ 08544",
    "lat": 40.34960,
    "lon": -74.65763,
}

PLACES = [
    {
        "name": "Agricola Eatery",
        "kind": "Cooked steak",
        "access": "Walk",
        "address": "11 Witherspoon St, Princeton, NJ 08542",
        "lat": 40.35048,
        "lon": -74.65975,
        "note": "About a 4–6 minute walk. Check the current menu before visiting.",
        "priority": "Closest cooked-steak option",
    },
    {
        "name": "Yankee Doodle Tap Room",
        "kind": "Cooked steak",
        "access": "Walk",
        "address": "10 Palmer Square E, Princeton, NJ 08542",
        "lat": 40.35065,
        "lon": -74.66133,
        "note": "About a 6–8 minute walk. Check the current menu before visiting.",
        "priority": "Casual downtown option",
    },
    {
        "name": "Witherspoon Grill",
        "kind": "Cooked steak",
        "access": "Walk",
        "address": "57 Witherspoon St, Princeton, NJ 08542",
        "lat": 40.35226,
        "lon": -74.66068,
        "note": "About an 8–10 minute walk. Steak-focused American grill.",
        "priority": "Nearby traditional grill",
    },
    {
        "name": "Roots Steakhouse",
        "kind": "Cooked steak",
        "access": "Walk",
        "address": "98 University Pl, Princeton, NJ 08540",
        "lat": 40.34395,
        "lon": -74.66017,
        "note": "About a 12–15 minute walk. Full steakhouse selection.",
        "priority": "Largest downtown steak selection",
    },
    {
        "name": "The Meeting House",
        "kind": "Cooked steak",
        "access": "Walk",
        "address": "277 Witherspoon St, Princeton, NJ 08540",
        "lat": 40.36044,
        "lon": -74.66492,
        "note": "About a 20–25 minute walk. Check whether steak is on the current menu.",
        "priority": "Longer walk",
    },
    {
        "name": "Whole Earth Center",
        "kind": "Raw steak",
        "access": "Walk",
        "address": "360 Nassau St, Princeton, NJ 08540",
        "lat": 40.35394,
        "lon": -74.64451,
        "note": "About a 20–25 minute walk. Exact cuts and inventory vary.",
        "priority": "Closest walkable raw-steak market",
    },
    {
        "name": "McCaffrey's Food Market",
        "kind": "Raw steak",
        "access": "Walk",
        "address": "301 N Harrison St, Princeton, NJ 08540",
        "lat": 40.36596,
        "lon": -74.64989,
        "note": "About a 30–35 minute walk. Full-service meat counter.",
        "priority": "Strong butcher-counter selection",
    },
    {
        "name": "Ruth's Chris Steak House",
        "kind": "Cooked steak",
        "access": "TigerTransit Route 3",
        "address": "2 Village Blvd, Princeton, NJ 08540",
        "lat": 40.35698,
        "lon": -74.61254,
        "note": "Use Route 3 toward Forrestal/PPPL when operating. Verify the live schedule and final return trip in TripShot.",
        "priority": "TigerTransit-accessible steakhouse",
    },
    {
        "name": "Whole Foods Market",
        "kind": "Raw steak",
        "access": "TigerTransit Route WS",
        "address": "3495 US-1 S, Princeton, NJ 08540",
        "lat": 40.30737,
        "lon": -74.66640,
        "note": "Use the Weekend Shopper when operating. Verify the current schedule in TripShot.",
        "priority": "Butcher-counter option",
    },
    {
        "name": "Wegmans",
        "kind": "Raw steak",
        "access": "TigerTransit Route WS",
        "address": "240 Nassau Park Blvd, Princeton, NJ 08540",
        "lat": 40.30379,
        "lon": -74.67832,
        "note": "Use the Weekend Shopper when operating. Verify the current schedule in TripShot.",
        "priority": "Large grocery selection",
    },
    {
        "name": "Trader Joe's",
        "kind": "Raw steak",
        "access": "TigerTransit Route WS",
        "address": "3528 US-1, Princeton, NJ 08540",
        "lat": 40.30706,
        "lon": -74.68208,
        "note": "Use the Weekend Shopper when operating. Verify the current schedule in TripShot.",
        "priority": "Packaged steak cuts",
    },
    {
        "name": "Eddie V's Prime Seafood",
        "kind": "Cooked steak",
        "access": "TigerTransit Route WS + walk",
        "address": "3535 US-1, Suite 100-C, Princeton, NJ 08540",
        "lat": 40.30775,
        "lon": -74.67495,
        "note": "Use the Weekend Shopper when operating, followed by a walk. Verify the pedestrian route and return schedule.",
        "priority": "TigerTransit fine-dining option",
    },
]


def access_bucket(place: dict) -> str:
    return "Walk" if place["access"] == "Walk" else "Tiger"


def marker_style(place: dict) -> tuple[str, str]:
    if place["kind"] == "Cooked steak" and place["access"] == "Walk":
        return "darkred", "cutlery"
    if place["kind"] == "Raw steak" and place["access"] == "Walk":
        return "green", "shopping-basket"
    if place["kind"] == "Cooked steak":
        return "purple", "bus"
    return "blue", "shopping-cart"


def build_map() -> folium.Map:
    map_object = folium.Map(
        location=[40.342, -74.656],
        zoom_start=12,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    Fullscreen(
        position="topright",
        title="Full screen",
        title_cancel="Exit full screen",
    ).add_to(map_object)
    LocateControl(
        position="topright",
        flyTo=True,
        strings={"title": "Show my location"},
    ).add_to(map_object)

    groups = {
        ("Cooked steak", "Walk"): folium.FeatureGroup(
            name="Cooked steak — walk", show=True
        ),
        ("Raw steak", "Walk"): folium.FeatureGroup(
            name="Raw steak — walk", show=True
        ),
        ("Cooked steak", "Tiger"): folium.FeatureGroup(
            name="Cooked steak — TigerTransit", show=True
        ),
        ("Raw steak", "Tiger"): folium.FeatureGroup(
            name="Raw steak — TigerTransit", show=True
        ),
    }
    for group in groups.values():
        group.add_to(map_object)

    folium.Marker(
        [ORIGIN["lat"], ORIGIN["lon"]],
        tooltip="Start: Firestone Library",
        popup=folium.Popup(
            f"<b>{ORIGIN['name']}</b><br>{ORIGIN['address']}<br>"
            "<b>Your starting point</b>",
            max_width=320,
        ),
        icon=folium.Icon(color="red", icon="book", prefix="fa"),
    ).add_to(map_object)

    for place in PLACES:
        color, icon = marker_style(place)
        travel_mode = "walking" if place["access"] == "Walk" else "transit"
        directions = (
            "https://www.google.com/maps/dir/?api=1"
            f"&origin={quote_plus(ORIGIN['address'])}"
            f"&destination={quote_plus(place['address'])}"
            f"&travelmode={travel_mode}"
        )

        popup_html = f"""
        <div style="font-family:Arial,sans-serif; line-height:1.35; width:310px;">
          <div style="font-size:16px; font-weight:700; margin-bottom:4px;">
            {place['name']}
          </div>
          <div><b>Type:</b> {place['kind']}</div>
          <div><b>Access:</b> {place['access']}</div>
          <div><b>Address:</b> {place['address']}</div>
          <div style="margin-top:7px;">{place['note']}</div>
          <div style="margin-top:7px;">
            <b>Why consider it:</b> {place['priority']}
          </div>
          <div style="margin-top:9px;">
            <a href="{directions}" target="_blank" rel="noopener">
              Open directions
            </a>
          </div>
        </div>
        """

        key = (place["kind"], access_bucket(place))
        folium.Marker(
            [place["lat"], place["lon"]],
            tooltip=f"{place['name']} — {place['access']}",
            popup=folium.Popup(popup_html, max_width=360),
            icon=folium.Icon(color=color, icon=icon, prefix="fa"),
        ).add_to(groups[key])

    folium.Circle(
        [ORIGIN["lat"], ORIGIN["lon"]],
        radius=1609,
        color="#555",
        weight=1,
        fill=False,
        dash_array="5,5",
        tooltip="Approximate 1-mile radius from Firestone",
    ).add_to(map_object)

    folium.PolyLine(
        [
            [40.34370, -74.65920],
            [40.30737, -74.66640],
            [40.30379, -74.67832],
            [40.30706, -74.68208],
        ],
        color="#4b63a8",
        weight=3,
        opacity=0.55,
        dash_array="8,8",
        tooltip="Schematic only: Weekend Shopper sequence",
    ).add_to(map_object)

    folium.LayerControl(collapsed=False).add_to(map_object)

    title_html = """
    <div style="
     position: fixed; top: 10px; left: 50px; right: 90px; z-index: 9999;
     background: rgba(255,255,255,0.96); border: 1px solid #777;
     border-radius: 6px; padding: 10px 14px; font-family: Arial, sans-serif;
     box-shadow: 0 1px 5px rgba(0,0,0,.25);">
      <div style="font-size:18px; font-weight:700;">
        Steak options from Firestone Library — no car required
      </div>
      <div style="font-size:13px; margin-top:3px;">
        Verify restaurant menus, store inventory, and TigerTransit schedules
        before traveling. The dashed blue line is schematic.
      </div>
    </div>
    """
    map_object.get_root().html.add_child(folium.Element(title_html))

    return map_object


if __name__ == "__main__":
    build_map().save(OUTPUT)
    print(f"Created {OUTPUT.resolve()}")
