
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="ECOSORT | Smart Waste Management",
    page_icon="♻️",
    layout="wide"
)

CATEGORIES = {
    "Biodegradable": {
        "description": "Waste that can break down naturally.",
        "examples": "Fruit peels, vegetable scraps, leaves",
        "disposal": (
            "Place suitable food and garden waste in the "
            "designated organic-waste or composting stream."
        ),
    },
    "Non-biodegradable": {
        "description": "Materials that do not readily break down naturally.",
        "examples": "Clean glass, metal cans, many plastic items",
        "disposal": (
            "Separate recyclable materials according to local "
            "recycling rules. Not every non-biodegradable item "
            "is recyclable."
        ),
    },
    "Toxic": {
        "description": "Waste that may contain substances harmful to health or the environment.",
        "examples": "Certain chemical residues and contaminated materials",
        "disposal": (
            "Do not pour chemicals into drains or mix unknown "
            "substances. Follow local hazardous-waste guidance."
        ),
    },
    "Hazardous": {
        "description": "Waste requiring special handling because it presents a safety or environmental risk.",
        "examples": "Batteries, certain electronic waste and chemical containers",
        "disposal": (
            "Keep the item separate from ordinary household waste "
            "and use an authorized collection or disposal service."
        ),
    },
}

st.title("♻️ ECOSORT")
st.subheader("AI-Based Smart Solid Waste Management")
st.write(
    "Upload a waste image, explore the four waste categories, "
    "and view disposal guidance."
)

st.info(
    "Prototype mode: category selection below is for demonstration. "
    "This version does not yet predict waste categories using AI."
)

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["Waste Classifier", "Dashboard", "About Project"]
)

if "history" not in st.session_state:
    st.session_state.history = []

if page == "Waste Classifier":
    st.header("Waste Classification")

    uploaded_file = st.file_uploader(
        "Upload a waste image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file:
        st.image(
            uploaded_file,
            caption="Uploaded waste image",
            use_container_width=True
        )

    st.markdown("### Demonstration classification")
    st.write(
        "Choose a category to test the interface. "
        "The choice is not an AI-generated prediction."
    )

    selected_category = st.selectbox(
        "Select a category",
        list(CATEGORIES.keys())
    )

    if st.button("Show Classification Result", type="primary"):
        details = CATEGORIES[selected_category]

        result = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": selected_category,
            "image_name": (
                uploaded_file.name if uploaded_file else "No image"
            ),
            "mode": "Demonstration"
        }

        st.session_state.history.insert(0, result)

        st.success(f"Demonstration category: {selected_category}")
        st.write(details["description"])
        st.write(f"**Examples:** {details['examples']}")
        st.write(f"**Disposal guidance:** {details['disposal']}")

        if selected_category in ["Toxic", "Hazardous"]:
            st.warning(
                "Do not handle unknown waste based on this demo. "
                "Use official local guidance or a qualified waste "
                "management service."
            )

        st.caption(
            "No AI prediction or confidence score was calculated."
        )

elif page == "Dashboard":
    st.header("Classification Dashboard")

    history = st.session_state.history

    col1, col2 = st.columns(2)
    col1.metric("Total demo records", len(history))
    col2.metric(
        "Categories explored",
        len(set(item["category"] for item in history))
    )

    if history:
        counts = {}
        for item in history:
            category = item["category"]
            counts[category] = counts.get(category, 0) + 1

        st.subheader("Records by category")
        st.bar_chart(counts)

        st.subheader("Recent classification history")
        st.dataframe(history, use_container_width=True)

        if st.button("Clear demonstration history"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info(
            "No records yet. Visit Waste Classifier and "
            "create a demonstration record first."
        )

elif page == "About Project":
    st.header("About ECOSORT")
    st.write(
        "ECOSORT is a prototype for AI-based solid waste "
        "management and disposal guidance."
    )

    st.subheader("Project objectives")
    st.markdown(
        """
        - Explore four categories of solid waste.
        - Provide category-specific disposal guidance.
        - Develop an image-upload interface.
        - Display a dashboard and demonstration history.
        - Prepare for integration of a trained AI model.
        """
    )

    st.subheader("Technology")
    st.write("Python, Streamlit and GitHub")

    st.warning(
        "The current version is a user-interface prototype. "
        "AI image classification, model validation and persistent "
        "database storage have not yet been implemented."
    )

st.divider()
st.caption("ECOSORT | Academic software prototype")
