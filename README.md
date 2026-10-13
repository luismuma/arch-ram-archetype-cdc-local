# arch-ram-archetype-db-relational

![Archetype](https://img.shields.io/badge/Archetype-DB%20Relational-blue)
![Templates](https://img.shields.io/badge/Templates-FreeMarker-0969DA)
![Migration](https://img.shields.io/badge/Migration-Liquibase-orange)
[![Publish](https://github.com/mapfre-tech/arch-ram-archetype-db-relational/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/mapfre-tech/arch-ram-archetype-db-relational/actions/workflows/publish.yml)
[![Labeler PR](https://github.com/mapfre-tech/arch-ram-archetype-db-relational/actions/workflows/labeler-pr.yml/badge.svg?branch=main)](https://github.com/mapfre-tech/arch-ram-archetype-db-relational/actions/workflows/labeler-pr.yml)
[![Labeler Merge](https://github.com/mapfre-tech/arch-ram-archetype-db-relational/actions/workflows/labeler-merge-conflict.yml/badge.svg?branch=main)](https://github.com/mapfre-tech/arch-ram-archetype-db-relational/actions/workflows/labeler-merge-conflict.yml)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](version.txt)
![Repo](https://img.shields.io/badge/Repo-Privado-grey)
![SemVer](https://img.shields.io/badge/SemVer-✓-brightgreen)

Arquetipo de Base de Datos Relacional para la Arquitectura de Referencia de MAPFRE

## 🎯 Descripción

Este repositorio contiene un **arquetipo** diseñado para generar proyectos de construccion de ficheros de configuracion a base de datos(db_connections.yml), kafka (kafka.yml) y application (application.yml) para ser inyectados en el proceso de replicacion de datos CDC, siguiendo los estándares y mejores prácticas de la Arquitectura de Referencia de MAPFRE.

El arquetipo utiliza **FreeMarker** como motor de plantillas para generar automáticamente la estructura completa de un proyecto de base de datos, incluyendo:

- Configuraciones de Liquibase para gestión de esquemas
- Archivos de propiedades para diferentes entornos
- Estructura de carpetas estandarizada
- Documentación base del proyecto

## 🏗️ ¿Qué es un Arquetipo?

Un arquetipo es una plantilla o patrón que define la estructura base de un proyecto. En este caso, cuando se utiliza este arquetipo, se genera automáticamente un proyecto completo de base de datos relacional con:

- **Gestión de esquemas** mediante Liquibase
- **Soporte multi-base de datos** (MySQL, PostgreSQL, Oracle, DB2)
- **Configuración Docker** para desarrollo local
- **Integración continua** (opcional, según necesidades del proyecto)
- **Documentación completa** y guías de uso

## 📁 Estructura del Arquetipo

```text
arch-ram-archetype-db-relational/
├── README.md                           # Este archivo
├── CHANGELOG.md                        # Registro de cambios del arquetipo
├── CONTRIBUTING.md                     # Guía de contribución
├── version.txt                         # Versión del arquetipo
└── templates/                          # Plantillas FreeMarker
    ├── CHANGELOG.md                    # Template del changelog del proyecto
    ├── CONTRIBUTING.md                 # Template de guía de contribución
    ├── README.md.ftl                   # Template del README del proyecto
    ├── project-manifest.json.ftl       # Manifiesto del proyecto generado
    ├── local/                          # Templates para desarrollo local
    │   └── database.properties.ftl     # Configuración de conexión a BD
    └── sources/                        # Templates de migraciones
        └── database-template/          # Plantillas para bases de datos
            ├── master.xml              # Punto de entrada a las migraciones
            └── changelogs/
                └── 0.0.0/
                    └── init-schema.xml.ftl  # Migración inicial de schema
```

### 🔗 Referencias clave del arquetipo

- [templates/sources/database-template/master.xml](templates/sources/database-template/master.xml)
- [templates/sources/database-template/changelogs/0.0.0/init-schema.xml.ftl](templates/sources/database-template/changelogs/0.0.0/init-schema.xml.ftl)
- [templates/local/database.properties.ftl](templates/local/database.properties.ftl)
- [templates/project-manifest.json.ftl](templates/project-manifest.json.ftl)

## 🔧 Tecnologías Utilizadas

- **FreeMarker**: Motor de plantillas para generar archivos dinámicos
- **Liquibase**: Gestión y versionado de esquemas de base de datos
- **Docker**: Contenedorización para desarrollo local
- **GitHub Actions**: CI/CD para integración y despliegue continuo

## 🚀 Cómo Usar Este Arquetipo

### Prerrequisitos

- Acceso al sistema de arquetipos de MAPFRE
- Conocimientos básicos de Liquibase
- Docker (opcional, para desarrollo local)

### Generación de Proyecto

1. **Accede al generador de arquetipos** de MAPFRE
2. **Selecciona** el arquetipo `arch-ram-archetype-db-relational`
3. **Configura los parámetros**:
   - Nombre del componente
   - Descripción del proyecto
   - Bases de datos a incluir (nombre y tipo)
   - Versión inicial
4. **Genera el proyecto** - se creará automáticamente con toda la estructura necesaria

#### Validación de migraciones con Liquibase (local)

```bash
# Variables de conexión (ejemplo PostgreSQL)
export LIQUIBASE_URL="jdbc:postgresql://localhost:5432/catalog"
export LIQUIBASE_USERNAME="postgres"
export LIQUIBASE_PASSWORD="postgres"

# Aplicar migraciones del master.xml generado
liquibase \
    --url="$LIQUIBASE_URL" \
    --username="$LIQUIBASE_USERNAME" \
    --password="$LIQUIBASE_PASSWORD" \
    --changeLogFile="sources/catalog/master.xml" \
    update
```

Nota: Ajusta `sources/<db>/master.xml` al nombre real de la base de datos generada.

### Parámetros de Configuración

El arquetipo acepta los siguientes parámetros mediante `specificConfig`:

- `version`: Versión inicial del proyecto
- `databases`: Array de bases de datos a incluir
  - `databaseName`: Nombre de la base de datos
  - `databaseType`: Tipo (mysql, postgresql, oracle, db2)

#### Ejemplo de `specificConfig`

```json
{
    "version": "0.1.0",
    "databases": [
        { "databaseName": "catalog", "databaseType": "postgresql" },
        { "databaseName": "billing", "databaseType": "mysql" }
    ]
}
```

### Estructura del Proyecto Generado

Una vez generado, el proyecto tendrá la siguiente estructura:

```text
mi-proyecto-db/
├── .github/workflows/           # CI/CD workflows
├── sources/                     # Código fuente de esquemas
│   └── [database-name]/        # Por cada BD configurada
├── local/                       # Configuración desarrollo local
├── project-manifest.json       # Manifiesto del proyecto
├── README.md                    # Documentación del proyecto
├── CHANGELOG.md                 # Registro de cambios
└── CONTRIBUTING.md              # Guía de contribución
```

Dentro de cada base de datos se generará un primer changelog **0.0.0** que contiene la inicializacion del schema en la base de datos, necesaria tanto para el desarrollo local como para las validaciones en el CI de las migraciones aplicadas.

## 🎯 Casos de Uso

Este arquetipo es ideal para:

- **Nuevos proyectos** que requieran bases de datos relacionales
- **Estandarización** de la gestión de esquemas en MAPFRE
- **Proyectos multi-base de datos** con diferentes motores
- **Equipos** que quieran adoptar las mejores prácticas de  MAPFRE
- **Migración** de proyectos existentes a estándares MAPFRE

## 📋 Características del Proyecto Generado

Los proyectos generados con este arquetipo incluyen:

- ✅ **Gestión de esquemas** con Liquibase
- ✅ **Soporte multi-BD** (MySQL, PostgreSQL, Oracle, DB2)  
- ✅ **Desarrollo local** con Docker
- ✅ **CI/CD** con GitHub Actions
- ✅ **Documentación** completa y estructurada
- ✅ **Buenas prácticas** de versionado y rollback
- ✅ **Scripts** de automatización
- ✅ **Ejemplos** de uso y configuración

## 🔄 Versionado y Actualizaciones

Este arquetipo sigue el versionado semántico:

- **Major**: Cambios que rompen compatibilidad
- **Minor**: Nuevas características compatibles
- **Patch**: Correcciones de errores

Para ver los cambios en cada versión, consulta el [CHANGELOG.md](CHANGELOG.md).

### Estado de CI

El estado del pipeline se muestra arriba mediante el badge de **CI**. Si el nombre del workflow difiere (p. ej., `build.yml` o `test.yml`), actualiza el enlace del badge a:

```text
https://github.com/<owner>/<repo>/actions/workflows/<workflow>.yml/badge.svg?branch=<branch>
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Lee la [Guía de Contribución](CONTRIBUTING.md)
2. Sigue la estrategia de branching definida
3. Asegúrate de que las plantillas FreeMarker funcionen correctamente
4. Incluye documentación para nuevas características

## 📞 Soporte

Para soporte técnico y consultas:

- **Documentación**: [MAPFRE Marketplace](https://www.marketplace.mapfre.com)
- **Issues**: Usa la sección de Issues de este repositorio
- **Contribuciones**: Consulta [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 Licencia

```text
Copyright (c) MAPFRE DevOps Platform
```

---

**Nota**: Este es un arquetipo para generar proyectos. El código real de bases de datos se genera en el proyecto destino usando las plantillas FreeMarker incluidas en la carpeta `templates/`.

---

## 🤖 Agentes de IA

Este repositorio incluye soporte para agentes de codificación con IA (GitHub Copilot, Claude Code, OpenCode).
Antes de generar o modificar código, el agente debe cargar el skill `database-relacional`,
que contiene las convenciones, patrones y buenas prácticas de este arquetipo
(Liquibase · PostgreSQL / Oracle / MySQL / DB2).

| Herramienta | Fichero |
|---|---|
| Claude Code | `templates/CLAUDE.md` + `templates/.claude/settings.json` |
| OpenCode | `templates/AGENTS.md` |
| GitHub Copilot | `templates/.github/copilot-instructions.md` |

Consulta [README.agents.md](README.agents.md) para las instrucciones de instalación (`clai` + configuración del skill).