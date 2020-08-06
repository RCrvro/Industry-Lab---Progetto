import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from pykafka import KafkaClient
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_extendable_graph as deg
import plotly.io as pio
import datetime

db = pd.read_csv("/Users/riccardocervero/Desktop/Progetto Industry Lab/DbRidotto.csv")

#Portata
client_portata = KafkaClient(hosts="127.0.0.1:9092")
topic1 = client_portata.topics['portata']
consumer1 = topic1.get_simple_consumer()

#Coefficiente
client = KafkaClient(hosts="127.0.0.1:9092")
topic = client.topics['test']
consumer = topic.get_simple_consumer()

colors = {
    'background': '#000000',
    'text': '#ffffff'
}


fig1 = go.Figure(dict(
            data=[{'x': [datetime.datetime.now().time().strftime('%H:%M:%S.%f')[:-3]],
                   'y': [0],
                   'mode':'lines+markers'
                   }],
                   layout=go.Layout(yaxis=dict(title='Flow rate values'),
                                    xaxis=dict(title='Observation'),
                                    template = "plotly_dark",
                                    colorway = ['#ff8400'])
        )
)

fig2 = go.Figure(dict(
            data=[{'x': [datetime.datetime.now().time().strftime('%H:%M:%S.%f')[:-3]],
                   'y': [0],
                   'mode':'lines+markers'
                   }],
                   layout=go.Layout(yaxis=dict(title='α values'),
                                    xaxis=dict(title='Observation'),
                                    template = "plotly_dark",
                                    colorway = ['#59e01b'])
        )

)


fig3 = go.Figure(data=go.Violin(y=db['Coefficiente_140'], box_visible=True, line_color='#46de00',
                               meanline_visible=True, fillcolor='#46de00', opacity=0.6
                               ),
                 layout= go.Layout(yaxis=dict(title='α values'),template = "plotly_dark"))


fig4 = go.Figure(data=go.Violin(y=db['media_portata_velocita_1'], box_visible=True, line_color='#ff8400',
                               meanline_visible=True, fillcolor='#ff8400', opacity=0.6
                               ),
                 layout= go.Layout(yaxis=dict(title='Flow rate values'),template = "plotly_dark"))



app = dash.Dash()
app.layout = html.Div(style={'backgroundColor': colors['background']},children=[html.H1(
        children='GP5 - Flow Performance Monitoring',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Application for real-time monitoring of flow rate and leakage coefficient values, received from simulated Apache-Kafka connected sensors.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([
        html.Div([
        html.H3(children=' Flow rate - Media portata 140rpm',
        style={'color': colors['text']}
    ),
    deg.ExtendableGraph(
        id='extendablegraph_portata',
        figure=fig1
    ),
    dcc.Interval(
        id='interval_extendablegraph_update1',
        interval=1000,
        n_intervals=0,
        max_intervals=-1),
    html.Div(id='output1') 
], className="six columns"),

        html.Div([
        html.H3(children=' Leakage coefficient α',
        style={'color': colors['text']}
    ),
    deg.ExtendableGraph(
        id='extendablegraph_example',
        figure=fig2
    ),
    dcc.Interval(
        id='interval_extendablegraph_update',
        interval=1000,
        n_intervals=0,
        max_intervals=-1),
    html.Div(id='output')
], className="six columns"),


        html.Div([
        html.H3(children='Flow rate - Boxplot',
        style={'color': colors['text']}
    ),
    deg.ExtendableGraph(
        id='extendablegraph_boxplot2',
        figure=fig4
    ),
    dcc.Interval(
        id='interval_extendablegraph_boxplot2',
        interval=1000,
        n_intervals=0,
        max_intervals=-1),
    html.Div(id='output_box2')
    ], className="six columns"),
        

        html.Div([
        html.H3(children='Leakage coefficient α - Boxplot',
        style={'color': colors['text']}
    ),
    deg.ExtendableGraph(
        id='extendablegraph_boxplot',
        figure=fig3
    ),
    dcc.Interval(
        id='interval_extendablegraph_boxplot',
        interval=1000,
        n_intervals=0,
        max_intervals=-1),
    html.Div(id='output_box')
    ], className="six columns"),


    ], className="row")
])

#Aggiunta del layout
fig1.update_traces(hovertemplate='Timestamp: %{x} <br>Value: %{y}')
fig2.update_traces(hovertemplate='Timestamp: %{x} <br>Value: %{y}')


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

@app.callback(Output('extendablegraph_example', 'extendData'),
              [Input('interval_extendablegraph_update', 'n_intervals')],
              [State('extendablegraph_example', 'figure')])
def update_extendData(n_intervals, existing):
    for message in consumer:
        if message is not None:
           x_new = datetime.datetime.now().time().strftime('%H:%M:%S.%f')[:-3]
           y_new = float(message.value.decode("utf-8"))
        return [dict(x=[x_new], y=[y_new])], [0], 100

@app.callback(Output('extendablegraph_boxplot2', 'extendData'),
              [Input('interval_extendablegraph_boxplot2', 'n_intervals')],
              [State('extendablegraph_boxplot2', 'figure')])
def update_extendData(n_intervals, existing):
    for message in consumer1:
        if message is not None:
           y_new = float(message.value.decode("utf-8"))
        return [dict(y=[y_new])], [0], 100

@app.callback(Output('extendablegraph_portata', 'extendData'),
              [Input('interval_extendablegraph_update1', 'n_intervals')],
              [State('extendablegraph_portata', 'figure')])
def update_extendData(n_intervals, existing):
    for message in consumer1:
        if message is not None:
           x_new = datetime.datetime.now().time().strftime('%H:%M:%S.%f')[:-3]
           y_new = float(message.value.decode("utf-8"))
        return [dict(x=[x_new], y=[y_new])], [0], 100

@app.callback(Output('extendablegraph_boxplot', 'extendData'),
              [Input('interval_extendablegraph_boxplot', 'n_intervals')],
              [State('extendablegraph_boxplot', 'figure')])
def update_extendData(n_intervals, existing):
    for message in consumer:
        if message is not None:
           y_new = float(message.value.decode("utf-8"))
        return [dict(y=[y_new])], [0], 100

if __name__ == '__main__':
    app.run_server(debug=True)
