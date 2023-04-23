from dash import Dash,dcc , Output, Input
import dash_bootstrap_components as dbc
import dash_html_components as html
import os
import  plotly.graph_objects as go 

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
title = html.H1('دنبال چی می گردی؟',style={'color':'green','font-family':'B Titr','text-align':'center'})
subtitle = html.P('با کالو هر کالایی رو که بخوای پیدا می کنی. فقط کافیه یه اسم بدی!', style={'text-align':'center', 'direction':'rtl'})
tBox = dcc.Input(
    id='searchname',
    value='نام محصول را وارد کنید...',
    type='text',
    style={
        'width': '550px',
        'color': '#8d8d8d',
        'margin': '10px',
        'direction': 'rtl',
        'padding': '10px 20px',
        'border': '1px solid #ddd',
        'border-radius': '25px',
    }
)

btn = html.Button(
    id='submit-button',
    children='جستجو',
    style={
        'background-color': '#03a9f4',
        'color': '#fff',
        'border-radius': '25px',
        'padding': '10px 20px',
        'border': '1px solid #ddd',
        'font-weight': 'bold'
    }
)

# Navigation bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("درباره ما", href="#")),
                    dbc.NavItem(dbc.NavLink("تماس با ما", href="#")), 
                ],
                navbar=True,
            ),
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/logo.png", height="40px", className="ml-auto"))
                    ],
                    align="center"
                ),
                href="#",
            )
        ]
    ),
    color="dark",
    style={'width' : '100%'},
    dark=True
)

# Data for products
products = [
    {"name": "Product 1", "image": "/assets/image1.png", "price": "$10.00"},
    {"name": "Product 2", "image": "/assets/image2.png", "price": "$20.00"},
    {"name": "Product 3", "image": "/assets/image3.png", "price": "$30.00"},
    {"name": "Product 4", "image": "/assets/image1.png", "price": "$10.00"},
    {"name": "Product 5", "image": "/assets/image2.png", "price": "$20.00"},
    {"name": "Product 6", "image": "/assets/image3.png", "price": "$30.00"},
]

# Create card for each product
cards = []
for product in products:
    card = dbc.Card(
        [
            html.Img(src=product["image"]),
            dbc.CardBody(
                [
                    html.H5(product["name"], className="card-title"),
                    html.P(product["price"], className="card-text"),
                ]
            ),
        ],
        style={"width": "18rem",
               'background-color': '#e9e9e9',
               "margin":"35px"},
    )
    cards.append(card)

# Create columns to hold the cards
row1 = dbc.Row(cards[:3])
row2 = dbc.Row(cards[3:6])
row3 = dbc.Row(cards[6:])

# Create a row to hold the columns
productbox = dbc.Row([row1, row2, row3] , style={
    'color': '#000',
    'padding': '10px 20px',
    'border': '1px solid #ddd',
    'font-weight': 'bold'
})

my_graph = dcc.Graph(figure={})

my_btn = dbc.Button('نمایش نمودار',style={'margin-top':'20px'})

@app.callback(
    Output(my_graph,component_property='figure'),
    Output(my_btn,component_property='n_clicks'),
    Input(my_btn,component_property='n_clicks')
)
def show_images(n_clicks):
    if n_clicks>0:
        
        with open('prices.txt') as f:
            number_list = f.read().split('\n')
        
        number_list = list(map(int,number_list))
        print(number_list)
        figure = go.Figure(data=go.Scatter(x=list(range(0,len(number_list))), y=number_list))
        return figure , n_clicks

app.layout = dbc.Container([
    navbar, # منوی بالا
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([title], width=12)
    ]), #تیتر اصلی صفحه
    dbc.Row([
        dbc.Col([subtitle], width=12)
    ]),#عنوان فرعی صفحه
    dbc.Row([
        dbc.Col([tBox], width={"size": 12, "offset": 12}, className="text-center justify-content-center"),
        dbc.Col([btn], width={"size": 6, "offset": 3}, className="text-center justify-content-center")
    ]),
    html.Br(),
    html.Div([productbox]), # محصولات
    dbc.Row([my_graph,my_btn],className='text-center') #نمودار
])

if __name__=='__main__':
    app.run_server(port='8000')
