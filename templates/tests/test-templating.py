import json
import os
import re
import pytest


# ==============================================================================
# CONFIGURACIÓN DINÁMICA DEL PROYECTO
# ==============================================================================
#
# Prioridad:
#
# 1. GENERATED_PROJECT_PATH -> proyecto generado explícitamente
# 2. GITHUB_WORKSPACE       -> GitHub Actions
# 3. Directorio actual      -> ejecución local
#
# ==============================================================================

PROJECT_ROOT = (
    os.getenv("GENERATED_PROJECT_PATH")
    or os.getenv("GITHUB_WORKSPACE")
    or os.getcwd()
)

PROJECT_ROOT = os.path.abspath(PROJECT_ROOT)


# ==============================================================================
# CONFIGURACIÓN CDC
# ==============================================================================

CDC_CONFIG_RELATIVE_PATH = os.path.join(
    "config-CDC",
    "application",
    "cdc_input_json_content.json",
)

CDC_CONFIG_PATH = os.path.join(
    PROJECT_ROOT,
    CDC_CONFIG_RELATIVE_PATH,
)


# ==============================================================================
# VARIABLES OBLIGATORIAS DEL CDC
# ==============================================================================
#
# Estas son las únicas variables que debe utilizar el template.
#
# El proyecto generado NO debe contener valores reales como:
#
# DEV
# PRE
# PRO
# ORACLE
# DB2
# MONGODB
# KAFKA
# CLIENTES_DB
#
# Debe contener variables:
#
# ${ENV}
# ${BBDD_ENGINE}
# ${BBDD_NAME}
# ...
#
# ==============================================================================

EXPECTED_VARIABLES = [
    "ENV",
    "REQUEST_TYPE",
    "PROJECT",
    "BBDD_ENGINE",
    "BBDD_NAME",
    "TABLES",
    "REPLICATION_TYPE",
    "TARGET_ENGINE",
    "KAFKA_CLUSTER_NAME",
    "KAFKA_IDENTITY_POOL",
    "KAFKA_TOPIC_PREFIX",
    "TARGET_INFO",
    "USER_NAME",
    "COST_CENTER",
]


# ==============================================================================
# ESTRUCTURA ESPERADA DEL JSON
# ==============================================================================

EXPECTED_ROOT_KEYS = [
    "env",
    "request_type",
    "project",
    "bbdd_engine",
    "bbdd_name",
    "tables",
    "replication_type",
    "target_engine",
    "kafka_cluster_name",
    "kafka_identity_pool",
    "kafka_topic_prefix",
    "target_info",
    "user_name",
    "cost_center",
]


# ==============================================================================
# PATRÓN DE VARIABLE
# ==============================================================================
#
# Ejemplos válidos:
#
# ${ENV}
# ${BBDD_ENGINE}
# ${BBDD_NAME}
# ${KAFKA_CLUSTER_NAME}
#
# Ejemplos inválidos:
#
# ${env}
# ${BbddEngine}
# ${BBDD-ENGINE}
# ENV
# DEV
# ORACLE
#
# ==============================================================================

VARIABLE_PATTERN = re.compile(
    r"^\$\{([A-Z][A-Z0-9_]*)\}$"
)


# ==============================================================================
# CLASE PRINCIPAL DE TEST
# ==============================================================================

class TestGeneratedCDCProject:

    # ==========================================================================
    # 1. EXISTENCIA DEL FICHERO CDC
    # ==========================================================================

    def test_cdc_input_file_exists(self):
        """
        Comprueba que exista el único fichero de configuración CDC esperado.
        """

        assert os.path.isfile(CDC_CONFIG_PATH), (
            "No se encontró el fichero de configuración CDC esperado:\n"
            f"{CDC_CONFIG_PATH}"
        )

    # ==========================================================================
    # 2. JSON VÁLIDO
    # ==========================================================================

    def test_cdc_input_json_is_valid(self):
        """
        Comprueba que cdc_input_json_content.json sea JSON válido.
        """

        self._assert_file_exists()

        with open(
            CDC_CONFIG_PATH,
            "r",
            encoding="utf-8",
        ) as f:

            try:
                json.load(f)

            except json.JSONDecodeError as exc:

                pytest.fail(
                    "El fichero "
                    "config-CDC/application/"
                    "cdc_input_json_content.json "
                    f"no contiene un JSON válido: {exc}"
                )

    # ==========================================================================
    # 3. ESTRUCTURA JSON
    # ==========================================================================

    def test_cdc_input_json_structure(self):
        """
        Valida que el JSON contenga exactamente la estructura CDC esperada.
        """

        data = self._load_json()

        actual_keys = list(data.keys())

        assert actual_keys == EXPECTED_ROOT_KEYS, (
            "La estructura del JSON CDC no es la esperada.\n"
            f"Esperadas: {EXPECTED_ROOT_KEYS}\n"
            f"Encontradas: {actual_keys}"
        )

    # ==========================================================================
    # 4. NO EXISTEN CAMPOS ANTIGUOS
    # ==========================================================================

    def test_no_legacy_configuration_fields(self):
        """
        Comprueba que no hayan quedado propiedades del modelo anterior.
        """

        data = self._load_json()

        legacy_fields = [
            "databases",
            "database",
            "targets",
            "runtime",
            "observability",
            "security",
            "quality",
            "paths",
            "metadata",
            "archetype",
        ]

        found = [
            field
            for field in legacy_fields
            if field in data
        ]

        assert not found, (
            "Se encontraron propiedades del modelo antiguo "
            "que ya no deben existir en "
            "cdc_input_json_content.json: "
            f"{found}"
        )

    # ==========================================================================
    # 5. TODAS LAS VARIABLES SON PLACEHOLDERS
    # ==========================================================================

    def test_all_cdc_values_are_variables(self):
        """
        Comprueba que todos los valores del JSON sean placeholders
        con formato ${VARIABLE_MAYUSCULA}.
        """

        data = self._load_json()

        for key in EXPECTED_ROOT_KEYS:

            value = data[key]

            # --------------------------------------------------------------
            # TABLES
            # --------------------------------------------------------------

            if key == "tables":

                assert isinstance(value, list), (
                    f"El campo '{key}' debe ser una lista."
                )

                assert len(value) == 1, (
                    f"El campo '{key}' debe contener "
                    "exactamente una variable."
                )

                self._assert_variable(
                    key,
                    value[0],
                )

            # --------------------------------------------------------------
            # RESTO DE CAMPOS
            # --------------------------------------------------------------

            else:

                self._assert_variable(
                    key,
                    value,
                )

    # ==========================================================================
    # 6. VARIABLES ESPERADAS
    # ==========================================================================

    def test_expected_variables_are_used(self):
        """
        Comprueba que cada propiedad utilice exactamente
        la variable esperada.
        """

        data = self._load_json()

        expected_mapping = {
            "env": "ENV",
            "request_type": "REQUEST_TYPE",
            "project": "PROJECT",
            "bbdd_engine": "BBDD_ENGINE",
            "bbdd_name": "BBDD_NAME",
            "tables": "TABLES",
            "replication_type": "REPLICATION_TYPE",
            "target_engine": "TARGET_ENGINE",
            "kafka_cluster_name": "KAFKA_CLUSTER_NAME",
            "kafka_identity_pool": "KAFKA_IDENTITY_POOL",
            "kafka_topic_prefix": "KAFKA_TOPIC_PREFIX",
            "target_info": "TARGET_INFO",
            "user_name": "USER_NAME",
            "cost_center": "COST_CENTER",
        }

        for json_key, variable_name in expected_mapping.items():

            if json_key == "tables":
                value = data[json_key][0]
            else:
                value = data[json_key]

            expected_value = (
                "${"
                + variable_name
                + "}"
            )

            assert value == expected_value, (
                f"El campo '{json_key}' debe utilizar "
                f"la variable '{expected_value}', "
                f"pero contiene: '{value}'"
            )

    # ==========================================================================
    # 7. NINGÚN VALOR HARDCODEADO
    # ==========================================================================

    def test_no_hardcoded_configuration_values(self):
        """
        Comprueba que ningún valor configurable haya sido hardcodeado.

        IMPORTANTE:
        No se busca simplemente que palabras como DEV, PRE, ORACLE
        o KAFKA no aparezcan en el fichero.

        Eso podría producir falsos positivos.

        Se valida que cada valor configurable sea exactamente:

            ${VARIABLE_MAYUSCULA}

        Ejemplos válidos:

            ${ENV}
            ${BBDD_ENGINE}
            ${BBDD_NAME}
            ${TARGET_ENGINE}

        Ejemplos inválidos:

            DEV
            PRE
            ORACLE
            KAFKA
            CLIENTES_DB
            ${env}
            ${BbddEngine}
            ${BBDD-ENGINE}
        """

        data = self._load_json()

        configurable_fields = {
            "env",
            "request_type",
            "project",
            "bbdd_engine",
            "bbdd_name",
            "tables",
            "replication_type",
            "target_engine",
            "kafka_cluster_name",
            "kafka_identity_pool",
            "kafka_topic_prefix",
            "target_info",
            "user_name",
            "cost_center",
        }

        for field in configurable_fields:

            assert field in data, (
                f"No existe el campo configurable '{field}' "
                "en cdc_input_json_content.json"
            )

            value = data[field]

            # --------------------------------------------------------------
            # TABLES
            # --------------------------------------------------------------

            if field == "tables":

                assert isinstance(value, list), (
                    f"El campo '{field}' debe ser una lista"
                )

                assert value, (
                    f"El campo '{field}' no puede estar vacío"
                )

                for index, table in enumerate(value):

                    assert isinstance(table, str), (
                        f"'{field}[{index}]' debe ser un string"
                    )

                    assert VARIABLE_PATTERN.fullmatch(table), (
                        f"El valor '{field}[{index}]' no es una "
                        f"variable válida: {table!r}. "
                        "Debe tener formato "
                        "${VARIABLE_MAYUSCULA}."
                    )

            # --------------------------------------------------------------
            # RESTO DE CAMPOS
            # --------------------------------------------------------------

            else:

                assert isinstance(value, str), (
                    f"El campo '{field}' debe ser un string"
                )

                assert VARIABLE_PATTERN.fullmatch(value), (
                    f"El valor del campo '{field}' no es una "
                    f"variable válida: {value!r}. "
                    "Debe tener formato "
                    "${VARIABLE_MAYUSCULA}."
                )

    # ==========================================================================
    # 8. NO EXISTE DIRECTORIO DB-CONNECTIONS
    # ==========================================================================

    def test_no_legacy_db_connections_directory(self):
        """
        Comprueba que no exista la antigua carpeta db-connections.
        """

        db_connections_path = os.path.join(
            PROJECT_ROOT,
            "config-CDC",
            "db-connections",
        )

        assert not os.path.exists(db_connections_path), (
            "La carpeta legacy 'config-CDC/db-connections' "
            "no debe existir en el nuevo modelo CDC:\n"
            f"{db_connections_path}"
        )

    # ==========================================================================
    # 9. NO EXISTEN FICHEROS KAFKA DE CONEXIÓN
    # ==========================================================================

    def test_no_legacy_kafka_connection_files(self):
        """
        Comprueba que no exista ningún fichero Kafka independiente
        perteneciente al modelo antiguo.
        """

        forbidden_files = [
            os.path.join(
                PROJECT_ROOT,
                "config-CDC",
                "target-connections",
                "kafka.yml",
            ),
            os.path.join(
                PROJECT_ROOT,
                "config-CDC",
                "target-connections",
                "kafka.yaml",
            ),
            os.path.join(
                PROJECT_ROOT,
                "config-CDC",
                "kafka.yml",
            ),
            os.path.join(
                PROJECT_ROOT,
                "config-CDC",
                "kafka.yaml",
            ),
        ]

        existing_files = [
            path
            for path in forbidden_files
            if os.path.exists(path)
        ]

        assert not existing_files, (
            "Se encontraron ficheros Kafka del modelo antiguo "
            "que ya no deben generarse:\n"
            + "\n".join(existing_files)
        )

    # ==========================================================================
    # 10. SOLO DEBE EXISTIR LA CONFIGURACIÓN APPLICATION ESPERADA
    # ==========================================================================

    def test_cdc_application_directory(self):
        """
        Comprueba que exista el directorio application y que contenga
        el fichero esperado.
        """

        application_dir = os.path.join(
            PROJECT_ROOT,
            "config-CDC",
            "application",
        )

        assert os.path.isdir(application_dir), (
            "No existe el directorio CDC application:\n"
            f"{application_dir}"
        )

        files = [
            file
            for file in os.listdir(application_dir)
            if os.path.isfile(
                os.path.join(
                    application_dir,
                    file,
                )
            )
        ]

        expected_file = "cdc_input_json_content.json"

        assert expected_file in files, (
            "No existe el fichero CDC esperado "
            f"'{expected_file}' en:\n"
            f"{application_dir}\n"
            f"Ficheros encontrados: {files}"
        )

        # No debe quedar el template FreeMarker sin procesar.
        assert "cdc_input_json_content.json.ftl" not in files, (
            "El fichero FreeMarker '.ftl' no debe existir "
            "en el proyecto generado:\n"
            f"{application_dir}"
        )

    # ==========================================================================
    # 11. NO EXISTEN VALORES FTL SIN RESOLVER
    # ==========================================================================

    def test_no_freemarker_syntax_remains(self):
        """
        Comprueba que no queden instrucciones de FreeMarker
        en el JSON generado.

        Debe existir:

            ${VARIABLE}

        Pero no:

            ${r"..."}
            <#if>
            <#list>
            <#assign>
            <@...>
        """

        self._assert_file_exists()

        with open(
            CDC_CONFIG_PATH,
            "r",
            encoding="utf-8",
        ) as f:

            content = f.read()

        forbidden_patterns = [
            r'\$\{r"',
            r"<#",
            r"</#",
            r"<@",
            r"</@",
        ]

        for pattern in forbidden_patterns:

            assert not re.search(
                pattern,
                content,
            ), (
                "El fichero generado contiene sintaxis "
                f"FreeMarker sin resolver: '{pattern}'"
            )

    # ==========================================================================
    # 12. COMPROBAR VARIABLES NO DUPLICADAS
    # ==========================================================================

    def test_no_duplicate_variables(self):
        """
        Comprueba que una misma variable CDC no se utilice accidentalmente
        en dos propiedades diferentes del JSON.
        """

        data = self._load_json()

        variables = []

        for key, value in data.items():

            if key == "tables":

                variables.extend(value)

            else:

                variables.append(value)

        extracted_variables = []

        for value in variables:

            match = VARIABLE_PATTERN.fullmatch(value)

            assert match, (
                f"Valor no válido como variable: {value}"
            )

            extracted_variables.append(
                match.group(1)
            )

        assert len(extracted_variables) == len(
            set(extracted_variables)
        ), (
            "Hay variables CDC duplicadas dentro "
            "del JSON de entrada: "
            f"{extracted_variables}"
        )

    # ==========================================================================
    # HELPERS
    # ==========================================================================

    @staticmethod
    def _assert_file_exists():
        """
        Comprueba que exista el fichero CDC.
        """

        assert os.path.isfile(CDC_CONFIG_PATH), (
            "No se encontró el fichero de configuración CDC:\n"
            f"{CDC_CONFIG_PATH}"
        )

    @staticmethod
    def _load_json():
        """
        Carga y devuelve el JSON CDC.
        """

        TestGeneratedCDCProject._assert_file_exists()

        with open(
            CDC_CONFIG_PATH,
            "r",
            encoding="utf-8",
        ) as f:

            try:
                return json.load(f)

            except json.JSONDecodeError as exc:

                pytest.fail(
                    "El fichero CDC contiene JSON inválido: "
                    f"{exc}"
                )

    @staticmethod
    def _assert_variable(
        field_name,
        value,
    ):
        """
        Valida que un valor tenga exactamente:

            ${VARIABLE_MAYUSCULAS}

        y que la variable esté definida en EXPECTED_VARIABLES.
        """

        assert isinstance(value, str), (
            f"El campo '{field_name}' debe ser string, "
            f"pero es: {type(value).__name__}"
        )

        match = VARIABLE_PATTERN.fullmatch(value)

        assert match, (
            f"El campo '{field_name}' debe contener "
            "una variable con formato ${VARIABLE_MAYUSCULAS}, "
            f"pero contiene: '{value}'"
        )

        variable_name = match.group(1)

        assert variable_name in EXPECTED_VARIABLES, (
            f"La variable '{variable_name}' utilizada en "
            f"'{field_name}' no está definida como variable CDC válida."
        )


# ==============================================================================
# EJECUCIÓN DIRECTA
# ==============================================================================

if __name__ == "__main__":
    pytest.main(
        [
            "-v",
            __file__,
        ]
    )
