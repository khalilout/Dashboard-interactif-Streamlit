import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SalesVision USA", layout="wide")

STATE_NAMES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
    'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
    'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
    'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska',
    'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
    'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
    'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

STATE_COORDS = {
    'AL': (32.806671, -86.791130), 'AK': (61.370716, -152.404419), 'AZ': (33.729759, -111.431221),
    'AR': (34.969704, -92.373123), 'CA': (36.116203, -119.681564), 'CO': (39.059811, -105.311104),
    'CT': (41.597782, -72.755371), 'DE': (39.318523, -75.507141), 'DC': (38.897438, -77.026817),
    'FL': (27.766279, -81.686783), 'GA': (33.040619, -83.643074), 'HI': (21.094318, -157.498337),
    'ID': (44.240459, -114.478828), 'IL': (40.349457, -88.986137), 'IN': (39.849426, -86.258278),
    'IA': (42.011539, -93.210526), 'KS': (38.526600, -96.726486), 'KY': (37.668140, -84.670067),
    'LA': (31.169546, -91.867805), 'ME': (44.693947, -69.381927), 'MD': (39.063946, -76.802101),
    'MA': (42.230171, -71.530106), 'MI': (43.326618, -84.536095), 'MN': (45.694454, -93.900192),
    'MS': (32.741646, -89.678696), 'MO': (38.456085, -92.288368), 'MT': (46.921925, -110.454353),
    'NE': (41.125370, -98.268082), 'NV': (38.313515, -117.055374), 'NH': (43.452492, -71.563896),
    'NJ': (40.298904, -74.521011), 'NM': (34.840515, -106.248482), 'NY': (42.165726, -74.948051),
    'NC': (35.630066, -79.806419), 'ND': (47.528912, -99.784012), 'OH': (40.388783, -82.764915),
    'OK': (35.565342, -96.928917), 'OR': (44.572021, -122.070938), 'PA': (40.590752, -77.209755),
    'RI': (41.680893, -71.511780), 'SC': (33.856892, -80.945007), 'SD': (44.299782, -99.438828),
    'TN': (35.747845, -86.692345), 'TX': (31.054487, -97.563461), 'UT': (40.150032, -111.862434),
    'VT': (44.045876, -72.710686), 'VA': (37.769337, -78.169968), 'WA': (47.400902, -121.490494),
    'WV': (38.491226, -80.954453), 'WI': (44.268543, -89.616508), 'WY': (42.755966, -107.302490)
}


@st.cache_data
def load_data():
    df = pd.read_csv("dataset/donnees_ventes_etudiants.csv", low_memory=False)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['State Complet'] = df['State'].map(STATE_NAMES)
    df['Country'] = 'USA'
    df['Latitude'] = df['State'].map(lambda x: STATE_COORDS.get(x, (None, None))[0])
    df['Longitude'] = df['State'].map(lambda x: STATE_COORDS.get(x, (None, None))[1])
    return df


df = load_data()

# ---------- EN-TÊTE ----------
st.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='color: #1f77b4; margin-bottom: 0;'>📊 SalesVision USA</h1>
        <p style='color: gray; font-size: 16px;'>Dashboard de pilotage des ventes — Solution développée pour votre entreprise</p>
    </div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR : FILTRES ----------
st.sidebar.header("Filtres")

min_date = df['order_date'].min()
max_date = df['order_date'].max()
date_range = st.sidebar.date_input(
    "Période",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

regions = sorted(df['Region'].unique())
selected_regions = st.sidebar.multiselect("Région", regions, default=[])

df_temp = df[df['Region'].isin(selected_regions)] if selected_regions else df

states = sorted(df_temp['State Complet'].unique())
selected_states = st.sidebar.multiselect("State", states, default=[])

df_temp2 = df_temp[df_temp['State Complet'].isin(selected_states)] if selected_states else df_temp

countries = sorted(df_temp2['Country'].unique())
selected_countries = st.sidebar.multiselect("Country", countries, default=[])

df_temp3 = df_temp2[df_temp2['Country'].isin(selected_countries)] if selected_countries else df_temp2

cities = sorted(df_temp3['City'].unique())
selected_cities = st.sidebar.multiselect("City", cities, default=[])

statuses = sorted(df['status'].unique())
selected_statuses = st.sidebar.multiselect("Statut de la commande", statuses, default=[])

# ---------- APPLICATION DE TOUS LES FILTRES ----------
df_filtered = df.copy()

if len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered['order_date'] >= pd.to_datetime(date_range[0])) &
        (df_filtered['order_date'] <= pd.to_datetime(date_range[1]))
    ]
if selected_regions:
    df_filtered = df_filtered[df_filtered['Region'].isin(selected_regions)]
if selected_states:
    df_filtered = df_filtered[df_filtered['State Complet'].isin(selected_states)]
if selected_countries:
    df_filtered = df_filtered[df_filtered['Country'].isin(selected_countries)]
if selected_cities:
    df_filtered = df_filtered[df_filtered['City'].isin(selected_cities)]
if selected_statuses:
    df_filtered = df_filtered[df_filtered['status'].isin(selected_statuses)]

# ---------- ONGLETS ----------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🏠 Vue d'ensemble", "👥 Clients", "📈 Ventes détaillées", "🗺️ Carte"]
)

# ===================== TAB 1 : VUE D'ENSEMBLE =====================
with tab1:
    st.subheader("Indicateurs clés")

    col1, col2, col3 = st.columns(3)

    with col1:
        total_ventes = df_filtered['total'].sum()
        st.metric("💰 Nombre total de vente", f"{total_ventes:,.0f}")

    with col2:
        nb_clients = df_filtered['cust_id'].nunique()
        st.metric("👥 Nombre distinct de clients", f"{nb_clients:,}")

    with col3:
        nb_commandes = df_filtered['order_id'].nunique()
        st.metric("📦 Nombre total de commande", f"{nb_commandes:,}")

    st.markdown("---")
    st.subheader("Ventes par catégorie et par région")

    col1, col2 = st.columns(2)

    with col1:
        ventes_categorie = df_filtered.groupby('category')['total'].sum().reset_index()
        ventes_categorie = ventes_categorie.sort_values('total', ascending=False)
        fig_bar = px.bar(
            ventes_categorie,
            x='category',
            y='total',
            title="Nombre total de vente par Catégorie"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        ventes_region = df_filtered.groupby('Region')['total'].sum().reset_index()
        fig_pie = px.pie(
            ventes_region,
            names='Region',
            values='total',
            title="Pourcentage du nombre total de vente par Région"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    with st.expander("🔍 Voir un extrait des données filtrées"):
        st.dataframe(df_filtered.head(20))

# ===================== TAB 2 : CLIENTS =====================
with tab2:
    st.subheader("Top 10 des meilleurs clients")

    top_clients = df_filtered.groupby('full_name')['total'].sum().reset_index()
    top_clients = top_clients.sort_values('total', ascending=False).head(10)

    fig_top10 = px.bar(
        top_clients.sort_values('total'),
        x='total',
        y='full_name',
        orientation='h',
        title="Top 10 des meilleurs clients (par nombre total de vente)"
    )
    st.plotly_chart(fig_top10, use_container_width=True)

    st.markdown("---")
    st.subheader("Répartition des clients par âge et par genre")

    col1, col2 = st.columns(2)

    with col1:
        fig_age = px.histogram(
            df_filtered,
            x='age',
            nbins=20,
            title="Répartition de l'âge des clients"
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col2:
        gender_counts = df_filtered['Gender'].value_counts(normalize=True).reset_index()
        gender_counts.columns = ['Gender', 'Pourcentage']
        gender_counts['Pourcentage'] = gender_counts['Pourcentage'] * 100

        fig_gender = px.bar(
            gender_counts,
            x='Gender',
            y='Pourcentage',
            text=gender_counts['Pourcentage'].round(1).astype(str) + '%',
            title="Répartition Hommes / Femmes (%)"
        )
        st.plotly_chart(fig_gender, use_container_width=True)

# ===================== TAB 3 : VENTES DÉTAILLÉES =====================
with tab3:
    st.subheader("Évolution du nombre total de vente par mois")

    df_filtered['annee_mois'] = df_filtered['order_date'].dt.to_period('M').astype(str)

    ventes_mensuelles = df_filtered.groupby('annee_mois')['total'].sum().reset_index()
    ventes_mensuelles = ventes_mensuelles.sort_values('annee_mois')

    fig_line = px.line(
        ventes_mensuelles,
        x='annee_mois',
        y='total',
        markers=True,
        title="Nombre total de vente par mois"
    )
    fig_line.update_xaxes(title="Année-Mois")
    fig_line.update_yaxes(title="Total des ventes")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    st.subheader("Données détaillées")
    st.dataframe(df_filtered.head(50))

# ===================== TAB 4 : CARTE =====================
with tab4:
    st.subheader("🗺️ Carte des ventes par State")

    map_style = st.selectbox(
        "Style de carte",
        ["open-street-map", "carto-positron", "carto-darkmatter"],
        index=0
    )

    ventes_state = df_filtered.groupby(
        ['State', 'State Complet', 'Latitude', 'Longitude']
    )['total'].sum().reset_index()

    fig_map = px.scatter_mapbox(
        ventes_state,
        lat='Latitude',
        lon='Longitude',
        size='total',
        color='total',
        hover_name='State Complet',
        hover_data={'total': True, 'Latitude': False, 'Longitude': False},
        zoom=3,
        center={"lat": 39.8, "lon": -98.5},
        height=600,
        color_continuous_scale='Reds',
        title="Nombre total de vente par State"
    )
    fig_map.update_layout(mapbox_style=map_style)
    fig_map.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_map, use_container_width=True)