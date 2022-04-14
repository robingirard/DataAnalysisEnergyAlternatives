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
def marimekko_2(df,x_var_name,y_var_name,cond_var_name,effectif_var_name,color_discrete_sequence):
    labels = df[x_var_name].unique().tolist() #["apples","oranges","pears","bananas"]
    Cond_var_values = df[cond_var_name].unique().tolist()
    widths = np.array(df.groupby([x_var_name])[effectif_var_name].sum())/df[effectif_var_name].sum()*100
    Y_given_X = (df.groupby([x_var_name,y_var_name])[effectif_var_name].sum()/df.groupby(x_var_name)[effectif_var_name].sum()*100).reset_index()
    # test : Y_given_X.groupby(x_var_name).sum() == 100
    heights = {k: list(v) for k, v in Y_given_X.groupby([y_var_name])[effectif_var_name]}
    Total = df[effectif_var_name].sum()/10**6
    Condvar_given_XY= (df.groupby([x_var_name,y_var_name,cond_var_name])[effectif_var_name].sum()/df.groupby([x_var_name,y_var_name])[effectif_var_name].sum()*100).reset_index()
    Condvar_given_XY=Condvar_given_XY.set_index([x_var_name,y_var_name,cond_var_name])
    # test : Condvar_given_XY.groupby([x_var_name,y_var_name]).sum() == 100

    patter_sequence =["/",".", "x", "+"]
    fig = go.Figure()
    for i,key in enumerate(heights):
        cur_offset = widths*0
        for j in range(0,len(Cond_var_values)):
            alpha = np.array(Condvar_given_XY.loc[(slice(None),key,Cond_var_values[j]),"IPONDL"])/100
            y0 = np.cumsum([0]+heights[key].copy() );
            y1 = np.cumsum(heights[key].copy()+[100])
            for k in range(0,len(widths)):
                if k==0:
                    showlegend = True
                else :
                    showlegend = False
                x0 = np.cumsum(widths)[k]-widths[k]+cur_offset[k]
                x1 = x0 + widths[k]*alpha[k]
                fig.add_trace(go.Bar(
                    showlegend=showlegend,
                    marker_color=color_discrete_sequence[i],
                    marker_pattern_shape=patter_sequence[j],
                    name="Class "+key+", "+Cond_var_values[j],
                    offset=0,y=heights[key].copy(),
                    x=[np.cumsum(widths)[k]-widths[k]+cur_offset[k]],
                    width=widths[k]*alpha[k],
                    customdata=np.transpose([labels[k], np.around(widths*heights[key]*alpha/100,1)[k],
                                             np.around(widths*heights[key]*Total*alpha/(100*100),1)[k]]),
                    texttemplate="Nb : %{customdata[2]} Millions, <br>%{customdata[1]} [%total]",
                    textposition="inside",
                    textangle=0,
                    textfont_color="white",
                    hovertemplate="<br>".join([
                        "Nb : %{customdata[2]} Millions",
                        "Prop : %{customdata[1]} [%total]"
                    ])
                ))

            cur_offset = cur_offset + widths * alpha
        fig.update_xaxes(
            tickvals=np.cumsum(widths)-widths/2,
            ticktext= ["%s" % l for l in labels]
        )
        fig.update_layout(barmode='stack')
        fig.update_xaxes(range=[0, 100])
        fig.update_yaxes(range=[0, 100])

    fig.update_layout(
        title_text="Marimekko Chart",
        barmode = "stack" ,
        uniformtext=dict(mode="hide", minsize=10),
    )
    plotly.offline.plot(fig, filename='tmp.html')

    return fig

ColorY_var_name="energy_class"
horizontalX_var_name="construction_year_class"
TextureX_var_name="residential_type"
def marimekko_3(df,ColorY_var_name,horizontalX_var_name,TextureX_var_name,effectif_var_name,color_discrete_sequence):
    ## ColorY_var_name : variable codée par couleur répartie sur la hauteur  --  e.g. classe énergétique
    ## horizontalX_var_name : variable codée par X -- e.g. age du bâtiment
    ## TextureX_var_name : variable codée par la texture sur la largeur -- e.g. type de logement
    pattern_sequence = ["/", ".", "x", "+"]
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
    AllX_given_ColorY= (df.groupby([ColorY_var_name,horizontalX_var_name,TextureX_var_name])[effectif_var_name].sum()/df.groupby([ColorY_var_name])[effectif_var_name].sum()*100).reset_index()
    AllX_given_ColorY=AllX_given_ColorY.set_index([ColorY_var_name,horizontalX_var_name,TextureX_var_name]).\
        rename(columns={"IPONDL": "Proportion"})
    # test : AllX_given_ColorY.groupby(ColorY_var_name)["Dwidth"].sum() == 100
    AllDistrib = AllX_given_ColorY.join(ColorY_given_horizontalX, how="inner")
    AllDistrib["Dwidth"]=AllDistrib["Proportion"]/AllDistrib["Dheight"]*100
    AllDistrib["x1"] = AllDistrib["Dwidth"].groupby(ColorY_var_name).cumsum()
    AllDistrib["Dwidth0"] = AllDistrib["Dwidth"].groupby(ColorY_var_name).shift().fillna(0)
    AllDistrib["x0"] = AllDistrib["Dwidth0"].groupby(ColorY_var_name).cumsum()



    LegendList=[]


    fig = go.Figure()
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
                "shape": pattern_dic[TextureX_val]
            },
            fill='tonexty',
            mode='none',
            name="Class " + ColorY_val + ", "+TextureX_val,
            y=[y0, y0, y1, y1, y0],
            x=[x0, x1, x1, x0, x0],
            texttemplate="Nb : "+str(np.around(Effectif, 1))+" Millions, <br>"+str(np.around(Proportion, 1))+" [%total]",
            textfont_color="white",
            hovertemplate="<br>".join([
                "Nb : "+str(np.around(Effectif, 1))+" Millions",
                "Prop : "+str(np.around(Proportion, 1))+" [%total]"
            ])
        ))
  #  fig.update_xaxes(
  #      tickvals=np.cumsum(widths)-widths/2,
  #      ticktext= ["%s" % l for l in labels]
  #  )
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 100])

    fig.update_layout(
        title_text="Marimekko Chart",
        uniformtext=dict(mode="hide", minsize=10),
    )
    plotly.offline.plot(fig, filename='tmp.html')

    return fig
