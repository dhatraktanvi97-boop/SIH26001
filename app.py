import streamlit as st
import folium
import joblib
import random
import os
import pandas as pd
from datetime import datetime
from streamlit_folium import st_folium

from data.sites import MONITORING_SITES


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SIH26001 - Hazard Monitoring",
    page_icon="🌍",
    layout="wide"
)


# =========================================================
# LOAD AI MODEL
# =========================================================

MODEL_PATH = "ai_model/landslide_model.pkl"

if not os.path.exists(MODEL_PATH):
    st.error(
        "AI model not found. Please run:\n\n"
        "py -3.13 ai_model/train_model.py"
    )
    st.stop()

model = joblib.load(MODEL_PATH)


# =========================================================
# RISK FUNCTIONS
# =========================================================

def risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    return "LOW"


def calculate_flood_score(
    rainfall,
    water_level
):

    score = (
        rainfall * 0.5
        + water_level * 0.5
    )

    return min(
        round(score, 2),
        100
    )


def calculate_ground_collapse_score(
    ground_movement,
    soil_moisture
):

    score = (
        ground_movement * 5 * 0.6
        + soil_moisture * 0.4
    )

    return min(
        round(score, 2),
        100
    )


# =========================================================
# REALISTIC SENSOR SIMULATOR
# =========================================================

def generate_sensor_reading(
    previous=None
):

    # First reading for a site
    if previous is None:

        return {

            "rainfall":
                round(
                    random.uniform(10, 80),
                    2
                ),

            "soil_moisture":
                round(
                    random.uniform(40, 70),
                    2
                ),

            "ground_movement":
                round(
                    random.uniform(0.5, 5),
                    2
                ),

            "water_level":
                round(
                    random.uniform(20, 60),
                    2
                ),

            "last_update":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }


    # -----------------------------------------------------
    # Gradual sensor changes
    # -----------------------------------------------------

    rainfall = (
        previous["rainfall"]
        + random.uniform(-8, 15)
    )

    soil_moisture = (
        previous["soil_moisture"]
        + random.uniform(-3, 5)
    )

    ground_movement = (
        previous["ground_movement"]
        + random.uniform(-0.5, 1.2)
    )

    water_level = (
        previous["water_level"]
        + random.uniform(-3, 6)
    )


    # -----------------------------------------------------
    # Keep values within physical ranges
    # -----------------------------------------------------

    rainfall = max(
        0,
        min(300, rainfall)
    )

    soil_moisture = max(
        0,
        min(100, soil_moisture)
    )

    ground_movement = max(
        0,
        min(20, ground_movement)
    )

    water_level = max(
        0,
        min(100, water_level)
    )


    return {

        "rainfall":
            round(
                rainfall,
                2
            ),

        "soil_moisture":
            round(
                soil_moisture,
                2
            ),

        "ground_movement":
            round(
                ground_movement,
                2
            ),

        "water_level":
            round(
                water_level,
                2
            ),

        "last_update":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }


# =========================================================
# INITIALIZE MONITORING SITES
# =========================================================

if "site_data" not in st.session_state:

    st.session_state.site_data = {}

    for site_id in MONITORING_SITES:

        st.session_state.site_data[site_id] = (
            generate_sensor_reading()
        )


# =========================================================
# TRACK NEW SENSOR READING
# =========================================================

if "new_reading" not in st.session_state:

    st.session_state.new_reading = False


# =========================================================
# SELECTED SITE
# =========================================================

site_ids = list(
    MONITORING_SITES.keys()
)


if "selected_site_id" not in st.session_state:

    st.session_state.selected_site_id = (
        site_ids[0]
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "🌍 Monitoring Network"
)


selected_site_id = st.sidebar.selectbox(

    "Select Monitoring Site",

    site_ids,

    key="selected_site_id",

    format_func=lambda x:
        MONITORING_SITES[x]["name"]
)


selected_site = MONITORING_SITES[
    selected_site_id
]


selected_data = (
    st.session_state.site_data[
        selected_site_id
    ]
)


# =========================================================
# UPDATE SENSOR DATA
# =========================================================

if st.sidebar.button(
    "🔄 Get New Sensor Readings"
):

    previous_data = (
        st.session_state.site_data[
            selected_site_id
        ]
    )


    st.session_state.site_data[
        selected_site_id
    ] = generate_sensor_reading(
        previous_data
    )


    st.session_state.new_reading = True

    st.rerun()


# =========================================================
# HEADER
# =========================================================

st.title(
    "🌍 AI-Based Early Warning & "
    "Hazard Monitoring System"
)

st.caption(
    "SIH26001 | Landslide Risk Monitoring "
    "for the North Eastern Region"
)


# =========================================================
# SITE INFORMATION
# =========================================================

st.subheader(
    f"📍 {selected_site['name']}"
)


st.write(
    f"**Location:** "
    f"{selected_site['city']}, "
    f"{selected_site['state']}"
)


st.write(
    f"**Site ID:** `{selected_site_id}`  |  "
    f"**Status:** 🟢 {selected_site['status']}"
)


st.caption(
    f"Last sensor update: "
    f"{selected_data['last_update']}"
)


# =========================================================
# AI INPUT DATA
# =========================================================

input_data = pd.DataFrame(

    [[

        selected_data["rainfall"],

        selected_data["soil_moisture"],

        selected_data["ground_movement"],

        selected_data["water_level"]

    ]],

    columns=[

        "rainfall",

        "soil_moisture",

        "ground_movement",

        "water_level"

    ]
)


# =========================================================
# AI LANDSLIDE PREDICTION
# =========================================================

landslide_prediction = model.predict(
    input_data
)[0]


# =========================================================
# FLOOD RISK
# =========================================================

flood_score = calculate_flood_score(

    selected_data["rainfall"],

    selected_data["water_level"]

)

flood_risk = risk_level(
    flood_score
)


# =========================================================
# GROUND COLLAPSE RISK
# =========================================================

ground_collapse_score = (
    calculate_ground_collapse_score(

        selected_data[
            "ground_movement"
        ],

        selected_data[
            "soil_moisture"
        ]
    )
)


ground_collapse_risk = risk_level(
    ground_collapse_score
)


# =========================================================
# OVERALL RISK
# =========================================================

risk_values = {

    "Landslide":
        landslide_prediction,

    "Flood":
        flood_risk,

    "Ground Collapse":
        ground_collapse_risk

}


risk_order = {

    "LOW": 1,

    "MEDIUM": 2,

    "HIGH": 3

}


highest_hazard = max(

    risk_values,

    key=lambda x:
        risk_order[
            risk_values[x]
        ]

)


overall_risk = risk_values[
    highest_hazard
]


# =========================================================
# ALERT SYSTEM
# =========================================================

st.subheader(
    "🚨 Current Hazard Status"
)


if overall_risk == "HIGH":

    st.error(
        f"🔴 HIGH RISK — "
        f"{highest_hazard}"
    )

    st.warning(
        "Immediate monitoring and "
        "appropriate emergency response "
        "should be considered."
    )


elif overall_risk == "MEDIUM":

    st.warning(
        f"🟠 MEDIUM RISK — "
        f"{highest_hazard}"
    )

    st.info(
        "Increase monitoring frequency "
        "and watch for rapid changes."
    )


else:

    st.success(
        f"🟢 LOW RISK — "
        f"{highest_hazard}"
    )


# =========================================================
# SENSOR READINGS
# =========================================================

st.subheader(
    "📡 Sensor Readings"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(

        "Rainfall",

        f"{selected_data['rainfall']} mm"

    )


with col2:

    st.metric(

        "Soil Moisture",

        f"{selected_data['soil_moisture']} %"

    )


with col3:

    st.metric(

        "Ground Movement",

        f"{selected_data['ground_movement']} mm"

    )


with col4:

    st.metric(

        "Water Level",

        f"{selected_data['water_level']} %"

    )


# =========================================================
# HAZARD ANALYSIS
# =========================================================

st.subheader(
    "🧠 AI Hazard Analysis"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.write(
        "🏔️ **Landslide**"
    )

    if landslide_prediction == "HIGH":

        st.error("HIGH")

    elif landslide_prediction == "MEDIUM":

        st.warning("MEDIUM")

    else:

        st.success("LOW")


with col2:

    st.write(
        "🌊 **Flood**"
    )

    st.metric(
        "Risk Score",
        flood_score
    )

    st.write(
        f"Risk Level: **{flood_risk}**"
    )


with col3:

    st.write(
        "⛏️ **Ground Collapse**"
    )

    st.metric(
        "Risk Score",
        ground_collapse_score
    )

    st.write(
        f"Risk Level: **{ground_collapse_risk}**"
    )


# =========================================================
# MAP
# =========================================================

st.subheader(
    "🗺️ Regional Monitoring Network"
)


st.caption(
    "Click a monitoring-site marker "
    "to inspect that site."
)


hazard_map = folium.Map(

    location=[
        25.5,
        92.5
    ],

    zoom_start=6,

    tiles="OpenStreetMap"
)


# =========================================================
# ADD MONITORING SITES
# =========================================================

for site_id, site in (
    MONITORING_SITES.items()
):

    data = (
        st.session_state.site_data[
            site_id
        ]
    )


    # -----------------------------------------------------
    # AI prediction for this site
    # -----------------------------------------------------

    site_input = pd.DataFrame(

        [[

            data["rainfall"],

            data["soil_moisture"],

            data["ground_movement"],

            data["water_level"]

        ]],

        columns=[

            "rainfall",

            "soil_moisture",

            "ground_movement",

            "water_level"

        ]
    )


    site_landslide = model.predict(
        site_input
    )[0]


    # -----------------------------------------------------
    # Flood
    # -----------------------------------------------------

    site_flood_score = (
        calculate_flood_score(

            data["rainfall"],

            data["water_level"]

        )
    )


    site_flood = risk_level(
        site_flood_score
    )


    # -----------------------------------------------------
    # Ground collapse
    # -----------------------------------------------------

    site_ground_score = (
        calculate_ground_collapse_score(

            data["ground_movement"],

            data["soil_moisture"]

        )
    )


    site_ground = risk_level(
        site_ground_score
    )


    # -----------------------------------------------------
    # Overall site risk
    # -----------------------------------------------------

    site_risks = {

        "Landslide":
            site_landslide,

        "Flood":
            site_flood,

        "Ground Collapse":
            site_ground

    }


    site_highest_hazard = max(

        site_risks,

        key=lambda x:
            risk_order[
                site_risks[x]
            ]

    )


    site_overall = site_risks[
        site_highest_hazard
    ]


    # -----------------------------------------------------
    # Marker colour
    # -----------------------------------------------------

    if site_overall == "HIGH":

        marker_color = "red"

    elif site_overall == "MEDIUM":

        marker_color = "orange"

    else:

        marker_color = "green"


    # -----------------------------------------------------
    # Popup
    # -----------------------------------------------------

    popup_html = f"""

    <div style="width:280px">

        <h4>
            📍 {site['name']}
        </h4>

        <b>Site ID:</b>
        {site_id}

        <br>

        <b>Location:</b>
        {site['city']},
        {site['state']}

        <br>

        <b>Status:</b>
        🟢 {site['status']}

        <hr>

        <b>🌧️ Rainfall:</b>
        {data['rainfall']} mm

        <br>

        <b>💧 Soil Moisture:</b>
        {data['soil_moisture']} %

        <br>

        <b>📈 Ground Movement:</b>
        {data['ground_movement']} mm

        <br>

        <b>🌊 Water Level:</b>
        {data['water_level']} %

        <hr>

        <b>🏔️ Landslide:</b>
        {site_landslide}

        <br>

        <b>🌊 Flood:</b>
        {site_flood}

        <br>

        <b>⛏️ Ground Collapse:</b>
        {site_ground}

        <hr>

        <b>⚠️ Overall Risk:</b>
        {site_overall}

        <br><br>

        <small>
            Last update:
            {data['last_update']}
        </small>

    </div>

    """


    # -----------------------------------------------------
    # Marker
    # -----------------------------------------------------

    folium.Marker(

        location=[

            site["latitude"],

            site["longitude"]

        ],

        popup=folium.Popup(

            popup_html,

            max_width=320

        ),

        tooltip=(

            f"{site['name']} | "
            f"{site_overall} RISK"

        ),

        icon=folium.Icon(

            color=marker_color,

            icon="info-sign"

        )

    ).add_to(hazard_map)


# =========================================================
# DISPLAY MAP
# =========================================================

map_result = st_folium(

    hazard_map,

    width=None,

    height=550,

    returned_objects=[
        "last_object_clicked"
    ]

)


# =========================================================
# MAP CLICK DETECTION
# =========================================================

clicked = map_result.get(
    "last_object_clicked"
)


if clicked:

    clicked_lat = clicked.get(
        "lat"
    )

    clicked_lon = clicked.get(
        "lng"
    )


    if (

        clicked_lat is not None

        and

        clicked_lon is not None

    ):

        nearest_site = None

        smallest_distance = (
            float("inf")
        )


        for site_id, site in (
            MONITORING_SITES.items()
        ):

            distance = (

                (
                    site["latitude"]
                    - clicked_lat
                ) ** 2

                +

                (
                    site["longitude"]
                    - clicked_lon
                ) ** 2

            )


            if (
                distance
                < smallest_distance
            ):

                smallest_distance = (
                    distance
                )

                nearest_site = (
                    site_id
                )


        if (

            nearest_site

            and

            nearest_site
            !=
            st.session_state[
                "selected_site_id"
            ]

        ):

            st.session_state[
                "selected_site_id"
            ] = nearest_site

            st.rerun()


# =========================================================
# SELECTED SITE DETAILS
# =========================================================

st.subheader(
    "📋 Monitoring Site Details"
)


detail1, detail2 = st.columns(2)


with detail1:

    st.write(
        f"**Site:** "
        f"{selected_site['name']}"
    )

    st.write(
        f"**Site ID:** "
        f"{selected_site_id}"
    )

    st.write(
        f"**City:** "
        f"{selected_site['city']}"
    )

    st.write(
        f"**State:** "
        f"{selected_site['state']}"
    )

    st.write(
        f"**Coordinates:** "
        f"{selected_site['latitude']}, "
        f"{selected_site['longitude']}"
    )


with detail2:

    st.write(
        f"**Landslide:** "
        f"{landslide_prediction}"
    )

    st.write(
        f"**Flood:** "
        f"{flood_risk}"
    )

    st.write(
        f"**Ground Collapse:** "
        f"{ground_collapse_risk}"
    )

    st.write(
        f"**Overall Risk:** "
        f"{overall_risk}"
    )


# =========================================================
# HISTORICAL MONITORING
# =========================================================

st.subheader(
    "📊 Historical Monitoring"
)


HISTORY_FILE = (
    "data/monitoring_history.csv"
)


# =========================================================
# ONLY LOG WHEN A NEW READING WAS GENERATED
# =========================================================

if st.session_state.new_reading:

    history_record = {

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "site_id":
            selected_site_id,

        "site_name":
            selected_site["name"],

        "rainfall":
            selected_data["rainfall"],

        "soil_moisture":
            selected_data["soil_moisture"],

        "ground_movement":
            selected_data[
                "ground_movement"
            ],

        "water_level":
            selected_data[
                "water_level"
            ],

        "landslide_risk":
            landslide_prediction,

        "flood_risk":
            flood_risk,

        "ground_collapse_risk":
            ground_collapse_risk
    }


    if os.path.exists(
        HISTORY_FILE
    ):

        history_df = pd.read_csv(
            HISTORY_FILE
        )

    else:

        history_df = pd.DataFrame()


    new_row = pd.DataFrame(
        [history_record]
    )


    history_df = pd.concat(

        [
            history_df,
            new_row
        ],

        ignore_index=True

    )


    history_df.to_csv(

        HISTORY_FILE,

        index=False

    )


    st.session_state.new_reading = False


# =========================================================
# LOAD HISTORY
# =========================================================

if os.path.exists(
    HISTORY_FILE
):

    history_df = pd.read_csv(
        HISTORY_FILE
    )

else:

    history_df = pd.DataFrame()


# =========================================================
# SITE HISTORY
# =========================================================

if not history_df.empty:

    site_history = history_df[

        history_df["site_id"]
        ==
        selected_site_id

    ].copy()


    if len(site_history) > 1:

        site_history[
            "timestamp"
        ] = pd.to_datetime(

            site_history[
                "timestamp"
            ]

        )


        site_history = (
            site_history.sort_values(
                "timestamp"
            )
        )


        st.write(

            "Historical data — "
            f"**{selected_site['name']}**"

        )


        st.line_chart(

            site_history.set_index(
                "timestamp"
            )[

                [

                    "rainfall",

                    "soil_moisture",

                    "ground_movement",

                    "water_level"

                ]

            ]

        )

    else:

        st.info(
            "More readings are required "
            "to display historical trends."
        )

else:

    st.info(
        "Generate new sensor readings "
        "to begin historical monitoring."
    )


# =========================================================
# SYSTEM STATUS
# =========================================================

st.subheader(
    "⚙️ System Status"
)


status1, status2, status3 = (
    st.columns(3)
)


with status1:

    st.success(
        "AI Model: ONLINE"
    )


with status2:

    st.success(
        "Monitoring Network: ONLINE"
    )


with status3:

    st.success(
        "Alert Engine: ACTIVE"
    )


# =========================================================
# PROTOTYPE NOTICE
# =========================================================

st.caption(

    "Prototype: sensor values are currently "
    "simulated. In deployment, the same "
    "pipeline will receive measurements "
    "from field monitoring units."

)