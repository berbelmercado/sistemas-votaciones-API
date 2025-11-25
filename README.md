Este proyecto es un API RESTful para gestionar un sistema de votaciones, desarrollado con FastAPI y SQLAlchemy.
Permite registrar votantes, candidatos, emitir votos y obtener estadísticas de la votación.

La base de datos utilizada es SQLite, para facilitar la ejecución sin necesidad de instalar servidores adicionales.

# Instrucciones para ejecutar el proyecto

1. descargar el archivo desde Github contenido en la URL https://github.com/berbelmercado/sistemas-votaciones-API
2. abrir la carpeta descargada desde Visual Studio Code
3. abrimos una nueva terminal en VSCode y creamos un entorno virtual:
	# Windows
	python -m venv env
	
	# Mac/Linux
	source env/bin/activate

4. activamos entorno virtual: cd env/Scripts/activate o abriendo una nueva terminal en VSCode
5. instalamos las dependencias ejecutando la siguiente linea:
	pip install -r requirement.txt

6. ejecutamos la siguiente linea para iniciar servidor local:
	 uvicorn  app:app --reload 

# Endpoints

Votantes
Método	Ruta	        Descripción
POST	/voters	        Registrar un nuevo votante
GET	/voters	        Listar todos los votantes
GET	/voters/{id}	Obtener un votante por ID
DELETE	/voters/{id}	Eliminar un votante

Candidatos
Método	Ruta	                Descripción
POST	/candidates	        Registrar un nuevo candidato
GET	/candidates	        Listar todos los candidatos
GET	/candidates/{id}	Obtener un candidato por ID
DELETE	/candidates/{id}	Eliminar un candidato

Votos
Método	Ruta	                Descripción
POST	/votes	                Emitir un voto voter_id y candidate_id
GET	/votes	                Listar todos los votos emitidos
GET	/votes/statistics	Obtener estadísticas de votación total, porcentaje, total de votantes que votaron.
# Documentación
FastAPI genera documentación automática se debe iniciar el sersidor local y luego ingresar a cualquiera de las 2 URL

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

# Capturas de estadisticas
- http://127.0.0.1:8000/votes/statistics
<img width="568" height="574" alt="image" src="https://github.com/user-attachments/assets/29b5ef04-a573-476a-9988-614f28647f53" />

# Ejemplos en postman

**Endpoint:** ` GET http://127.0.0.1:8000/voters/1`  
**Descripción:** Busca un votante.

**Request (GET):**

```json
{
    "name": "milton",
    "email": "milton@gmail.com",
    "id": 1,
    "has_voted": true
}

**Endpoint:** ` POST http://127.0.0.1:8000/voters/1`  
**Descripción:** Busca un votante.

**Request (POST):**

```json
{
	"name": "CamDanielaila"
    ,"email":"DaRD@hotmail"
}

**Respuesta:**  
```json{
    "name": "CamDanielaila",
    "email": "DaRD@hotmail",
    "has_voted": false,
    "message": "Votante registrado exitosamente"
}


