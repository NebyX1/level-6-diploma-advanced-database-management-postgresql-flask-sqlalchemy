from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData, create_engine
from database.config import DATABASE_CONNECTION_URI

# Crea un engine a partir de la URI de conexión a la base de datos
engine = create_engine(DATABASE_CONNECTION_URI)

# Configuración para generar el gráfico utilizando tus modelos definidos
graph = create_schema_graph(metadata=MetaData(),
                            show_datatypes=True,  # Muestra los tipos de columnas
                            show_indexes=False,  # No muestra los índices
                            rankdir='LR',  # De izquierda a derecha, usa 'TB' para de arriba a abajo
                            concentrate=False,  # No une los bordes entre las mismas entidades
                            engine=engine)  # Pasa el engine a create_schema_graph
graph.write_png('schema_diagram.png')  # Guarda el diagrama como PNG
