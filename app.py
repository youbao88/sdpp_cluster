from flask import Flask, render_template, Response, send_from_directory, url_for
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

app = Flask(__name__)
@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html', title = 'Home')

@app.route('/sankey')
def sankey():

    with open('static/visualization/sankey_plot_labels.json', 'rb') as file:
        output_redo = json.load(file)['data']

    node_x_position = [0.01]*6+[0.5]*6+[0.99]*6+[0.25, 0.75]
    node_y_position = [0.01, 0.25, 0.45, 0.62,0.78,0.9]*3 + [0.95, 0.95] 

    node_color = ['rgba(0.21044753832183283, 0.6773105080456748, 0.6433941168468681,1)']*3+['rgba(0.9677975592919913, 0.44127456009157356, 0.5358103155058701,1)']*3
    node_color = node_color *3 + ['rgba(168,168,168,1)']*2

    link_color = ['rgba(168,168,168,0.3)']*12
    link_color_ = ['rgba(0.21044753832183283, 0.6773105080456748, 0.6433941168468681,0.3)']*6*3 + ['rgba(0.9677975592919913, 0.44127456009157356, 0.5358103155058701,0.3)']*6*3
    link_color = link_color + link_color_*2

    fig_sankey = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 15,
        line = dict(color = "black", width = 0.5),
        label = ['%s-%s'%(str(y),x) for x in ['base', '10y', '20y'] for y in ['VLR', 'LRMP', 'LRHB', 'HRVP', 'HRBF', 'HRIR']] + ['type 2 diabetes', 'type 2 diabetes'],
        color = node_color,
        x = node_x_position,
        y = node_y_position,
        ),
        link = dict(
        source = [x[0] for x in output_redo], # indices correspond to labels, eg a1, a2, a1, b1, ...
        target = [x[1] for x in output_redo],
        value = [x[2] for x in output_redo],
        color = link_color
    ))])
    fig_sankey.update_layout(paper_bgcolor='rgba(0,0,0,0)', height = 800, font_size = 15)
    sankey_json = json.dumps(fig_sankey, cls = PlotlyJSONEncoder)
    return render_template('sankey.html', title = 'Sankey Plot', sankey_json = sankey_json)

@app.route('/umap')
def umap():
    sdpp_3d_UMAP_df = pd.read_csv('static/visualization/sdpp_3d_UMAP_210909.csv')
    fig_sdpp_3d_umap = px.scatter_3d(sdpp_3d_UMAP_df, x='x', y='y', z='z',
              color='cluster_labels_baseline')
    fig_sdpp_3d_umap.update_layout(font_size=15, height = 700, paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)', legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
    sdpp_umap_json = json.dumps(fig_sdpp_3d_umap, cls = PlotlyJSONEncoder)

    mexico_3d_UMAP_df = pd.read_csv('static/visualization/mexico_3d_UMAP_211007.csv')
    fig_mexico_3d_umap = px.scatter_3d(mexico_3d_UMAP_df, x='x', y='y', z='z',
              color='cluster_labels_baseline')
    fig_mexico_3d_umap.update_layout(font_size=15, height = 700, paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)', legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
    mexico_umap_json = json.dumps(fig_mexico_3d_umap, cls = PlotlyJSONEncoder)
    return render_template('umap.html', title = '3D Umap', sdpp_umap_json = sdpp_umap_json, mexico_umap_json = mexico_umap_json)

@app.route('/about')
def about():
    return render_template('about.html', title = 'About Us')

if __name__ == '__main__':
    app.run(debug = True, port = 5555)