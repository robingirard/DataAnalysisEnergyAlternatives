#region import et initialisation
import numpy as np
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

#region Marimekko
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

data_primary=Create_simplified_variables(data_primary)

ColorY_var_name = "energy_class"
horizontalX_var_name = "construction_year_class"
TextureX_var_name = "residential_type"
for TextureX_var_name in  ["heating_system_simple","living_area_class_simple","occupancy_status_simple","residential_type"]:
    df = data_primary.groupby([ColorY_var_name,horizontalX_var_name,TextureX_var_name], as_index=False)['IPONDL'].sum()
    fig = marimekko_2(df =df ,ColorY_var_name=ColorY_var_name,horizontalX_var_name=horizontalX_var_name,
                TextureX_var_name=TextureX_var_name,color_discrete_sequence=dpe_colors)
    plotly.offline.plot(fig, filename='Etiquette_age_'+TextureX_var_name+'.html')

ColorY_var_name = "energy_class"
horizontalX_var_name = "occupancy_status_simple"
TextureX_var_name = "heating_system_simple"
df = data_primary.groupby([ColorY_var_name,horizontalX_var_name,TextureX_var_name], as_index=False)['IPONDL'].sum()
fig = marimekko_2(df =df ,ColorY_var_name=ColorY_var_name,horizontalX_var_name=horizontalX_var_name,
            TextureX_var_name=TextureX_var_name,color_discrete_sequence=dpe_colors)
plotly.offline.plot(fig, filename='Etiquette_heating_system_'+TextureX_var_name+'.html')

ColorY_var_name = "energy_class"
horizontalX_var_name = "occupancy_status_simple"
TextureX_var_name = "living_area_class_simple"
df = data_primary.groupby([ColorY_var_name,horizontalX_var_name,TextureX_var_name], as_index=False)['IPONDL'].sum()
fig = marimekko_2(df =df ,ColorY_var_name=ColorY_var_name,horizontalX_var_name=horizontalX_var_name,
            TextureX_var_name=TextureX_var_name,color_discrete_sequence=dpe_colors)
plotly.offline.plot(fig, filename='Etiquette_heating_system_'+TextureX_var_name+'.html')

fig=marimekko(data_primary.groupby(['energy_class',"heating_system_simple"], as_index=False)['IPONDL'].sum(),
                x_var_name = "heating_system_simple",
                y_var_name= "energy_class",
                effectif_var_name='IPONDL',
              color_discrete_sequence=dpe_colors)
plotly.offline.plot(fig, filename='tmp.html')


ColorY_var_name = "heating_system_simple"
horizontalX_var_name = "energy_class"
TextureX_var_name="construction_year_class_simple";
df = data_primary.groupby([ColorY_var_name, horizontalX_var_name, TextureX_var_name], as_index=False)['IPONDL'].sum()
fig = marimekko_2(df=df, ColorY_var_name=ColorY_var_name, horizontalX_var_name=horizontalX_var_name,
                  TextureX_var_name=TextureX_var_name, color_discrete_sequence=dpe_colors)
plotly.offline.plot(fig, filename='Etiquette_age_' + TextureX_var_name + '.html')
#endregion

#region distribution conso et etiquette en énergie finale
energy_plot_max = 800
data_primary["energy_cuts"]=pd.cut(data_primary.energy_consumption,
                                   bins = np.arange(0,energy_plot_max,step=2.)).\
    map(lambda x:x.mid).astype("float")
indexes = data_primary.energy_consumption <= energy_plot_max
fig = px.bar(data_primary.loc[indexes,:].groupby(["energy_cuts","energy_class"], as_index=False)['IPONDL'].sum(),
                     x="energy_cuts", y='IPONDL',color="energy_class",
                color_discrete_sequence=dpe_colors,
             labels={
                 "energy_cuts": "Conso energetique",
                 "IPONDL": "Nombre de logements"}
             )
plotly.offline.plot(fig, filename='tmp.html')

data_primary.loc[:,"energy_consumption_final"]=data_primary.energy_consumption
data_primary.loc[data_primary["heating_system"].isin(['Chauffage électrique','Pompes à chaleur électricité']),"energy_consumption_final"]=data_primary.loc[data_primary["heating_system"].isin(['Chauffage électrique','Pompes à chaleur électricité']),"energy_consumption_final"]/2.55

data_primary.loc[:,"energy_class2"]=pd.cut(data_primary.energy_consumption_final,
                                   bins = [0,50,90,150,230,330,450,100000],labels=
                                   ["A","B","C","D","E","F","G"]).astype("str")

fig=marimekko(data_primary.groupby(['energy_class2',"heating_system_simple"], as_index=False)['IPONDL'].sum().dropna(),
                x_var_name = "heating_system_simple",
                y_var_name= "energy_class2",
                effectif_var_name='IPONDL',
              color_discrete_sequence=dpe_colors)
plotly.offline.plot(fig, filename='tmp.html')

ColorY_var_name = "energy_class2"
horizontalX_var_name = "construction_year_class"
TextureX_var_name="heating_system_simple";
df = data_primary.groupby([ColorY_var_name, horizontalX_var_name, TextureX_var_name], as_index=False)['IPONDL'].sum()
fig = marimekko_2(df=df, ColorY_var_name=ColorY_var_name, horizontalX_var_name=horizontalX_var_name,
                  TextureX_var_name=TextureX_var_name, color_discrete_sequence=dpe_colors)
plotly.offline.plot(fig, filename='Etiquette_finale_age_' + TextureX_var_name + '.html')
#endregion

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