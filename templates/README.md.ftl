# ${BBDD_ENGINE?upper_case} - ${ENV?upper_case}

## 🖥️ Descripción

Este proyecto se ha generado utilizando ArqRef (Reference Architecture MAPFRE). Puedes encontrar documentación y ayuda en [Marketplace MAPFRE](https://www.marketplace.mapfre.com).

Este repositorio contiene el arquetipo CDC para generar los ficheros de configuración de replicación de datos mediante plantillas **FreeMarker** (`.ftl`). Permite parametrizar la configuración del origen de datos, las conexiones de base de datos y el destino de replicación, como Kafka.

Los parámetros utilizados para identificar la generación son:

- **ENV:** entorno de despliegue (`DEV`, `PRE` o `PRO`).
- **BBDD_ENGINE:** motor de base de datos (`ORACLE`, `MONGODB` o `DB2`).

## 📁 Estructura del proyecto

```text
├── .github
│   └── workflows
│       ├── merge-commit.yml
│       └── pull-request.yml
├── config-CDC
│   ├── application
│   │   └── cdc_input_json_content.json.ftl
│   ├── db-connections
│   │   └── db-connections-${BBDD_ENGINE}.yml.ftl
│   └── target-connections
│       └── kafka.yml.ftl
├── spectral
│   └── rules
│       └── structure
├── tests
├── CONTRIBUTING.md
└── README.md
```

La estructura representa los principales componentes del arquetipo CDC. La ubicación y extensión de los ficheros definitivos dependerán de la estructura configurada en el repositorio fuente.

## ⚙️ Componentes principales

- **`config-CDC/application/`**: contiene la plantilla JSON de entrada para definir los parámetros de replicación CDC.
- **`config-CDC/db-connections/`**: contiene las plantillas de conexión a la base de datos de origen, seleccionadas según `BBDD_ENGINE`.
- **`config-CDC/target-connections/`**: contiene la plantilla de configuración del destino, como Kafka.
- **`spectral/rules/structure/`**: contiene las reglas Spectral utilizadas para validar la estructura de los ficheros de configuración.
- **`tests/`**: contiene las pruebas automatizadas de validación y renderizado de las plantillas.
- **`.github/workflows/pull-request.yml`**: valida los cambios propuestos mediante el proceso de integración continua.
- **`.github/workflows/merge-commit.yml`**: gestiona el proceso posterior a la integración de los cambios y la publicación del artefacto CDC.

## 🔄 Flujo de CI

### Pull Request: validación de cambios

El workflow de Pull Request se ejecuta cuando se crea o actualiza una solicitud de integración admitida por las reglas de ramas.

1. **Validación de ramas:** comprueba las combinaciones permitidas:
   - `feature/*` → `develop`
   - `hotfix/*` → `main`
2. **Validación del workflow:** comprueba la estructura y configuración del workflow.
3. **Preparación del entorno:** obtiene los datos y tokens necesarios para ejecutar las validaciones.
4. **Validación de plantillas:** comprueba la estructura y el renderizado de los ficheros de configuración.
5. **Pruebas automatizadas:** ejecuta los tests definidos para el arquetipo.
6. **Validación Spectral:** comprueba los ficheros de configuración mediante las reglas establecidas.
7. **Publicación del artefacto:** genera y publica el ZIP del arquetipo cuando se cumplen las condiciones definidas en el workflow.
8. **Finalización:** registra el resultado de la ejecución y realiza las tareas de limpieza previstas.

### Merge Commit: generación y publicación

El workflow de Merge Commit se ejecuta después de integrar los cambios en las ramas de destino.

- **Integración en `develop`:** genera el paquete de tipo *Snapshot*.
- **Integración en `main`:** genera el paquete de tipo *Release*.
- **Empaquetado:** genera el ZIP del arquetipo con los ficheros necesarios para su distribución.
- **Publicación:** publica el paquete en Azure Artifacts para que pueda consumirse en las siguientes fases del proceso.

## 🧩 Generación del arquetipo

El generador procesa las plantillas FreeMarker y utiliza `ENV` y `BBDD_ENGINE` para identificar el entorno y seleccionar el motor de base de datos.

Los valores de ejemplo son:

| Variable | Ejemplo |
|---|---|
| `ENV` | `DEV` |
| `BBDD_ENGINE` | `ORACLE` |

El resto de los parámetros de configuración se conservan como variables de plantilla cuando corresponde, para que puedan resolverse en las fases posteriores del proceso CDC.

## 📝 Consideraciones

- Los nombres de las ramas y los eventos admitidos deben coincidir con los configurados en los workflows.
- Los nombres de los directorios documentados deben mantenerse alineados con la estructura real del repositorio.
- Las validaciones y publicaciones efectivas dependen de los pasos configurados en cada workflow.
