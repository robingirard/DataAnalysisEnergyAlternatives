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
#cond_var_name="occupancy_status"
def marimekko_2(df,x_var_name,y_var_name,cond_var_name,effectif_var_name,color_discrete_sequence):
    labels = df[x_var_name].unique().tolist() #["apples","oranges","pears","bananas"]
    Cond_var_values = df[cond_var_name].unique().tolist()
    widths = np.array(df.groupby([x_var_name])[effectif_var_name].sum())/df[effectif_var_name].sum()*100
    Y_given_X = (df.groupby([x_var_name,y_var_name])[effectif_var_name].sum()/df.groupby(x_var_name)[effectif_var_name].sum()*100).reset_index()
    # test : Y_given_X.groupby(x_var_name).sum() == 100
    heights = {k: list(v) for k, v in Y_given_X.groupby(y_var_name)[effectif_var_name]}
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

            fig.add_trace(go.Bar(
                marker_color=color_discrete_sequence[i],
                marker_pattern_shape=patter_sequence[j],
                name=key,
                y=heights[key],
                x=np.cumsum(widths)-widths+cur_offset,
                width=widths*alpha,
                offset=0,
                customdata=np.transpose([labels, np.around(widths*heights[key]*alpha/100,1),
                                         np.around(widths*heights[key]*Total*alpha/(100*100),1)]),
                texttemplate="Nb : %{customdata[2]} Millions, <br>%{customdata[1]} [%total]",
                textposition="inside",
                textangle=0,
                textfont_color="white",
                hovertemplate="<br>".join([
                    "Nb : %{customdata[2]} Millions",
                    "Prop : %{customdata[1]} [%total]"
                ])
            ))
            cur_offset=cur_offset+widths*alpha
        fig.update_xaxes(
            tickvals=np.cumsum(widths)-widths/2,
            ticktext= ["%s" % l for l in labels]
        )
        fig.update_xaxes(range=[0, 100])
        fig.update_yaxes(range=[0, 100])




    fig.update_layout(
        title_text="Marimekko Chart",
        barmode="stack",
        uniformtext=dict(mode="hide", minsize=10),
    )
    plotly.offline.plot(fig, filename='tmp.html')

    return fig



