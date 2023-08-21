import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Cargar los datos
df_idj = pd.read_csv('IDJ_Jovenes.csv')

# Crear la aplicación de Dash
app = dash.Dash(__name__)

# Diseño del tablero con estilos
app.layout = html.Div(style={'backgroundColor': 'lightblue', 'textAlign': 'center'}, children=[
    html.H1("Indice de Desarrollo Juvenil", style={'color': 'darkblue'}),
    dcc.Tabs(id="tabs", value='educacion', children=[
        dcc.Tab(label='Educacion', value='educacion'),
        dcc.Tab(label='Salud', value='salud'),
        dcc.Tab(label='Estilo de Vida', value='estilo de vida'),
    ]),
    html.Div(id='tab-content')
])

# Callback para actualizar el contenido según la sección seleccionada
nivel_estudio_orden = ['Grado 1', 'Grado 2', 'Grado 3', 'Grado 4', 'Grado 5', 'Grado 6', 'Grado 7', 'Grado 8',
                       'Grado 9', 'Grado 10', 'Grado 11', 'Técnica incompleta o en curso',
                       'Tecnología Incompleta o en curso', 'Universitaria Incompleta o en curso',
                       'Técnica Completa', 'Tecnología Completa', 'Universitaria completa',
                       'No sabe/ No informa']
count_df = df_idj.groupby(['Edad', 'Estudia']).size().reset_index(name='Count')


si_data = count_df[count_df['Estudia'] == 'Sí']
no_data = count_df[count_df['Estudia'] == 'No']

contingency_table_percent = pd.crosstab(df_idj['NivelEstudio'], df_idj['Estrato'], normalize='index') * 100

df_copy = df_idj.copy()


df_copy['Count'] = 1

filtered_df = df_idj[(df_idj['RangoEdad'] == '14-17 años') & (df_idj['Trabaja'] == 'Sí')]


count_by_estrato = filtered_df.groupby('Estrato').size().reset_index(name='Count')

orden_categorias = ["No aplica", "13", "14","15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]

@app.callback(Output('tab-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'educacion':
        return html.Div(style={'margin': '20px'}, children=[
            dcc.Graph(
                figure=px.pie(df_idj, names='FrecuenciaLectura', title='Porcentaje de la Frecuencia con que leen')
            ),
            dcc.Graph(
                figure=px.histogram(
                    df_idj,
                    x='Edad',
                    color='NivelEstudio',
                    title='Distribución de Nivel de Estudio por Edad',
                    labels={'Edad': 'Edad', 'NivelEstudio': 'Nivel de Estudio'},
                    barmode='stack',
                    category_orders={'NivelEstudio': nivel_estudio_orden} 
                ).update_layout(
                    autosize=False,
                    width=1293,
                    height=800
                )
            ),
            dcc.Graph(
                figure=px.histogram(
                    df_idj,
                    x='Edad',
                    color='Estudia',
                    title='Distribución de Respuesta al Estudio por Edades ',
                    labels={'Edad': 'Edad', 'Estudia': 'Estudia'},
                    barmode='group'
                )
            ),
            dcc.Graph(
                figure=px.line(
                    title='Variación de Respuesta al Estudio por Edad',
                    labels={'Edad': 'Edad', 'Count': 'Cantidad'},    
                ).add_scatter(
                    x=si_data['Edad'], y=si_data['Count'], mode='lines', line_shape='linear', line=dict(color='blue'), name='Sí Estudia'
                ).add_scatter(
                    x=no_data['Edad'], y=no_data['Count'], mode='lines', line_shape='linear', line=dict(color='red'), name='No Estudia'
                )
            ),
            dcc.Graph(
                figure=px.bar(
                    contingency_table_percent, x=contingency_table_percent.index, y=contingency_table_percent.columns,
                    title='Distribución de Estrato por Nivel de Estudio', labels={'index': 'Nivel de Estudio'},
                    barmode='relative', height=500
                ).update_yaxes(
                    title_text='Porcentaje'
                )
            )
        ])
    elif tab == 'salud':
        return html.Div(style={'margin': '20px'}, children=[
            dcc.Graph(
                figure=px.pie(df_idj, names='AfiliacionSalud', title='Porcentaje de la Afiliacion a la Salud')
            ),
            dcc.Graph(
                figure=px.box(
                    df_idj, x='Edad', y='AfiliacionSalud', title='Afiliacion de la Salud por Edad'
                )
            ),
            dcc.Graph(
                figure=px.pie(
                    df_idj, names='FrecuenciaEjercicio', title='Porcentaje de la Frecuencia con que hacen ejercicio'
                )
            ),
            dcc.Graph(
                figure=px.box(
                    df_idj, x='Edad', y='FrecuenciaEjercicio', title='Frecuencia de Ejercicio por Edad'
                )
            ),
            dcc.Graph(
                figure=px.pie(
                    df_copy,
                    names='ConsumoLicor',
                    title='Distribución de Consumo de Licor por Rango de Edad',
                    hole=0.4,
                    color='ConsumoLicor',
                    facet_col='RangoEdad',
                    color_discrete_sequence=px.colors.qualitative.Set1  
                )
            ),
            dcc.Graph(
                figure=px.pie(
                    df_copy,
                    names='ConsumoDrogas',
                    title='Distribución de Consumo de Drogas por Rango de Edad',
                    hole=0.4,
                    color='ConsumoDrogas',
                    facet_col='RangoEdad',
                    color_discrete_sequence=px.colors.qualitative.Set1
                )
            ),
            dcc.Graph(
                figure=px.pie(
                    df_copy,
                    names='ConsumoCigarrillo',
                    title='Distribución de Consumo de Cigarrillo por Rango de Edad',
                    hole=0.4,
                    color='ConsumoCigarrillo',
                    facet_col='RangoEdad',
                    color_discrete_sequence=px.colors.qualitative.Set1
                )
            )
        ])    
    elif tab == 'estilo de vida':
        return html.Div(style={'margin': '20px'}, children=[
            dcc.Graph(
                figure=px.bar(
                    df_idj,
                    x='RangoEdad',
                    color='Trabaja',
                    barmode='group',
                    title='Comportamiento Laboral por Rango de Edad',
                    labels={'RangoEdad': 'Rango de Edad', 'Trabaja': '¿Trabaja?'}
                ).update_layout(
                    font_color='black',
                    paper_bgcolor='lightgray',  
                    plot_bgcolor='lightgray',        
                    barmode='group'
                )
            ),
            dcc.Graph(
                figure=px.bar(
                    count_by_estrato,
                    x='Estrato',
                    y='Count',
                    title='Distribución de Niños que trabajan en por Estratos para el Rango 14-17',
                    labels={'Estrato': 'Estrato', 'Count': 'Cantidad de Trabajadores'}
                )
            ),
            dcc.Graph(
                figure=px.histogram(
                    df_idj,
                    x='EdadALaQueTuvoPrimerHijo',
                    title='Distribución de Edad al Tener el Primer Hijo',
                    labels={'Edadalaquetuvosuprimerhijo': 'Edad al tener el primer hijo'},
                    nbins=10,
                    category_orders={"EdadALaQueTuvoPrimerHijo": orden_categorias} 
                )
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
