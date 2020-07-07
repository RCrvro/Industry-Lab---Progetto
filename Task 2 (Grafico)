import plotly.graph_objects as go
import numpy as np
import pandas as pd
from IPython.display import clear_output

def col(z,t=Tipo_pompa):
  if t == "STD":
    if (z<=57.36)|(z>=75.36):
      return "red"
    else:
      return "green"
  elif t == "DAI":
    if (z<=45.86)|(z>=63.36):
      return "red"
    else:
      return "green"

def limitgraph():
  Tipo_pompa=(input("Inserire il tipo di Pompa (DAI o STD): "))
  c = [float(e) for e in [(input("Inserire coordinate di pressione e coefficiente: "))][0].split(",")]
  c.append(float(108.36-(c[0]*c[1])))
  c = pd.DataFrame(c).transpose()
  c.columns = ['x','y','z']
  if Tipo_pompa == "DAI":
    db = pd.read_csv("/content/bench_DAI.csv",header=None,sep="\t")
  elif Tipo_pompa == "STD":
    db = pd.read_csv("/content/benchSTD.csv",header=None,sep="\t")
  fig = go.Figure()
  fig.add_trace(go.Mesh3d(x=db[0],y=db[1],z=db[2],opacity=0.2,color='blue',name="Reg. critica"))
  fig.update_layout(title=str("Limite di portata ("+str(Tipo_pompa)+")"),autosize=False,width=700,margin=dict(r=20, l=10, b=10, t=10))
  cl = col(c['z'][0])
  fig.add_trace(go.Scatter3d(x=c.x, y=c.y, z=c.z,mode='markers',marker=dict(color=cl),name="Osservazione"))
  fig.update_layout(scene = dict(
                    xaxis_title='Pressione',
                    yaxis_title='Coefficiente',
                    zaxis_title='Portata'))
  clear_output(wait=True)
  fig.show()
  
  #Per eseguire
  limitgraph()
