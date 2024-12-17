# CEDICA Web Page

Este proyecto es una aplicación web desarrollada para gestionar los procesos administrativos y operativos de **CEDICA** (Centro de Equinoterapia y Deportes Ecuestres Adaptados). Combina un backend robusto en **Flask** con un frontend moderno en **Vue.js**.

---

## 🚀 Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: Vue.js + TailwindCSS
- **Base de Datos**: PostgreSQL
- **Almacenamiento de Documentos**: MinIO
- **Autenticación**: OAuth (Google)
- **Otros**: SQLAlchemy, ULID

---

## 📂 Estructura del Proyecto

```plaintext

/proyecto-raiz
│
├── admin/                     # Aplicación de administración (backend)
│   ├── __pycache__/           # Archivos de caché de Python
│   ├── downloads/             # Carpeta para descargas
│   ├── flask_session/         # Configuración de sesiones de Flask
│   ├── node_modules/          # Dependencias de Node.js (si se usan)
│   ├── src/                   # Código fuente principal
│   │   ├── core/              # Lógica central del backend
│   │   ├── downloads/         # Módulos relacionados con descargas
│   │   └── web/               # Controladores y vistas web
│   ├── static/                # Archivos estáticos (CSS, JS, imágenes)
│   ├── tests/                 # Pruebas unitarias y de integración
│   ├── .gitignore             # Archivos y carpetas ignorados por Git
│   ├── app.py                 # Archivo principal de la aplicación Flask
│   ├── poetry.lock            # Archivo de bloqueo de dependencias (Poetry)
│   ├── pyproject.toml         # Configuración del proyecto Python
│   └── README.md              # Documentación de la aplicación admin
│
├── portal/                    # Aplicación pública (frontend)
│   ├── dist/                  # Archivos compilados para producción
│   ├── node_modules/          # Dependencias de Node.js
│   ├── public/                # Archivos públicos (index.html, favicon, etc.)
│   ├── src/                   # Código fuente del frontend
│   ├── .gitignore             # Archivos ignorados por Git
│   ├── babel.config.js        # Configuración de Babel
│   ├── jsconfig.json          # Configuración de JavaScript
│   ├── package.json           # Dependencias y scripts del proyecto Node.js
│   ├── package-lock.json      # Archivo de bloqueo de dependencias
│   ├── README.md              # Documentación de la aplicación portal
│   └── vue.config.js          # Configuración de Vue.js
│
├── node_modules/              # Dependencias globales (si las hay)
└── README.md                  # Documentación principal del proyecto

```

---

## ⚙️ Instalación y Configuración

### 1. Clona el repositorio

```bash
git clone https://github.com/frandiaz99/CEDICA_WebPage.git
cd CEDICA_WebPage
```

### 2. Configura el entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura las variables de entorno

Crea un archivo `.env` en la carpeta raíz y agrega:

```plaintext
GOOGLE_OAUTH_CLIENT_ID=your_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost/db_name
MINIO_ENDPOINT=http://localhost:9000
```

### 5. Inicializa la base de datos

```bash
flask reset-db
flask seed-db
```

### 6. Ejecuta el servidor

```bash
flask run
```

### 7. Configura y ejecuta el Frontend (Vue.js)

```bash
cd web/public
npm install
npm run dev
```

---

## 🔍 Uso del Proyecto

- **Backend**: Accede en `http://localhost:5000`
- **Frontend**: Accede en `http://localhost:8080`

---

## 💪 Contribuciones

Las contribuciones son bienvenidas. Sigue estos pasos:

1. Haz un **fork** del repositorio.
2. Crea una nueva rama:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza los cambios y haz un commit:
   ```bash
   git commit -m "Añadir nueva funcionalidad X"
   ```
4. Haz un **push** a tu rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Crea un **Pull Request**.

---

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](https://opensource.org/licenses/MIT).

---

