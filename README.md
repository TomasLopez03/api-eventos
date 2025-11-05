# 🚀 API RESTful para Gestión de Eventos

[![Estado del Build](https://img.shields.io/badge/Status-Activo-brightgreen)]([https://github.com/TomasLopez03/api-eventos.git])
[![Framework](https://img.shields.io/badge/Framework-Django%20REST%20Framework-blue)](https://www.djangoproject.com/)
[![Licencia](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🌟 Visión General

Esta API RESTful, construida con **Django REST Framework (DRF)**, permite la gestión completa de eventos, incluyendo la organización, registro de asistentes y publicación de comentarios. El diseño sigue los principios REST, utilizando métodos HTTP y códigos de estado semánticos.

### Características Clave

* **Modelado de Recursos:** Gestión de `Eventos`, `Asistentes` y `Comentarios`.
* **Autenticación:** Implementada con **Simple JWT** (JSON Web Tokens).
* **Diseño RESTful:** Uso de `PUT` para operaciones idempotentes (ej. registro de asistencia).
* **Documentación:** Generada automáticamente con **drf-spectacular** (Swagger UI y Redoc).
* **Filtrado y Paginación:** Implementación de paginación por número de página y `Limit/Offset`.

---

## 🛠️ Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

* Python 3.8+
* Git

## ⚙️ Configuración del Proyecto

Sigue estos pasos para clonar el repositorio y configurar el entorno local.

### 1. Clonar el Repositorio

```
git clone https://github.com/TomasLopez03/api-eventos.git
cd api-eventos
```
### 2. Crear y Activar el Entorno Virtual

```
python -m venv venv
```

### 3. Instalar Dependencias

```
pip install -r requeriments.txt
```

### 4. Configuración de la Base de Datos

```
cd eventhub
python manage.py makemigrations
python manage.py migrate
```

### 5. Ejecutar el Servidor

```
python manage.py runserver
```

# 📚 Documentacion Interactiva (Swagger)
Todos los endpoints, esquemas de datos y códigos de error estan detallados en la documentación
interactiva:

* **Swagger UI:** `http://localhost:8000/api/schema/swagger-ui/`

### Flujo de Autenticacion (JWT)
Todos los endpoints de gestion de eventos requieren el `Acces Token` en el encabezado
`Authorization: Bearer <token>`

* `POST  /api/v1/usarios/registo/` : Crea un nuevo usuario en la DB.
* `POST /api/token/` : Obtiene el `access` y `refresh` token.
* `POST /api/token/refresh/` : Renueva el token de acceso.

# 🤝🏻 Contribuciones

Si encuentras un erro o tienes alguna sugerencia, siente libre de abrir un issue o enviar una 
pull request









