import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="SalesVision USA", layout="wide")

# ---------- PALETTE DE COULEURS COHÉRENTE ----------
COLOR_SEQUENCE = ["#1f77b4", "#4a90d9", "#7fb3e0", "#0d3c61", "#a8cce8", "#2c5f8a"]

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

# Traduction des statuts de commande en libellés lisibles
STATUS_NAMES = {
    'received': 'Reçue',
    'complete': 'Complétée',
    'order_refunded': 'Remboursée',
    'canceled': 'Annulée',
    'refund': 'Remboursement',
    'cod': 'Paiement à la livraison',
    'paid': 'Payée',
    'processing': 'En traitement',
    'closed': 'Clôturée',
    'pending': 'En attente',
    'pending_paypal': 'En attente (PayPal)',
    'payment_review': 'Vérification du paiement',
    'holded': 'En attente de validation'
}

STATUTS_ANNULATION = ['Annulée', 'Remboursée', 'Remboursement']


@st.cache_data
def load_data():
    df = pd.read_csv("dataset/donnees_ventes_etudiants.csv", low_memory=False)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['State Complet'] = df['State'].map(STATE_NAMES)
    df['Country'] = 'USA'
    df['Latitude'] = df['State'].map(lambda x: STATE_COORDS.get(x, (None, None))[0])
    df['Longitude'] = df['State'].map(lambda x: STATE_COORDS.get(x, (None, None))[1])
    df['Statut'] = df['status'].map(STATUS_NAMES).fillna(df['status'])
    return df


with st.spinner("Chargement des données..."):
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


# Callback de réinitialisation : remet chaque filtre à sa valeur par défaut
# AVANT que les widgets ne soient redessinés (méthode fiable recommandée par Streamlit)
def reset_filters():
    st.session_state["filter_date"] = (min_date, max_date)
    st.session_state["filter_region"] = []
    st.session_state["filter_state"] = []
    st.session_state["filter_country"] = []
    st.session_state["filter_city"] = []
    st.session_state["filter_status"] = []


st.sidebar.button(
    "🔄 Réinitialiser tous les filtres",
    use_container_width=True,
    type="primary",
    on_click=reset_filters
)

st.sidebar.markdown("---")

date_range = st.sidebar.date_input(
    "Période",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="filter_date"
)

regions = sorted(df['Region'].unique())
selected_regions = st.sidebar.multiselect("Région", regions, key="filter_region")

df_temp = df[df['Region'].isin(selected_regions)] if selected_regions else df

states = sorted(df_temp['State Complet'].unique())
selected_states = st.sidebar.multiselect("State", states, key="filter_state")

df_temp2 = df_temp[df_temp['State Complet'].isin(selected_states)] if selected_states else df_temp

countries = sorted(df_temp2['Country'].unique())
selected_countries = st.sidebar.multiselect("Country", countries, key="filter_country")

df_temp3 = df_temp2[df_temp2['Country'].isin(selected_countries)] if selected_countries else df_temp2

cities = sorted(df_temp3['City'].unique())
selected_cities = st.sidebar.multiselect("City", cities, key="filter_city")

statuts = sorted(df['Statut'].unique())
selected_statuts = st.sidebar.multiselect("Statut de la commande", statuts, key="filter_status")


# ---------- FONCTION DE FILTRAGE (réutilisable pour la comparaison de période) ----------
def apply_filters(base_df, start=None, end=None):
    d = base_df
    if start is not None and end is not None:
        d = d[(d['order_date'] >= pd.to_datetime(start)) & (d['order_date'] <= pd.to_datetime(end))]
    if selected_regions:
        d = d[d['Region'].isin(selected_regions)]
    if selected_states:
        d = d[d['State Complet'].isin(selected_states)]
    if selected_countries:
        d = d[d['Country'].isin(selected_countries)]
    if selected_cities:
        d = d[d['City'].isin(selected_cities)]
    if selected_statuts:
        d = d[d['Statut'].isin(selected_statuts)]
    return d


has_period = len(date_range) == 2

if has_period:
    df_filtered = apply_filters(df, date_range[0], date_range[1])
else:
    df_filtered = apply_filters(df)

# ---------- MESSAGE SI AUCUNE DONNÉE ----------
if df_filtered.empty:
    st.warning("⚠️ Aucune donnée ne correspond à cette combinaison de filtres. Essayez d'élargir votre sélection ou cliquez sur 'Réinitialiser tous les filtres'.")
    st.stop()

# ---------- CALCUL DE LA PÉRIODE PRÉCÉDENTE (pour comparaison) ----------
delta_ventes = None
delta_commandes = None
delta_clients = None

if has_period:
    start, end = date_range
    period_days = (end - start).days + 1
    prev_end = start - pd.Timedelta(days=1)
    prev_start = prev_end - pd.Timedelta(days=period_days - 1)
    df_prev = apply_filters(df, prev_start, prev_end)

    if not df_prev.empty:
        prev_total = df_prev['total'].sum()
        prev_clients = df_prev['cust_id'].nunique()
        prev_commandes = df_prev['order_id'].nunique()

        curr_total = df_filtered['total'].sum()
        curr_clients = df_filtered['cust_id'].nunique()
        curr_commandes = df_filtered['order_id'].nunique()

        if prev_total > 0:
            delta_ventes = f"{((curr_total - prev_total) / prev_total) * 100:+.1f}% vs période précédente"
        if prev_clients > 0:
            delta_clients = f"{((curr_clients - prev_clients) / prev_clients) * 100:+.1f}% vs période précédente"
        if prev_commandes > 0:
            delta_commandes = f"{((curr_commandes - prev_commandes) / prev_commandes) * 100:+.1f}% vs période précédente"

# ---------- BOUTON D'EXPORT CSV ----------
csv_data = df_filtered.to_csv(index=False).encode('utf-8')
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="⬇️ Exporter les données filtrées (CSV)",
    data=csv_data,
    file_name="ventes_filtrees.csv",
    mime="text/csv",
    use_container_width=True
)

# ---------- ONGLETS ----------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🏠 Vue d'ensemble", "👥 Clients", "📈 Ventes détaillées", "🗺️ Carte"]
)

# ===================== TAB 1 : VUE D'ENSEMBLE =====================
with tab1:
    st.subheader("Indicateurs clés")

    total_ventes = df_filtered['total'].sum()
    nb_clients = df_filtered['cust_id'].nunique()
    nb_commandes = df_filtered['order_id'].nunique()
    panier_moyen = total_ventes / nb_commandes if nb_commandes > 0 else 0
    qte_totale = df_filtered['qty_ordered'].sum()
    nb_annulations = df_filtered[df_filtered['Statut'].isin(STATUTS_ANNULATION)]['order_id'].nunique()
    taux_annulation = (nb_annulations / nb_commandes * 100) if nb_commandes > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Nombre total de vente", f"${total_ventes:,.0f}", delta=delta_ventes)
    with col2:
        st.metric("👥 Nombre distinct de clients", f"{nb_clients:,}", delta=delta_clients)
    with col3:
        st.metric("📦 Nombre total de commande", f"{nb_commandes:,}", delta=delta_commandes)
    with col4:
        st.metric("🧺 Panier moyen", f"${panier_moyen:,.2f}")

    col5, col6 = st.columns(2)
    with col5:
        st.metric("📦 Quantité totale d'articles vendus", f"{qte_totale:,.0f}")
    with col6:
        st.metric("↩️ Taux d'annulation / remboursement", f"{taux_annulation:.1f}%")

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
            title="Nombre total de vente par Catégorie",
            color_discrete_sequence=COLOR_SEQUENCE
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        top_cat = ventes_categorie.iloc[0]
        pct_cat = (top_cat['total'] / total_ventes) * 100
        st.info(f"💡 La catégorie **{top_cat['category']}** est la plus vendue, représentant **{pct_cat:.1f}%** des ventes totales.")

    with col2:
        ventes_region = df_filtered.groupby('Region')['total'].sum().reset_index()
        fig_pie = px.pie(
            ventes_region,
            names='Region',
            values='total',
            title="Pourcentage du nombre total de vente par Région",
            color_discrete_sequence=COLOR_SEQUENCE
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        top_region = ventes_region.sort_values('total', ascending=False).iloc[0]
        pct_region = (top_region['total'] / total_ventes) * 100
        st.info(f"💡 La région **{top_region['Region']}** génère **{pct_region:.1f}%** du chiffre d'affaires.")

    st.markdown("---")
    st.subheader("Répartition par mode de paiement")

    paiement_counts = df_filtered.groupby('payment_method')['order_id'].nunique().reset_index()
    paiement_counts.columns = ['Mode de paiement', 'Nombre de commandes']
    paiement_counts = paiement_counts.sort_values('Nombre de commandes', ascending=False)

    fig_paiement = px.bar(
        paiement_counts,
        x='Mode de paiement',
        y='Nombre de commandes',
        title="Nombre de commandes par mode de paiement",
        color_discrete_sequence=COLOR_SEQUENCE
    )
    st.plotly_chart(fig_paiement, use_container_width=True)

    top_paiement = paiement_counts.iloc[0]
    st.info(f"💡 Le mode de paiement le plus utilisé est **{top_paiement['Mode de paiement']}** ({top_paiement['Nombre de commandes']:,} commandes).")

    st.markdown("---")
    with st.expander("🔍 Voir un extrait des données filtrées"):
        st.dataframe(df_filtered.head(20))

# ===================== TAB 2 : CLIENTS =====================
with tab2:
    st.subheader("Top 10 des meilleurs clients (par montant)")

    top_clients = df_filtered.groupby('full_name')['total'].sum().reset_index()
    top_clients = top_clients.sort_values('total', ascending=False).head(10)

    fig_top10 = px.bar(
        top_clients.sort_values('total'),
        x='total',
        y='full_name',
        orientation='h',
        title="Top 10 des meilleurs clients (par nombre total de vente)",
        color_discrete_sequence=COLOR_SEQUENCE
    )
    st.plotly_chart(fig_top10, use_container_width=True)

    best_client = top_clients.iloc[0]
    st.info(f"💡 **{best_client['full_name']}** est votre meilleur client, avec **${best_client['total']:,.0f}** d'achats cumulés.")

    st.markdown("---")
    st.subheader("Top 10 des clients les plus fidèles (par nombre de commandes)")

    fidelite = df_filtered.groupby('full_name')['order_id'].nunique().reset_index()
    fidelite.columns = ['full_name', 'nb_commandes']
    fidelite = fidelite.sort_values('nb_commandes', ascending=False).head(10)

    fig_fidelite = px.bar(
        fidelite.sort_values('nb_commandes'),
        x='nb_commandes',
        y='full_name',
        orientation='h',
        title="Top 10 des clients les plus fidèles (nombre de commandes)",
        color_discrete_sequence=[COLOR_SEQUENCE[2]]
    )
    st.plotly_chart(fig_fidelite, use_container_width=True)

    most_loyal = fidelite.iloc[0]
    st.info(f"💡 **{most_loyal['full_name']}** est votre client le plus fidèle, avec **{most_loyal['nb_commandes']}** commandes passées.")

    st.markdown("---")
    st.subheader("Répartition des clients par âge et par genre")

    col1, col2 = st.columns(2)

    with col1:
        fig_age = px.histogram(
            df_filtered,
            x='age',
            nbins=20,
            title="Répartition de l'âge des clients",
            color_discrete_sequence=[COLOR_SEQUENCE[0]]
        )
        st.plotly_chart(fig_age, use_container_width=True)

        age_moyen = df_filtered['age'].mean()
        st.info(f"💡 L'âge moyen des clients est de **{age_moyen:.0f} ans**.")

    with col2:
        gender_counts = df_filtered['Gender'].value_counts(normalize=True).reset_index()
        gender_counts.columns = ['Gender', 'Pourcentage']
        gender_counts['Pourcentage'] = gender_counts['Pourcentage'] * 100

        fig_gender = px.bar(
            gender_counts,
            x='Gender',
            y='Pourcentage',
            text=gender_counts['Pourcentage'].round(1).astype(str) + '%',
            title="Répartition Hommes / Femmes (%)",
            color='Gender',
            color_discrete_sequence=COLOR_SEQUENCE
        )
        st.plotly_chart(fig_gender, use_container_width=True)

        top_gender = gender_counts.sort_values('Pourcentage', ascending=False).iloc[0]
        st.info(f"💡 La clientèle est majoritairement composée de **{top_gender['Gender']}** ({top_gender['Pourcentage']:.1f}%).")

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
        title="Nombre total de vente par mois",
        color_discrete_sequence=COLOR_SEQUENCE
    )
    fig_line.update_xaxes(title="Année-Mois")
    fig_line.update_yaxes(title="Total des ventes")
    st.plotly_chart(fig_line, use_container_width=True)

    if len(ventes_mensuelles) > 0:
        best_month = ventes_mensuelles.sort_values('total', ascending=False).iloc[0]
        st.info(f"💡 Le meilleur mois est **{best_month['annee_mois']}** avec **${best_month['total']:,.0f}** de ventes.")

    st.markdown("---")
    st.subheader("🔮 Prévision des ventes (3 prochains mois)")

    ts = ventes_mensuelles.set_index('annee_mois')['total']
    ts.index = pd.PeriodIndex(ts.index, freq='M').to_timestamp()
    n_periods = len(ts)

    if n_periods >= 4:
        try:
            if n_periods >= 24:
                model = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=12)
            else:
                model = ExponentialSmoothing(ts, trend='add', seasonal=None)
            fit = model.fit()
            forecast = fit.forecast(3)

            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(
                x=ts.index, y=ts.values,
                mode='lines+markers', name='Ventes réelles',
                line=dict(color=COLOR_SEQUENCE[0])
            ))
            forecast_x = [ts.index[-1]] + list(forecast.index)
            forecast_y = [ts.values[-1]] + list(forecast.values)
            fig_forecast.add_trace(go.Scatter(
                x=forecast_x, y=forecast_y,
                mode='lines+markers', name='Prévision (3 mois)',
                line=dict(color='#d62728', dash='dash')
            ))
            fig_forecast.update_layout(
                title="Prévision des ventes pour les 3 prochains mois (méthode Holt-Winters)",
                xaxis_title="Mois",
                yaxis_title="Total des ventes"
            )
            st.plotly_chart(fig_forecast, use_container_width=True)

            st.info(f"💡 Prévision : les ventes du mois prochain sont estimées à environ **${forecast.iloc[0]:,.0f}**.")
        except Exception:
            st.warning("⚠️ Impossible de générer une prévision fiable avec les données actuelles (série trop courte ou irrégulière).")
    else:
        st.info("Pas assez de mois de données pour générer une prévision fiable (minimum 4 mois recommandé). Élargissez la période sélectionnée.")

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
        color_continuous_scale='Blues',
        title="Nombre total de vente par State"
    )
    fig_map.update_layout(mapbox_style=map_style)
    fig_map.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_map, use_container_width=True)

    if len(ventes_state) > 0:
        top_state = ventes_state.sort_values('total', ascending=False).iloc[0]
        st.info(f"💡 Le State qui génère le plus de ventes est **{top_state['State Complet']}** avec **${top_state['total']:,.0f}**.")