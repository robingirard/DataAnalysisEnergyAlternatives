def rename_legend(ax, new_name):
    old_legend = ax.legend_
    handles = old_legend.legendHandles
    labels = [t.get_text() for t in old_legend.get_texts()]
    ax.legend(handles, labels, title=new_name)


import plotly.graph_objects as go
import numpy as np


def marimekko(df,x_var_name,y_var_name,effectif_var_name,color_discrete_sequence):
    labels = df[x_var_name].unique().tolist() #["apples","oranges","pears","bananas"]
    widths = np.array(df.groupby(x_var_name)[effectif_var_name].sum())/df[effectif_var_name].sum()*100
    Y_given_X = (df.groupby([x_var_name,y_var_name])[effectif_var_name].sum()/df.groupby(x_var_name)[effectif_var_name].sum()*100).reset_index()
    # test : Y_given_X.groupby(x_var_name).sum() == 100
    heights = {k: list(v) for k, v in Y_given_X.groupby(y_var_name)[effectif_var_name]}
    Total = df[effectif_var_name].sum()/10**6

    fig = go.Figure()
    for i,key in enumerate(heights):
        fig.add_trace(go.Bar(
            marker_color=color_discrete_sequence[i],
            name=key,
            y=heights[key],
            x=np.cumsum(widths)-widths,
            width=widths,
            offset=0,
            customdata=np.transpose([labels, np.around(widths*heights[key]/100,1),
                                     np.around(widths*heights[key]*Total/(100*100),1)]),
            texttemplate="Nb : %{customdata[2]} Millions, <br>%{customdata[1]} [%total]",
            textposition="inside",
            textangle=0,
            textfont_color="white",
            hovertemplate="<br>".join([
                "Nb : %{customdata[2]} Millions",
                "Prop : %{customdata[1]} [%total]"
            ])
        ))

    fig.update_xaxes(
        tickvals=np.cumsum(widths)-widths/2,
        ticktext= ["%s" % l for l in labels]
    )

    fig.update_xaxes(range=[0,100])
    fig.update_yaxes(range=[0,100])

    fig.update_layout(
        title_text="Marimekko Chart",
        barmode="stack",
        uniformtext=dict(mode="hide", minsize=10),
    )
    return fig
#cond_var_name="residential_type"

def marimekko_2(df,ColorY_var_name,horizontalX_var_name,TextureX_var_name,color_discrete_sequence,effectif_var_name='IPONDL'):
    ## ColorY_var_name : variable codée par couleur répartie sur la hauteur  --  e.g. classe énergétique
    ## horizontalX_var_name : variable codée par X -- e.g. age du bâtiment
    ## TextureX_var_name : variable codée par la texture sur la largeur -- e.g. type de logement
    pattern_sequence = [ '/', 'x', '-', '|', '+', '.',"\\",'']
    pattern_dic = dict(zip(df[TextureX_var_name].unique(),pattern_sequence))
    color_dic = dict(zip(df[ColorY_var_name].unique(), color_discrete_sequence))

    #calcul des distribution verticales et horizontales
    Total = df[effectif_var_name].sum()/10**6
    ColorY_given_horizontalX = (df.groupby([ColorY_var_name,horizontalX_var_name])[effectif_var_name].sum()/df.groupby(horizontalX_var_name)[effectif_var_name].sum()*100).reset_index()
    ColorY_given_horizontalX=ColorY_given_horizontalX.set_index([ColorY_var_name,horizontalX_var_name]). \
        rename(columns={"IPONDL": "Dheight"})
    ColorY_given_horizontalX["y1"] = ColorY_given_horizontalX["Dheight"].groupby([horizontalX_var_name]).cumsum()
    ColorY_given_horizontalX["Dheight0"] = ColorY_given_horizontalX["Dheight"].groupby([horizontalX_var_name]).shift().fillna(0)
    ColorY_given_horizontalX["y0"] = ColorY_given_horizontalX["Dheight0"].groupby([horizontalX_var_name]).cumsum()
    # test : ColorY_given_horizontalX.groupby(horizontalX_var_name)["Dheight"].sum() == 100
    AllX_given_ColorY= (df.groupby([ColorY_var_name,horizontalX_var_name,TextureX_var_name])[effectif_var_name].sum()/df[effectif_var_name].sum()*100).reset_index()
    AllX_given_ColorY=AllX_given_ColorY.set_index([ColorY_var_name,horizontalX_var_name,TextureX_var_name]).\
        rename(columns={"IPONDL": "Proportion"})
    # test : AllX_given_ColorY["Proportion"].sum() == 100
    AllDistrib = AllX_given_ColorY.join(ColorY_given_horizontalX, how="inner")
    AllDistrib["Dwidth"]=AllDistrib["Proportion"]/(AllDistrib["Dheight"]/100)
    AllDistrib["x1"] = AllDistrib["Dwidth"].groupby(ColorY_var_name).cumsum()
    AllDistrib["Dwidth0"] = AllDistrib["Dwidth"].groupby(ColorY_var_name).shift().fillna(0)
    AllDistrib["x0"] = AllDistrib["Dwidth0"].groupby(ColorY_var_name).cumsum()

    #to put labels on X axis
    widths = np.array(df.groupby([horizontalX_var_name])[effectif_var_name].sum()) / df[effectif_var_name].sum() * 100
    labels_X_axis  = df[horizontalX_var_name].unique().tolist()


    LegendList=[]
    fig = go.Figure()
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 100])
    for (ColorY_val,horizontalX_val,TextureX_val) in AllDistrib.index:
        cur_distrib = AllDistrib.loc[(ColorY_val,horizontalX_val,TextureX_val),]
        if (ColorY_val,TextureX_val) in LegendList:
            showlegend=False
        else:
            showlegend = True
            LegendList=LegendList+[(ColorY_val,TextureX_val)]
        x0 = cur_distrib.x0; x1=cur_distrib.x1;  y0 = cur_distrib.y0; y1=cur_distrib.y1;
        Effectif = df.set_index([ColorY_var_name,horizontalX_var_name,TextureX_var_name]).\
                       loc[(ColorY_val,horizontalX_val,TextureX_val),effectif_var_name]/10**6
        Proportion = Effectif /Total*100
        fig.add_trace(go.Scatter(
            showlegend=showlegend,
            fillpattern={
                "bgcolor": color_dic[ColorY_val],
                "fgcolor": "grey",
                "shape": pattern_dic[TextureX_val]
            },
            fill='tonexty',
            mode='none',
            marker={"line":{"autocolorscale":False,"color":"#FFFFFF","width":1}},
            marker_size=0,
            name="Class " + ColorY_val + ", "+TextureX_val,
            y=[y0, y0, y1, y1, y0],
            x=[x0, x1, x1, x0, x0],
            hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            showlegend=False,
            fill='tonexty',
            mode='none',
            marker={"line":{"autocolorscale":False,"color":"#FFFFFF","width":1}},
            marker_size=0,
            name="Class " + ColorY_val + ", "+TextureX_val,
            y=[(y0+y1)/2],
            x=[(x0+x1)/2],
            customdata=np.transpose([ColorY_val, horizontalX_val,TextureX_val,np.around(Effectif, 1),np.around(Proportion, 1)]),
            texttemplate="Nb : %{customdata[3]} Millions, <br> %{customdata[4]} [%total]",
            textposition='middle center',
            #textfont_color="white",
            hovertemplate="<br>".join([
                ColorY_val+","+horizontalX_val+","+TextureX_val,
                "Nb : "+str(np.around(Effectif, 2))+" Millions",
                "Prop : "+str(np.around(Proportion, 2))+" [%total]",
            ])
        ))


        fig.update_xaxes(range=[0, 100])
        fig.update_yaxes(range=[0, 100])
        fig.add_trace(go.Scatter(
            showlegend=False,
            mode='lines',
            hoverinfo="skip",
            line=dict(color='white', width=0.5),
            y=[y0, y0, y1, y1, y0],
            x=[x0, x1, x1, x0, x0],
        ))


    fig.update_xaxes(
        tickvals=np.cumsum(widths)-widths/2,
        ticktext= ["%s" % l for l in labels_X_axis]
    )
    for i in range(0,len(widths)-1):
        x0=np.cumsum(widths)[i]
        fig.add_trace(go.Scatter(
            showlegend=False,
            mode='lines',
            line=dict(color='#DEDEDE', width=1.1),
            y=[0,100],
            x=[x0,x0],
        ))

    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(
        hovermode="closest",
        legend_title=ColorY_var_name+", <br>"+TextureX_var_name,
        legend=dict(itemsizing="trace",itemwidth=40),
        title_text="Distribution de ("+ ColorY_var_name+","+horizontalX_var_name+","+TextureX_var_name+")",
        uniformtext=dict(mode="hide", minsize=10),
    )
    #plotly.offline.plot(fig, filename='tmp.html')

    return fig


def Create_simplified_variables(df):
    df["construction_year_class_simple"] = df["construction_year_class"]
    df.loc[df["construction_year_class_simple"].isin(['[1919, 1945]','[1000, 1918]']),"construction_year_class_simple"]='avant 1945'
    df.loc[df["construction_year_class_simple"].isin(['[1946, 1970]','[1991, 2005]','[1971, 1990]']), 'construction_year_class_simple']='[1946, 1990]'
    df.loc[df["construction_year_class_simple"].isin(['[2006, 2012]','[2013, 2100]']),"construction_year_class_simple"]='après 2006'

    df["living_area_class_simple"] = df["living_area_class"]
    df.loc[df["living_area_class_simple"].isin(['De 40 à 60 m²', 'De 30 à 40 m²', 'Moins de 30 m²']),"living_area_class_simple"]='moins de 60m2'
    df.loc[df["living_area_class_simple"].isin(['De 60 à 80 m²','De 80 à 100 m²']),"living_area_class_simple"]='De 60 à 100 m²'
    df.loc[df["living_area_class_simple"].isin(['De 100 à 120 m²', '120 m² ou plus']),"living_area_class_simple"]='100 m² ou plus'

    df["occupancy_status_simple"] = df["occupancy_status"]
    df.loc[df["occupancy_status_simple"].isin(['owner','free accomodation']),"occupancy_status_simple"]='Propriétaire'
    df.loc[df["occupancy_status_simple"].isin(['renter', 'low rent housing']),"occupancy_status_simple"]='Locataire'


    df["living_area_class_simple"] = df["living_area_class"]
    df.loc[df["living_area_class_simple"].isin(['De 40 à 60 m²', 'De 30 à 40 m²', 'Moins de 30 m²']),"living_area_class_simple"]='moins de 60m2'
    df.loc[df["living_area_class_simple"].isin(['De 60 à 80 m²','De 80 à 100 m²']),"living_area_class_simple"]='De 60 à 100 m²'
    df.loc[df["living_area_class_simple"].isin(['De 100 à 120 m²', '120 m² ou plus']),"living_area_class_simple"]='100 m² ou plus'

    df["heating_system_simple"] = df["heating_system"]
    df.loc[df["heating_system_simple"].isin(['Autres','Chauffage urbain']),"heating_system_simple"]='Autres et Chauffage urbain'
    df.loc[df["heating_system_simple"].isin(['Chaudière fioul','Chaudière - autres']),"heating_system_simple"]='Chaudière fioul-autre'

    return df
