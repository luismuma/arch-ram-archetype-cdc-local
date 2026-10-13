<#-- ============================================================
     project-manifest.json.ftl
     Manifiesto de proyecto CDC usando directamente variables en mayúsculas
     ============================================================ -->

{
  "version": "${VERSION!"1.0.0"?json_string}",
  "name": "${(BBDD_ENGINE!"ORACLE")?upper_case?json_string}-${(BBDD_NAME!"")?upper_case?json_string}_${(ENV!"DEV")?upper_case?json_string}",
  "displayName": "${DISPLAY_NAME!("CDC " + (BBDD_ENGINE!"ORACLE")?upper_case + " - " + (BBDD_NAME!"")?upper_case + " - " + (ENV!"DEV")?upper_case)?json_string}",
  "description": "${DESCRIPTION!("Configuración CDC para " + (BBDD_NAME!"")?upper_case + " en entorno " + (ENV!"DEV")?upper_case)?json_string}",
  "status": "${STATUS!"draft"?json_string}",

  "archetype": {
    "name": "cdc-database-to-kafka",
    "version": "1.6.0",
    "generator": {
      "name": "${GENERATOR_NAME!"cdc-project-generator"?json_string}",
      "version": "${GENERATOR_VERSION!"1.0.0"?json_string}"
    }
  },

  "metadata": {
    "projectId": "${(BBDD_ENGINE!"ORACLE")?lower_case?json_string}-${(BBDD_NAME!"")?lower_case?json_string}-${(ENV!"DEV")?lower_case?json_string}",
    "domain": "${DOMAIN!"data-platform"?json_string}",
    "subdomain": "${SUBDOMAIN!"change-data-capture"?json_string}",
    "criticality": "${CRITICALITY!"medium"?json_string}",
    "lifecycle": "${LIFECYCLE!"active"?json_string}",

    "generated": {
      "at": "${GENERATED_AT!""?json_string}",
      "by": "${GENERATED_BY!""?json_string}",
      "requestId": "${REQUEST_ID!""?json_string}",
      "changeId": "${CHANGE_ID!""?json_string}",
      "ticketId": "${TICKET_ID!""?json_string}"
    },

    "repository": {
      "url": "${GIT_REPOSITORY!""?json_string}",
      "projectPath": "${GIT_PROJECT_PATH!""?json_string}",
      "branch": "${GIT_BRANCH!""?json_string}",
      "commitSha": "${GIT_COMMIT_SHA!""?json_string}",
      "pipelineId": "${GIT_PIPELINE_ID!""?json_string}",
      "pipelineUrl": "${GIT_PIPELINE_URL!""?json_string}"
    },

    "owners": {
      "technicalOwner": "${TECHNICAL_OWNER!""?json_string}",
      "businessOwner": "${BUSINESS_OWNER!""?json_string}",
      "supportGroup": "${SUPPORT_GROUP!""?json_string}",
      "securityOwner": "${SECURITY_OWNER!""?json_string}",
      "contactEmail": "${CONTACT_EMAIL!""?json_string}"
    },

    "labels": {
      "component": "${(BBDD_ENGINE!"ORACLE")?upper_case?json_string}-${(BBDD_NAME!"")?upper_case?json_string}_${(ENV!"DEV")?upper_case?json_string}",
      "databaseEngine": "${(BBDD_ENGINE!"ORACLE")?upper_case?json_string}",
      "databaseName": "${(BBDD_NAME!"")?upper_case?json_string}",
      "environment": "${(ENV!"DEV")?upper_case?json_string}",
      "managedBy": "freemarker-template",
      "projectType": "change-data-capture"
    }
  },

  "databases": {
    "${(BBDD_NAME!"")?upper_case?json_string}_${(ENV!"DEV")?upper_case?json_string}": {
      "id": "${(BBDD_NAME!"")?upper_case?json_string}_${(ENV!"DEV")?upper_case?json_string}",
      "dbname": "${(BBDD_NAME!"")?upper_case?json_string}_${(ENV!"DEV")?upper_case?json_string}",
      "sourceDatabase": "${SOURCE_DATABASE!(BBDD_NAME!"")?upper_case?json_string}",
      "type": "${(BBDD_ENGINE!"ORACLE")?lower_case?json_string}",

      "connection": {
        "alias": "${SOURCE_CONNECTION_ALIAS!((BBDD_ENGINE!"ORACLE")?lower_case + "-" + (BBDD_NAME!"")?lower_case + "-" + (ENV!"DEV")?lower_case)?json_string}",
        "host": "${SOURCE_HOST!""?json_string}",
        "port": "${SOURCE_PORT!""?json_string}",
        "serviceName": "${SOURCE_SERVICE_NAME!""?json_string}",
        "schema": "${SOURCE_SCHEMA!""?json_string}",
        "tlsRequired": true,
        "credentials": {
          "provider": "${SECRETS_PROVIDER!"vault"?json_string}",
          "secretReference": "${SECRET_REFERENCE!("cdc-" + (BBDD_ENGINE!"ORACLE")?lower_case + "-" + (BBDD_NAME!"")?lower_case + "-" + (ENV!"DEV")?lower_case)?json_string}",
          "vaultPath": "${VAULT_PATH!("kv/data/cdc/" + (ENV!"DEV")?lower_case + "/" + (BBDD_ENGINE!"ORACLE")?lower_case + "/" + (BBDD_NAME!"")?lower_case)?json_string}"
        }
      },

      "cdc": {
        "enabled": true,
        "connector": "${CDC_CONNECTOR!("debezium-" + (BBDD_ENGINE!"ORACLE")?lower_case)?json_string}",
        "captureMode": "${CDC_CAPTURE_MODE!""?json_string}",
        "snapshotMode": "${SNAPSHOT_MODE!"initial"?json_string}",
        "publicationName": "${PUBLICATION_NAME!""?json_string}",
        "slotName": "${SLOT_NAME!""?json_string}",
        "deliverySemantic": "${DELIVERY_SEMANTIC!"at-least-once"?json_string}",
        "idempotentProducerEnabled": ${(IDEMPOTENT_PRODUCER_ENABLED!true)?c},
        "deadLetterQueueEnabled": ${(DLQ_ENABLED!true)?c}
      }
    }
  },

  "targets": {
    "kafka": {
      "enabled": true,
      "cluster": "${KAFKA_CLUSTER!("kafka-" + (ENV!"DEV")?lower_case)?json_string}",
      "bootstrapAlias": "${KAFKA_BOOTSTRAP_ALIAS!""?json_string}",

      "topic": {
        "name": "${KAFKA_TOPIC!(KAFKA_TOPIC_PREFIX!("cdc." + (ENV!"DEV")?lower_case + "." + (BBDD_ENGINE!"ORACLE")?lower_case + "." + (BBDD_NAME!"")?lower_case) + ".events.v1")?json_string}",
        "deadLetterTopic": "${KAFKA_DLQ_TOPIC!("dlq." + KAFKA_TOPIC!(KAFKA_TOPIC_PREFIX!("cdc." + (ENV!"DEV")?lower_case + "." + (BBDD_ENGINE!"ORACLE")?lower_case + "." + (BBDD_NAME!"")?lower_case) + ".events.v1"))?json_string}",
        "partitions": ${(KAFKA_PARTITIONS!3)?c},
        "replicationFactor": ${(KAFKA_REPLICATION_FACTOR!3)?c},
        "minInSyncReplicas": ${(KAFKA_MIN_IN_SYNC_REPLICAS!2)?c},
        "retentionMs": ${(KAFKA_RETENTION_MS!604800000)?c}
      },

      "serialization": {
        "format": "${SERIALIZATION_FORMAT!"avro"?json_string}",
        "schemaRegistryAlias": "${SCHEMA_REGISTRY_ALIAS!""?json_string}",
        "schemaCompatibility": "${SCHEMA_COMPATIBILITY!"BACKWARD"?json_string}"
      },

      "security": {
        "tlsRequired": true,
        "authentication": "external-secret-reference",
        "authorization": "topic-level-acl"
      }
    }
  },

  "runtime": {
    "platform": "kubernetes",
    "namespace": "${K8S_NAMESPACE!("cdc-" + (ENV!"DEV")?lower_case)?json_string}",
    "replicas": ${(REPLICAS!1)?c},

    "resources": {
      "requests": {
        "cpu": "${CPU_REQUEST!"250m"?json_string}",
        "memory": "${MEMORY_REQUEST!"512Mi"?json_string}"
      },
      "limits": {
        "cpu": "${CPU_LIMIT!"1"?json_string}",
        "memory": "${MEMORY_LIMIT!"1Gi"?json_string}"
      }
    },

    "security": {
      "runAsNonRoot": true,
      "readOnlyRootFilesystem": true,
      "allowPrivilegeEscalation": false,
      "networkPolicyRequired": true
    }
  },

  "observability": {
    "logging": {
      "format": "json",
      "level": "${LOG_LEVEL!"INFO"?json_string}",
      "redactSensitiveFields": true
    },

    "metrics": {
      "enabled": ${(METRICS_ENABLED!true)?c},
      "format": "prometheus",
      "endpoint": "/metrics"
    },

    "tracing": {
      "enabled": ${(TRACING_ENABLED!true)?c},
      "provider": "opentelemetry"
    }
  },

  "security": {
    "dataClassification": "${DATA_CLASSIFICATION!"internal"?json_string}",
    "containsPii": ${(CONTAINS_PII!false)?c},
    "containsSensitiveData": ${(CONTAINS_SENSITIVE_DATA!false)?c},
    "gdprApplicable": ${(GDPR_APPLICABLE!false)?c},

    "encryption": {
      "inTransitRequired": true,
      "minimumTlsVersion": "TLSv1.2",
      "atRestRequired": true
    },

    "secretManagement": {
      "provider": "${SECRETS_PROVIDER!"vault"?json_string}",
      "plainTextSecretsAllowed": false,
      "rotationRequired": true
    }
  },

  "quality": {
    "configurationValidationRequired": true,
    "schemaValidationRequired": true,
    "securityScanRequired": true,
    "secretScanRequired": true,
    "contractTestRequired": true,
    "liquibaseValidationRequired": true
  },

  "paths": {
    "applicationInput": "config-CDC/application/cdc_input_json_content.json",
    "databaseConnection": "config-CDC/db-connections/db-connections-${(BBDD_ENGINE!"ORACLE")?lower_case?json_string}.yml",
    "kafkaConnection": "config-CDC/target-connections/kafka.yml",
    "databaseChangelogMaster": "sources/database-template/master.xml",
    "securityMetadata": "security-metadata.toml"
  }
}

