# ${BBDD_ENGINE?upper_case} - ${ENV?upper_case}

## 🖥️ Descripción

Este proyecto se ha generado utilizando ArqRef (Reference Architecture MAPFRE). Puedes encontrar documentación y ayuda en el [Marketplace MAPFRE](https://www.marketplace.mapfre.com).

Contiene el arquetipo CDC para generar la configuración de replicación de datos mediante plantillas **FreeMarker** (`.ftl`), parametrizando el origen, las conexiones de base de datos y el destino.

- **ENV:** entorno (`DEV`, `PRE`, `PRO`).
- **BBDD_ENGINE:** motor de base de datos (`ORACLE`, `MONGODB`, `DB2`).

## 📁 Estructura del proyecto

```text
├── .github
│   └── workflows
│       ├── merge-commit.yml
│       └── pull-request.yml
├── config-CDC
│   └── application
│       └── cdc_input_json_content.json.ftl
├── tests
├── CONTRIBUTING.md
└── README.md

⚙️ Componentes principales
config-CDC/application/: plantilla JSON de entrada para definir los parámetros de replicación CDC.

tests/: pruebas automatizadas de validación y renderizado de plantillas.

.github/workflows/pull-request.yml: valida los cambios en los Pull Requests (feature/* → develop, hotfix/* → main).

.github/workflows/merge-commit.yml: gestiona la integración continua, empaquetado dual (arquetipo + ZIP de configuración específica con db_connection_names.yml), y publicación en Azure Artifacts.

🔄 Flujo de CI
Pull Request
Valida la estructura de ramas permitidas, ejecuta tests automatizados y comprueba el renderizado de los ficheros.

Merge Commit
Se ejecuta tras la fusión en ramas principales (develop para paquetes Snapshot y main/master para Release):

Generación de tokens centralizados y validación del esquema.

Descarga y filtrado dinámico del inventario CDC según BBDD_ENGINE y ENV.

Creación del ZIP del arquetipo y del paquete específico de despliegue (cdc-deployment-package.zip).

Publicación en el feed correspondiente de Azure Artifacts y subida a GitHub Actions.

Revocación segura de tokens.
