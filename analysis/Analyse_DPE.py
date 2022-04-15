#region import et initialisation
import pandas as pd
import string
from analysis.functions_Analyse_DPE import *
import plotly
import plotly.express as px

data_folder ="data/"
dpe_class_list = list(string.ascii_uppercase[:7])
dpe_colors = ['#009900', '#33cc33', '#B3FF00', '#e6e600', '#FFB300', '#FF4D00', '#FF0000']
geo_code_columns = ['district', 'city_code', 'city', 'department', 'region']

pd.options.display.width = 0
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
#endregion

data = pd.read_csv(data_folder+'base_logement_complete.csv',
                   dtype={geo_code: str for geo_code in geo_code_columns})
data.head()
data_primary = data.loc[data.occupancy_type.isin(['primary residence'])]
energy_class_count = data_primary.groupby('energy_class', as_index=False)['IPONDL'].sum()

#region simple histogram
fig = px.bar(data_primary.groupby('energy_class', as_index=False)['IPONDL'].sum(),
             x='energy_class', y='IPONDL', color="energy_class",
                color_discrete_sequence=dpe_colors,
                labels={
                  "energy_class": "Classe énergétique",
                  "IPONDL": "Nombre de logements"}
)
#fig.update_traces(marker_color=dpe_colors)
plotly.offline.plot(fig, filename='tmp.html')
#endregion

fig=marimekko(data_primary.groupby(['energy_class',"construction_year_class"], as_index=False)['IPONDL'].sum(),
                x_var_name = "construction_year_class",
                y_var_name= "energy_class",
                effectif_var_name='IPONDL',
              color_discrete_sequence=dpe_colors)
plotly.offline.plot(fig, filename='tmp.html')

ColorY_var_name = "energy_class"
horizontalX_var_name = "construction_year_class"
TextureX_var_name = "residential_type"

df = data_primary.groupby([ColorY_var_name,horizontalX_var_name,TextureX_var_name], as_index=False)['IPONDL'].sum()
fig = marimekko_2(df =df ,ColorY_var_name=ColorY_var_name,horizontalX_var_name=horizontalX_var_name,
            TextureX_var_name=TextureX_var_name,color_discrete_sequence=dpe_colors)
plotly.offline.plot(fig, filename='Etiquette_age_residential_type.html')

data_primary["living_area_class_simple"] = data_primary["living_area_class"]
data_primary.loc[data_primary["living_area_class_simple"].isin(['De 40 à 60 m²', 'De 30 à 40 m²', 'Moins de 30 m²']),"living_area_class_simple"]='moins de 60m2'
data_primary.loc[data_primary["living_area_class_simple"].isin(['De 60 à 80 m²','De 80 à 100 m²']),"living_area_class_simple"]='De 60 à 100 m²'
data_primary.loc[data_primary["living_area_class_simple"].isin(['De 100 à 120 m²', '120 m² ou plus']),"living_area_class_simple"]='100 m² ou plus'

data_primary["heating_system_simple"] = data_primary["heating_system"]
data_primary.loc[data_primary["heating_system_simple"].isin(['Autres','Chauffage urbain']),"heating_system_simple"]='Autres et Chauffage urbain'
data_primary.loc[data_primary["heating_system_simple"].isin(['Chaudière fioul','Chaudière - autres']),"heating_system_simple"]='Chaudière fioul-autre'
for TextureX_var_name in  ["heating_system_simple","living_area_class_simple","occupancy_status","residential_type"]:
    df = data_primary.groupby([ColorY_var_name,horizontalX_var_name,TextureX_var_name], as_index=False)['IPONDL'].sum()
    fig = marimekko_2(df =df ,ColorY_var_name=ColorY_var_name,horizontalX_var_name=horizontalX_var_name,
                TextureX_var_name=TextureX_var_name,color_discrete_sequence=dpe_colors)
    plotly.offline.plot(fig, filename='Etiquette_age_'+TextureX_var_name+'.html')

#region bazar
fig = px.bar(data_primary.groupby(['energy_class',"construction_year_class"], as_index=False)['IPONDL'].sum(),
             x='energy_class', y='IPONDL', color="energy_class",text="construction_year_class",
                color_discrete_sequence=dpe_colors,
                labels={
                "construction_year_class" : "année de construction",
                  "energy_class": "Classe énergétique",
                  "IPONDL": "Nombre de logements"}
)
plotly.offline.plot(fig, filename='tmp.html')

fig = px.bar(data_primary.groupby(['energy_class',"construction_year_class"], as_index=False)['IPONDL'].sum(),
             x='construction_year_class', y='IPONDL', color="energy_class",
                color_discrete_sequence=dpe_colors,
                labels={
                  "energy_class": "Classe énergétique",
                  "IPONDL": "Nombre de logements"}
)

plotly.offline.plot(fig, filename='tmp.html')

fig = px.line(data_primary.groupby('energy_class', as_index=False)['IPONDL'].sum(),
              x='energy_class', y='IPONDL', color="NbHours", hover_data=["Actualisation", "DureeVieMax",  "CAPEX","EcartTypePrixElec",  "AverageShift"],
                 facet_col="EcartTypePrixElec",facet_row="AverageShift",
                marker={'color': dpe_colors},
              labels={
                  "CoutTotal": "Coût [€/MWh]",
                  "CAPEX": "CAPEX [€/kW]"}
)
plotly.offline.plot(fig, filename='tmp.html')



energy_plot_max = 800.

px.histogram(x='energy_consumption',
             data=data_primary.loc[data_primary.energy_consumption <= energy_plot_max],
             hue='energy_class',
             ax=ax,
             binwidth=2.0,
             hue_order=dpe_class_list,
             multiple='stack',
             palette=dpe_colors,
             weights='IPONDL',
             linewidth=0)
ax.set_xlabel("Consommation d'énergie (en kWh/m²)")
ax.set_ylabel("Nombre de logements")
rename_legend(ax, 'Classe Energétique')
#endregion