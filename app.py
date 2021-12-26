##########
# LIBRARIES
##########
import pandas as pd
import streamlit as st
import requests
from PIL import Image

# PAGE CONFIG
########

st.set_page_config(layout="wide", page_title='Light Pollution Network')
row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((3, .2, 0.65, .1))
row0_1.title('Light Pollution Network')
with row0_2:
    st.write('')
row0_2.subheader('Web App by [Toby Avila](https://www.linkedin.com/in/toby-avila-118080208/)')
st.subheader('_Was the data helpful?_')

row3_1, row3_spacer2 = st.columns((3.2, .1))
with row3_1:
    st.markdown(
        "Hello there! Have you ever spent your weekend watching the night sky and had yourself complaining about how 'it's so hard to the see the stars with all this light pollution in my area' ? Well, this interactive application containing Globe at Night and Unihedron Database data allows you to discover the amount of light pollution which is present in different locations around the world!")
    st.markdown(
        "You can find the source code in the [Light Pollution Network GitHub Repository](https://github.com/Vaserium/Light-Pollution-Network/blob/main/app.py)")

####################
# Making Dataframe And
# Loading it Into Website
####################

# ------------------------------------------------- Displaying all data (just for show and will not actually use data from this)
excel_file = 'Data1.csv'
excel_file2 = 'Data2.csv'

dataToDisplay = pd.read_csv(excel_file)

dataToDisplay2 = pd.read_csv(excel_file2, error_bad_lines=False)
dataToDisplay2.dropna(subset=['Brightness'], inplace=True)

if st.checkbox('Show raw data'):
    st.write(dataToDisplay)
    if st.checkbox('Show more data'):
        st.write(dataToDisplay2)
# ------------------------------------------------- Organizing data into lists that consists of columns (exp: One column can be 'Latitude' with all of it's data in that list)
data = pd.read_csv(excel_file)
data.dropna(subset=['Brightness'], inplace=True)
lat = pd.DataFrame(data, columns=['Latitude'])
lon = pd.DataFrame(data, columns=['Longitude'])
brightness = pd.DataFrame(data, columns=['Brightness'])

data2 = pd.read_csv(excel_file2)
data2.dropna(subset=['Brightness'], inplace=True)
lat2 = pd.DataFrame(data2, columns=['Latitude'])
lon2 = pd.DataFrame(data2, columns=['Longitude'])
brightness2 = pd.DataFrame(data2, columns=['Brightness'])

# ---------------------------------------------------------------------------------------------------------------------------  Selections for Units, Location, ect......
st.header("Enter the name of City and Select Light Pollution Unit")
with st.form("my_form"):
    place = st.text_input("Location", "")
    # unit = form.selectbox(" SELECT LIGHT POLLUTION UNIT", ("All Units", "SQM", "Bortle"))
    submit = st.form_submit_button(label="Submit")

# --------------------------------------------------------------------------------------------------------------------------- Geocoding API Ready to use with Database
url = "https://forward-reverse-geocoding.p.rapidapi.com/v1/search"

querystring = {
    "q": place,
    "accept-language": "en", "polygon_threshold": "0.0"}

headers = {
    'x-rapidapi-host': "forward-reverse-geocoding.p.rapidapi.com",
    'x-rapidapi-key': "adbf836d5cmshb143032a7b5980ep1f1771jsnc43f9ba58fe2"
}

response = requests.request("GET", url, headers=headers, params=querystring)
# --------------------------------------------------------------------------------------------------------------------------- 1)Pressing Submit button,  2)Prints number

count = 0


def lat_difference(api, excel):
    # Max difference is 1.9
    dif = api - excel
    return dif


def lon_difference(api, excel):
    # Max difference is 1.9
    dif = api - excel
    return dif


def lat_is_between(a, x, b):
    return min(a, b) < x < max(a, b)


def lon_is_between(a, x, b):
    return min(a, b) < x < max(a, b)


def bortle_scale(val):
    bortle_class = 0
    if val > 21.90:
        bortle_class = 1
    elif 21.50 < val < 21.90:
        bortle_class = 2
    elif 21.50 < val < 21.90:
        bortle_class = 2
    elif 21.30 < val < 21.50:
        bortle_class = 3
    elif 20.80 < val < 21.30:
        bortle_class = 4
    elif 20.10 < val < 20.80:
        bortle_class = 4.5
    elif 19.10 < val < 21.10:
        bortle_class = 5
    elif 18.00 < val < 18.55:
        bortle_class = 6
    elif 18.55 < val < 19.10:
        bortle_class = 7
    elif val < 18.00:
        bortle_class = 8
    elif val < 18.00:
        bortle_class = 9
    return bortle_class


def bortle_description(bortle_scale):
    if bortle_scale == 1:
        st.markdown("<h1 style='text-align: center; color: Tomato;'>Excellent, truly dark-skies</h1>",
                    unsafe_allow_html=True)
    elif bortle_scale == 2:
        st.markdown("<h1 style='text-align: center; color: Tomato;'>Typical, truly dark skies</h1>",
                    unsafe_allow_html=True)
    elif bortle_scale == 3:
        st.markdown("<h1 style='text-align: center; color: Tomato;'>Rural Sky</h1>",
                    unsafe_allow_html=True)
    elif bortle_scale == 4:
        st.markdown("<h1 style='text-align: center; color: Tomato;'>Rural/Suburban transition</h1>",
                    unsafe_allow_html=True)
    elif bortle_scale == 5:
        st.markdown("<h1 style='text-align: center; color: Tomato;'>Suburban sky</h1>",
                    unsafe_allow_html=True)
    elif bortle_scale == 6 or bortle_scale == 7:
        st.markdown("<h1 style='text-align: center; color: Tomato;'>Bright, suburban sky</h1>",
                    unsafe_allow_html=True)
    elif bortle_scale == 8 or bortle_scale == 9:
        st.markdown("<h1 style='text-align: center; color: Tomato;'>City sky</h1>",
                    unsafe_allow_html=True)


def detailed_bortle_description(bortle_scale):
    if bortle_scale == 1:
        column1, column2, column3 = st.columns((1.5, 1, 1))
        column3.subheader("- Milky Way is visible with great detail")
        column3.subheader("- M33 (Pinwheel Galaxy) is very bright")
        column3.subheader("- Zodiacal lights visible")
        column3.subheader("- Airglow is obvious near the clouds and the horizon")
        column3.subheader("- Encompassing area is very dark")
        image = Image.open('Bortle_Class.png')
        column1.image(image, caption='Credit: OPT Telescopes', width=940)
    elif bortle_scale == 2:
        column1, column2, column3 = st.columns((1.5, 1, 1))
        column3.subheader("- Summer Milky Way is visible with great detail")
        column3.subheader("- M33(Pinwheel Galaxy) and other globular clusters are visible through direct vision")
        column3.subheader("- Zodiacal lights are bright, this causes feeble shadows after dark")
        column3.subheader("- Clouds appear as dark irregular balls")
        column3.subheader("- Ground is almost entirely dark")
        image = Image.open('Bortle_Class.png')
        column1.image(image, caption='Credit: OPT Telescopes', width=940)
    elif bortle_scale == 3:
        column1, column2, column3 = st.columns((1.5, 1, 1))
        column3.subheader("- Milky Way is visible with an outlined appearance")
        column3.subheader("- M31(Andromeda Galaxy) is visible, and other globular clusters are noticeable")
        column3.subheader("- Zodiacal lights are very bright during Spring and Autumn")
        column3.subheader("- Clouds aren't bright, and airglow is not visible")
        column3.subheader("- Ground is faintly bright")
        image = Image.open('Bortle_Class.png')
        column1.image(image, caption='Credit: OPT Telescopes', width=940)
    elif bortle_scale == 4:
        column1, column2, column3 = st.columns((1.5, 1, 1))
        column3.subheader(
            "- Milky Way is faint with most of it's details lost, but the structure is visible above the horizon")
        column3.subheader("- M31(Andromeda Galaxy) is still pretty visible")
        column3.subheader("- Clouds are illuminated but they appear very faint at the zenith")
        column3.subheader("- Sky is brighter than the land")
        image = Image.open('Bortle_Class.png')
        column1.image(image, caption='Credit: OPT Telescopes', width=940)
    elif bortle_scale == 5:
        column1, column2, column3 = st.columns((1.5, 1, 1))
        column3.subheader("- Milky Way is extremely faint, and is completely lost alongside the horizon")
        column3.subheader(
            "- Outline of M31(Andromeda Galaxy) and the radiance of the Orion Nebula are distinguishable")
        column3.subheader("- Zodiacal lights are pretty faint during Spring and Autumn")
        column3.subheader("- Clouds are brighter than the sky")
        column3.subheader("- Ground objects seem partially lit")
        image = Image.open('Bortle_Class.png')
        column1.image(image, caption='Credit: OPT Telescopes', width=940)
    elif bortle_scale == 6 or bortle_scale == 7:
        column1, column2, column3 = st.columns((1.5, 1, 1))
        column3.subheader(
            "- Milky Way seems partially visible overhead, certain chunks aren't visible due to light pollution. Or it is invisible")
        column3.subheader(
            "- Outline of M31(Andromeda Galaxy) and the radiance of the Orion Nebula are distinguishablen, and the Beehive Cluster is barely visible")
        column3.subheader("- Only the brightest constellations remain visible")
        column3.subheader("- Clouds are incredibly lit")
        column3.subheader("- Ground objects are lit evenly")
        image = Image.open('Bortle_Class.png')
        column1.image(image, caption='Credit: OPT Telescopes', width=940)
    elif bortle_scale == 8 or bortle_scale == 9:
        column1, column2, column3 = st.columns((1.5, 1, 1))
        column3.subheader("- Milky Way is 100% invisible")
        column3.subheader("- Plelades Cluster is visible, and some other faint objects are visible")
        column3.subheader("- Dimmest constellations are missing key stars")
        column3.subheader("- Clouds are incredibly lit")
        column3.subheader("- The sky has a somewhat orange glow and is so bright that it can be seen at night")
        image = Image.open('Bortle_Class.png')
        column1.image(image, caption='Credit: OPT Telescopes', width=940)


if submit:
    if len(response.json()) == 0:
        st.error("Your location is invalid")
    else:
        data_geocode = response.json()
        lon_geocode = data_geocode[0]['lon']
        lat_geocode = data_geocode[0]['lat']
        index = []
        index2 = []
        howManyMatched = 0
        howManyMatched2 = 0
        brightness_values = []
        brightness_values2 = []

        for i in range(len(data)):
            if lat_is_between(-1, lat_difference(float(lat_geocode), float(lat.iloc[i])), 1):
                index.append(i)

        for i in range(len(data2)):
            if lat_is_between(-1, lat_difference(float(lat_geocode), float(lat2.iloc[i])), 1):
                index2.append(i)

        for i in range(len(index)):
            if lon_is_between(-1, lon_difference(float(lon_geocode), float(lon.iloc[i])), 1):
                howManyMatched = howManyMatched + 1
                brightness_values.append(brightness.iloc[i])

        for i in range(len(index2)):
            if lon_is_between(-1, lon_difference(float(lon_geocode), float(lon2.iloc[i])), 1):
                howManyMatched2 = howManyMatched2 + 1
                brightness_values2.append(brightness2.iloc[i])

        # -------------------------------------- Create if statements to avoid tumbling into the divided by zero
        average_brightness = 0
        average_brightness2 = 0
        if len(brightness_values) > 0:
            average_brightness = float(sum(brightness_values) / len(brightness_values))
        if len(brightness_values2) > 0:
            average_brightness2 = float(sum(brightness_values2) / len(brightness_values2))

        if howManyMatched == 0 and howManyMatched2 == 0:
            st.error("Sorry about that, we don't have any brightness values that correspond to your location")
        elif howManyMatched == 0:
            brightness = str(round(average_brightness2, 2))
            bortle = str(bortle_scale(float(average_brightness2)))
            bortle_description(int(bortle))
            c1, c2, c3, c4 = st.columns((0.6, 2.1, 0.8, 1))
            c2.header("Brightness: " + brightness + " mag/arcsec^2")
            c3.header("Bortle Scale: " + bortle, )
            detailed_bortle_description(int(bortle))

        elif howManyMatched2 == 0:
            brightness = str(round(average_brightness, 2))
            bortle = str(bortle_scale(float(average_brightness)))
            bortle_description(int(bortle))
            c1, c2, c3, c4 = st.columns((0.6, 2.1, 0.8, 1))
            c2.header("Brightness: " + brightness + " mag/arcsec^2")
            c3.header("Bortle Scale: " + bortle)
            detailed_bortle_description(int(bortle))

        else:
            tot_avg = (average_brightness + average_brightness2) / 2
            brightness = str(round(tot_avg, 2))
            bortle = str(bortle_scale(float(tot_avg)))
            bortle_description(int(bortle))
            c1, c2, c3, c4 = st.columns((0.6, 2.1, 0.8, 1))
            c2.header("Brightness: " + brightness + " mag/arcsec^2")
            c3.header("Bortle Scale: " + bortle)
            detailed_bortle_description(int(bortle))
