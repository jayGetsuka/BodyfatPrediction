from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from dash_bootstrap_components._components.Container import Container
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

 
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assert/style.css'])
 
PLOTLY_LOGO = "https://i.gifer.com/Vnni.gif"

df = pd.read_csv('bodyfat.csv').dropna()


data = ["Neck", "Weight", "Abdomen", "Hip"]
X = df[data] #df[data] # Independet variable
y = df['BodyFat'] # dependent variable

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=23)


lin_reg = LinearRegression()
lin_reg.fit(X_train,y_train)

r2_score = lin_reg.score(X_test,y_test)
model_acc = r2_score*100

def Bodyfat_predict(x):
    result = lin_reg.predict([ [36.2, 154.25, 85.2, 94.5] ])
    return result[0]

 
app.layout = html.Div([
   dbc.Navbar(
           dbc.Container(
               [
                   html.A(
                       # Use row and col to control vertical alignment of logo / brand
                       dbc.Row(
                           [
                               dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                               dbc.Col(dbc.NavbarBrand("Dash BodyFat Prediction", className="ms-2")),
                           ],
                           align="center",
                           className="g-0",
                       ),
                       href="https://www.kaggle.com/datasets/bretthammit/pokemongo-stats-dataset",
                       style={"textDecoration": "none"},
                   ),
               ]
           ),
           color="dark",
           dark=True,
       )
   ,
   html.Div([
    html.Div([html.H5('{:.2f}'.format(model_acc)), html.P('Model  Accuracy')], style={'padding': 20, 'flex': 1, 'background-color':'#292b2c', 'margin-left':20, 'margin-right':20, 'margin-top':20, 'text-align':'center', 'color':'white'}),
    html.Div([html.H5(f'{len(df)}'), html.P('Number of rows in the data set')], style={'padding': 20, 'flex': 1, 'background-color':'#0275d8', 'margin-left':20, 'margin-right':20, 'margin-top':20, 'text-align':'center', 'color':'white'})

   ] , style={'display': 'flex', 'flex-direction': 'row'}),
   
   html.Div([
       html.Div([

       html.H5('Neck ',style={'display':'inline-block','margin-right':20, 'font-weight':'bold'}),
           dbc.Input(placeholder="Input Neck value", type="text", id="input-on-submit"),
           dbc.FormText(" Type number Neck in the box above"),
           html.Br(),html.Br(),
 
        html.H5('Weight',style={'display':'inline-block','margin-right':20, 'font-weight':'bold'}),
           dbc.Input(placeholder="Input Weight...", type="text", id="input-on-submit2"),
           dbc.FormText(" Type number Weight in the box above"),
           html.Br(),html.Br(),

        html.H5('Abdomen',style={'display':'inline-block','margin-right':20, 'font-weight':'bold'}),
           dbc.Input(placeholder="Input Abdomen...", type="text", id="input-on-submit3"),
           dbc.FormText(" Type number Abdomen in the box above"),
           html.Br(),html.Br(),

        html.H5('Hip',style={'display':'inline-block','margin-right':20, 'font-weight':'bold'}),
           dbc.Input(placeholder="Input Hip...", type="text", id="input-on-submit4"),
           dbc.FormText(" Type number Hip in the box above"),
           html.Br(),html.Br(),
        
        html.Div([
           dbc.Button("Submit", color="primary", id='submit-val', n_clicks=0),
   ], className="d-grid gap-2 col-6 mx-auto"),
 
   ], style={'padding': 20, 'flex': 1}),
 
       html.Div([

           html.Div(id='container-button-basic', style={'text-align':'center'},
            children=[]),
 
       ], style={'padding': 20, 'flex': 1}),
      
      
   ], style={'display': 'flex', 'flex-direction': 'column'}),
 
   
])
 
 
@app.callback(
   Output('container-button-basic', 'children'),
   Input('submit-val', 'n_clicks'),
   State('input-on-submit', 'value'),
   State('input-on-submit2', 'value'),
   State('input-on-submit3', 'value'),
   State('input-on-submit4', 'value'),
   
)
  
def update_output(n_clicks, value, value2, value3, value4):
    value_db = [value, value2, value3, value4]

    if not None in value_db:
        result = Bodyfat_predict(value_db)
        return html.Div([html.H5(f'Your body fat percentage is:  {result:.2f}')])
    else:
        return ''
