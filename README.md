## Inicio rapido:

- Requiere *Python 3.13.2* y *Pip*
- Instalar *requirements.txt*
- Borrar la db si está inicializada
- Ejecutar *init_db.py*
- Levantar la api con *uvicorn src.main:api --reload* desde /Project

## Ficheros:
```
Project/ 
├── .pytest_cache/ # Archivos temporales de pytest 
├── src/ # Código fuente principal 
│   ├── models/ # Definiciones de modelos de base de datos 
│   │   ├── init.py 
│   │   └── user_model.py 
│   ├── responses/ # Manejo de respuestas 
│   │   ├── init.py 
│   │   └── responses.py 
│   ├── routers/ # Definición de rutas de la API 
│   │   ├── init.py 
│   │   └── user_router.py 
│   ├── schemas/ # Esquemas (Pydantic)  
│   │   ├── init.py 
│   │   └── user_schema.py 
│   ├── database.py # Configuración de la base de datos
│   └── main.py # Punto de entrada principal de la aplicación y handlers de excepciones
├── tests/ # Pruebas del proyecto (**Falta Continuar**)
├── init_db.py # Script para inicializar la base de datos 
├── test.db # Archivo de base de datos SQLite 
├── README.md # Documentación del proyecto 
└── .gitattributes # Configuración para Git
```
