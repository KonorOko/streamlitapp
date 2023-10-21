'''
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from the .env file
load_dotenv()
from sqlalchemy import create_engine, MetaData

connection_string = "mysql+mysqlconnector://45wonyp10vd2fnvak8tz:pscale_pw_fFwKbJoObAsv3eSc3qmQMdX6t0rmT2MJu4W7AAGJiyB@aws.connect.psdb.cloud:3306/project"
engine = create_engine(connection_string, echo=True)

metadata = MetaData()
metadata.reflect(bind=engine)

for table in metadata.tables.values():
    print(table.name)

from models import Ahorro

# Crear una instancia del modelo Ahorro con los valores que deseas agregar
nuevo_registro = Ahorro(Fecha='2023-10-19', Ingreso=10, Gasto=0)

# Establecer una sesión con la base de datos
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Agregar el nuevo registro a la sesión y luego hacer commit para guardar los cambios en la base de datos
session.add(nuevo_registro)
session.commit()

# Cerrar la sesión después de realizar las operaciones
session.close()
'''