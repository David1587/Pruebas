# API de Gestión de Vulnerabilidades en Cloud

Esta API en Django REST Framework permite gestionar vulnerabilidades en infraestructura Cloud, cruzando información con CVEs del NIST.

## Instalación y ejecución

### 1️⃣ Clonar el repositorio
```sh
git clone https://github.com/TU_USUARIO/NOMBRE_DEL_REPO.git
cd NOMBRE_DEL_REPO
2️⃣ Configurar el entorno virtual
sh
Copiar
Editar
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
pip install -r requirements.txt
3️⃣ Configurar la base de datos
Modificar settings.py con la configuración de la base de datos que prefieras.

4️⃣ Ejecutar migraciones
sh
Copiar
Editar
python manage.py migrate
5️⃣ Ejecutar la aplicación
sh
Copiar
Editar
python manage.py runserver
La API estará disponible en http://localhost:8000/vulnerabilities/

🐳 Usando Docker
sh
Copiar
Editar
docker build -t django-api .
docker run -p 8000:8000 django-api
📌 Endpoints principales
GET /vulnerabilities/ → Obtener todas las vulnerabilidades
POST /vulnerabilities/fixed/ → Registrar vulnerabilidades solucionadas
GET /vulnerabilities/unfixed/ → Listar vulnerabilidades no solucionadas
GET /vulnerabilities/summary/ → Resumen de vulnerabilidades por severidad
GET /vulnerabilities/fetch_nist/ → Obtener datos del NIST
📖 Autenticación y Seguridad
La API puede usar tokens JWT para autenticación. Revisa la documentación en docs/.

