
import json
import os
import re
import pytest


# ==============================================================================
# CONFIGURACIÓN DINÁMICA DEL PROYECTO
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
# VALORES LITERALES PERMITIDOS
# ==============================================================================

ALLOWED_ENVIRONMENTS = {
    "DEV",
    "PRE",
    "PRO",
}

ALLOWED_BBDD_ENGINES = {
    "ORACLE",
    "DB2",
    "MONGODB",
}


# ==============================================================================
# VARIABLES ESPERADAS DEL CDC
# ==============================================================================

EXPECTED_VARIABLES = [
    "REQUEST_TYPE",
    "PROJECT",
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
    "CHANGE_NUMBER",
    "COMMENTS",
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
    "change_number",
    "comments",
]


# ==============================================================================
# MAPEO ENTRE CAMPOS JSON Y VARIABLES
# ==============================================================================

EXPECTED_VARIABLE_MAPPING = {
    "request_type": "REQUEST_TYPE",
    "project": "PROJECT",
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
    "change_number": "CHANGE_NUMBER",
    "comments": "COMMENTS",
}


# ==============================================================================
# PATRÓN DE VARIABLE
# ==============================================================================

VARIABLE_PATTERN = re.compile(
    r"^\$\{([A-Z][A-Z0-9_]*)\}$"
)


# ==============================================================================
# CLASE PRINCIPAL DE TEST
# ==============================================================================

class TestGeneratedCDCProject:

    # ==========================================================================
    # 1. EXISTENCIA DEL FICHERO
    # ==========================================================================

    def test_cdc_input_file_exists(self):
        """Comprueba que exista el fichero de configuración CDC."""

        assert os.path.isfile(CDC_CONFIG_PATH), (
            "No se encontró el fichero de configuración CDC:\n"
            f"{CDC_CONFIG_PATH}"
        )

    # ==========================================================================
    # 2. JSON VÁLIDO
    # ==========================================================================

    def test_cdc_input_json_is_valid(self):
        """Comprueba que el fichero contiene JSON válido."""

        data = self._load_json()

        assert isinstance(data, dict), (
            "El contenido del JSON CDC debe ser un objeto JSON."
        )

    # ==========================================================================
    # 3. ESTRUCTURA JSON
    # ==========================================================================

    def test_cdc_input_json_structure(self):
        """Valida las propiedades esperadas y su orden."""

        data = self._load_json()

        actual_keys = list(data.keys())

        assert actual_keys == EXPECTED_ROOT_KEYS, (
            "La estructura del JSON CDC no es la esperada.\n"
            f"Esperadas: {EXPECTED_ROOT_KEYS}\n"
            f"Encontradas: {actual_keys}"
        )

    # ==========================================================================
    # 4. NO EXISTEN CAMPOS LEGACY
    # ==========================================================================

    def test_no_legacy_configuration_fields(self):
        """Comprueba que no existan propiedades del modelo anterior."""

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
            "Se encontraron propiedades del modelo antiguo: "
            f"{found}"
        )

    # ==========================================================================
    # 5. TODOS LOS VALORES SON VÁLIDOS
    # ==========================================================================

    def test_all_cdc_values_are_variables(self):
        """
        Valida que env y bbdd_engine tengan valores permitidos.
        El resto de campos deben contener placeholders.
        """

        data = self._load_json()

        assert data["env"] in ALLOWED_ENVIRONMENTS, (
            f"El campo 'env' debe ser uno de "
            f"{sorted(ALLOWED_ENVIRONMENTS)}, "
            f"pero contiene: {data['env']!r}"
        )

        assert data["bbdd_engine"] in ALLOWED_BBDD_ENGINES, (
            f"El campo 'bbdd_engine' debe ser uno de "
            f"{sorted(ALLOWED_BBDD_ENGINES)}, "
            f"pero contiene: {data['bbdd_engine']!r}"
        )

        for key in EXPECTED_VARIABLE_MAPPING:
            value = data[key]

            if key == "tables":
                assert isinstance(value, list), (
                    "El campo 'tables' debe ser una lista."
                )

                assert len(value) == 1, (
                    "El campo 'tables' debe contener exactamente "
                    "una variable."
                )

                self._assert_variable(key, value[0])

            else:
                self._assert_variable(key, value)

    # ==========================================================================
    # 6. VARIABLES ESPERADAS
    # ==========================================================================

    def test_expected_variables_are_used(self):
        """Comprueba la correspondencia entre campos y variables."""

        data = self._load_json()

        for json_key, variable_name in EXPECTED_VARIABLE_MAPPING.items():

            if json_key == "tables":
                value = data[json_key][0]
            else:
                value = data[json_key]

            expected_value = f"${{{variable_name}}}"

            assert value == expected_value, (
                f"El campo '{json_key}' debe utilizar "
                f"'{expected_value}', pero contiene: {value!r}"
            )

    # ==========================================================================
    # 7. NINGÚN VALOR CONFIGURABLE NO AUTORIZADO
    # ==========================================================================

    def test_no_hardcoded_configuration_values(self):
        """
        Permite valores literales únicamente en:
        - env: DEV, PRE, PRO.
        - bbdd_engine: ORACLE, DB2, MONGODB.

        Todos los demás valores deben ser placeholders.
        """

        data = self._load_json()

        assert data["env"] in ALLOWED_ENVIRONMENTS, (
            f"Valor no permitido en 'env': {data['env']!r}. "
            f"Valores válidos: {sorted(ALLOWED_ENVIRONMENTS)}"
        )

        assert data["bbdd_engine"] in ALLOWED_BBDD_ENGINES, (
            f"Valor no permitido en 'bbdd_engine': "
            f"{data['bbdd_engine']!r}. "
            f"Valores válidos: {sorted(ALLOWED_BBDD_ENGINES)}"
        )

        for field in EXPECTED_VARIABLE_MAPPING:

            assert field in data, (
                f"No existe el campo configurable '{field}'."
            )

            value = data[field]

            if field == "tables":
                assert isinstance(value, list), (
                    "El campo 'tables' debe ser una lista."
                )

                assert value, (
                    "El campo 'tables' no puede estar vacío."
                )

                for index, table in enumerate(value):
                    assert isinstance(table, str), (
                        f"'tables[{index}]' debe ser un string."
                    )

                    assert VARIABLE_PATTERN.fullmatch(table), (
                        f"'tables[{index}]' contiene un valor no "
                        f"permitido: {table!r}. "
                        "Debe tener formato ${VARIABLE_MAYUSCULA}."
                    )

            else:
                assert isinstance(value, str), (
                    f"El campo '{field}' debe ser un string."
                )

                assert VARIABLE_PATTERN.fullmatch(value), (
                    f"El campo '{field}' contiene un valor no "
                    f"permitido: {value!r}. "
                    "Debe tener formato ${VARIABLE_MAYUSCULA}."
                )

    # ==========================================================================
    # 8. NO EXISTE DIRECTORIO DB-CONNECTIONS LEGACY
    # ==========================================================================

    def test_no_legacy_db_connections_directory(self):
        """Comprueba que no exista la carpeta antigua db-connections."""

        path = os.path.join(
            PROJECT_ROOT,
            "config-CDC",
            "db-connections",
        )

        assert not os.path.exists(path), (
            "La carpeta legacy no debe existir:\n"
            f"{path}"
        )

    # ==========================================================================
    # 9. NO EXISTEN FICHEROS KAFKA LEGACY
    # ==========================================================================

    def test_no_legacy_kafka_connection_files(self):
        """Comprueba que no existan los ficheros Kafka antiguos."""

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
            "Se encontraron ficheros Kafka legacy:\n"
            + "\n".join(existing_files)
        )

    # ==========================================================================
    # 10. DIRECTORIO APPLICATION
    # ==========================================================================

    def test_cdc_application_directory(self):
        """Comprueba que exista el directorio y el JSON generado."""

        application_dir = os.path.join(
            PROJECT_ROOT,
            "config-CDC",
            "application",
        )

        assert os.path.isdir(application_dir), (
            f"No existe el directorio:\n{application_dir}"
        )

        files = [
            file
            for file in os.listdir(application_dir)
            if os.path.isfile(os.path.join(application_dir, file))
        ]

        expected_file = "cdc_input_json_content.json"

        assert expected_file in files, (
            f"No existe '{expected_file}' en {application_dir}. "
            f"Ficheros encontrados: {files}"
        )

        assert "cdc_input_json_content.json.ftl" not in files, (
            "El proyecto generado no debe contener el template .ftl."
        )

    # ==========================================================================
    # 11. NO EXISTE SINTAXIS FREEMARKER SIN RESOLVER
    # ==========================================================================

    def test_no_freemarker_syntax_remains(self):
        """Comprueba que no queden instrucciones FreeMarker sin resolver."""

        self._assert_file_exists()

        with open(CDC_CONFIG_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        forbidden_patterns = [
            r'\$\{r"',
            r"<#",
            r"</#",
            r"<@",
            r"</@",
        ]

        for pattern in forbidden_patterns:
            assert not re.search(pattern, content), (
                "El fichero generado contiene sintaxis "
                f"FreeMarker sin resolver: {pattern!r}"
            )

    # ==========================================================================
    # 12. NO EXISTEN VARIABLES DUPLICADAS
    # ==========================================================================

    def test_no_duplicate_variables(self):
        """
        Comprueba que las variables sean válidas y no se repitan.
        env y bbdd_engine son valores literales y no se incluyen
        en la comprobación de placeholders.
        """

        data = self._load_json()

        extracted_variables = []

        for key in EXPECTED_VARIABLE_MAPPING:
            value = data[key]

            values = value if key == "tables" else [value]

            assert isinstance(values, list), (
                f"El campo '{key}' debe contener un string "
                "o una lista de strings."
            )

            for item in values:
                match = (
                    VARIABLE_PATTERN.fullmatch(item)
                    if isinstance(item, str)
                    else None
                )

                assert match, (
                    f"Valor no válido como variable en "
                    f"'{key}': {item!r}"
                )

                extracted_variables.append(match.group(1))

        assert len(extracted_variables) == len(set(extracted_variables)), (
            "Hay variables CDC duplicadas: "
            f"{extracted_variables}"
        )

    # ==========================================================================
    # HELPERS
    # ==========================================================================

    @staticmethod
    def _assert_file_exists():
        """Comprueba que exista el fichero CDC."""

        assert os.path.isfile(CDC_CONFIG_PATH), (
            "No se encontró el fichero de configuración CDC:\n"
            f"{CDC_CONFIG_PATH}"
        )

    @staticmethod
    def _load_json():
        """Carga y devuelve el JSON CDC."""

        TestGeneratedCDCProject._assert_file_exists()

        with open(CDC_CONFIG_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as exc:
                pytest.fail(
                    f"El fichero CDC contiene JSON inválido: {exc}"
                )

    @staticmethod
    def _assert_variable(field_name, value):
        """Valida el formato y el nombre de una variable CDC."""

        assert isinstance(value, str), (
            f"El campo '{field_name}' debe ser string, "
            f"pero es {type(value).__name__}."
        )

        match = VARIABLE_PATTERN.fullmatch(value)

        assert match, (
            f"El campo '{field_name}' debe contener una variable "
            f"${{VARIABLE_MAYUSCULAS}}, pero contiene: {value!r}"
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
    pytest.main(["-v", __file__])
