"""
ArchGen AI - Motor Lógico de Generación y Validación de Arquitecturas de Software
================================================================================
Desarrollado para ingeniería DevOps, diseño de sistemas y arquitectura de software.
Genera diagramas Mermaid.js, desglose de componentes por capas, especificaciones
Docker Compose listas para producción y auditorías de calidad arquitectónica (ADR).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


# ==============================================================================
# ENUMERACIONES Y MODELOS DE DOMINIO
# ==============================================================================

class ArchitecturePattern(str, Enum):
    """Patrones arquitectónicos principales soportados por el motor."""
    MICROSERVICES = "Microservicios Distribuidos"
    EVENT_DRIVEN = "Arquitectura Orientada a Eventos (EDA)"
    MODULAR_MONOLITH = "Monolito Modular de Alto Rendimiento"
    HEXAGONAL = "Arquitectura Hexagonal (Puertos y Adaptadores)"
    CQRS_EVENT_SOURCING = "CQRS y Event Sourcing"
    SERVERLESS = "Arquitectura Serverless / FaaS"
    DATA_PIPELINE = "Pipeline de Ingesta y Streaming de Datos"
    N_TIER = "Arquitectura en Capas (N-Tier Empresarial)"


class Layer(str, Enum):
    """Capas lógicas y físicas de la arquitectura."""
    CLIENT = "Capa de Presentación / Clientes"
    GATEWAY = "Edge & API Gateway"
    APPLICATION = "Servicios de Aplicación & Orquestación"
    DOMAIN = "Servicios de Negocio / Dominio"
    MESSAGING = "Bus de Mensajería & Eventos Asíncronos"
    PERSISTENCE = "Capa de Persistencia & Almacenamiento"
    CACHE = "Capa de Aceleración & Caching en Memoria"
    OBSERVABILITY = "Observabilidad, Métricas & Monitoreo"
    SECURITY = "Identidad, Autenticación & Seguridad"


class ComponentType(str, Enum):
    """Tipos de componentes del sistema."""
    UI = "Frontend / Cliente"
    GATEWAY = "API Gateway / Ingress"
    SERVICE = "Microservicio / API"
    WORKER = "Worker Asíncrono / Consumer"
    DATABASE = "Base de Datos Relacional / NoSQL"
    CACHE = "Cache en Memoria"
    QUEUE = "Broker de Mensajes / Streaming"
    MONITORING = "Herramienta de Observabilidad"
    AUTH = "Servicio de Autenticación / IAM"
    STORAGE = "Almacenamiento de Objetos / S3"


class Pillar(str, Enum):
    """Pilares del marco Well-Architected."""
    SECURITY = "Seguridad y Control de Acceso"
    SCALABILITY = "Escalabilidad y Rendimiento"
    RELIABILITY = "Resiliencia y Tolerancia a Fallos"
    OBSERVABILITY = "Observabilidad y Monitoreo"
    MAINTAINABILITY = "Mantenibilidad y Modularidad"


class Severity(str, Enum):
    """Nivel de severidad para hallazgos y validaciones."""
    INFO = "INFO"
    WARNING = "ADVERTENCIA"
    CRITICAL = "CRÍTICO"


@dataclass
class ComponentSpec:
    """Especificación técnica de un componente del sistema."""
    id: str
    name: str
    layer: Layer
    component_type: ComponentType
    technology: str
    description: str
    port: Optional[str] = None
    docker_image: Optional[str] = None
    env_vars: Dict[str, str] = field(default_factory=dict)
    volumes: List[str] = field(default_factory=list)
    healthcheck: Optional[str] = None
    depends_on: List[str] = field(default_factory=list)


@dataclass
class RelationshipSpec:
    """Relación o flujo de comunicación entre dos componentes."""
    source_id: str
    target_id: str
    protocol: str
    label: str
    is_async: bool = False


@dataclass
class ValidationFinding:
    """Hallazgo o recomendación de la auditoría de arquitectura."""
    pillar: Pillar
    severity: Severity
    title: str
    description: str
    recommendation: str


@dataclass
class TradeOff:
    """Compromiso arquitectónico evaluado."""
    concept: str
    advantage: str
    drawback: str
    mitigation: str


@dataclass
class GenerationResult:
    """Resultado completo de la generación de arquitectura."""
    title: str
    pattern: ArchitecturePattern
    summary: str
    load_profile: str
    compliance: str
    components: List[ComponentSpec]
    relationships: List[RelationshipSpec]
    validations: List[ValidationFinding]
    pillar_scores: Dict[str, int]
    trade_offs: List[TradeOff]
    mermaid_diagram: str
    docker_compose_yaml: str
    markdown_report: str


# ==============================================================================
# MOTOR HEURÍSTICO Y GENERADOR DE ARQUITECTURAS
# ==============================================================================

class ArchitectureGenerator:
    """
    Motor inteligente de análisis de requerimientos, diseño de topologías,
    generación de diagramas Mermaid.js, docker-compose y auditorías de calidad.
    """

    def __init__(self) -> None:
        self._init_knowledge_base()

    def _init_knowledge_base(self) -> None:
        """Inicializa diccionarios de patrones, tecnologías y heurísticas."""
        self.domain_keywords = {
            "ecommerce": [
                "ecommerce", "tienda", "carrito", "catalogo", "pedidos",
                "compras", "checkout", "orden", "ordenes", "ventas", "productos"
            ],
            "fintech": [
                "fintech", "banco", "bancario", "pagos", "transferencias",
                "saldo", "billetera", "tarjeta", "credito", "debito", "transaccion", "ledger"
            ],
            "iot": [
                "iot", "sensores", "telemetria", "dispositivos", "mqtt",
                "streaming", "tiempo real", "gps", "mediciones", "sensores"
            ],
            "health": [
                "salud", "medico", "paciente", "citas", "historia clinica",
                "hospital", "doctor", "farmacia", "telemedicina", "hipaa"
            ],
            "social": [
                "social", "chat", "mensajes", "publicaciones", "seguidores",
                "feed", "red social", "notificaciones", "comentarios", "amigos"
            ],
            "saas": [
                "saas", "multi-tenant", "multitenant", "empresarial", "b2b",
                "suscripciones", "organizaciones", "inquilinos", "tenant"
            ],
            "logistics": [
                "logistica", "envios", "rutas", "repartidores", "almacen",
                "tracking", "rastreo", "vehiculos", "flota", "paquetes"
            ]
        }

    def analyze_and_generate(
        self,
        requirements_text: str,
        preferred_pattern: Optional[str] = None,
        load_profile: str = "Media (1k - 10k RPM)",
        compliance: str = "Estándar Empresarial",
        target_infra: str = "Docker Local / Compose"
    ) -> GenerationResult:
        """
        Punto de entrada principal. Analiza requerimientos en lenguaje natural
        y sintetiza una arquitectura completa y robusta.
        """
        cleaned_text = requirements_text.strip().lower() if requirements_text else ""

        # 1. Detección de Dominio y Patrón Arquitectónico
        detected_domain = self._detect_domain(cleaned_text)
        pattern = self._resolve_pattern(cleaned_text, preferred_pattern, detected_domain)

        # 2. Síntesis y Selección de Componentes
        components, relationships = self._synthesize_topology(
            text=cleaned_text,
            domain=detected_domain,
            pattern=pattern,
            load_profile=load_profile,
            compliance=compliance
        )

        # 3. Auditoría de Calidad Well-Architected y Puntuación
        validations, pillar_scores = self._audit_architecture(
            components=components,
            relationships=relationships,
            pattern=pattern,
            load_profile=load_profile,
            compliance=compliance
        )

        # 4. Matriz de Trade-offs
        trade_offs = self._evaluate_trade_offs(pattern, load_profile)

        # 5. Generación de Artefactos de Código y Diagramas
        mermaid_code = self._generate_mermaid(
            pattern=pattern,
            components=components,
            relationships=relationships
        )

        docker_compose_code = self._generate_docker_compose(
            components=components,
            title=f"ArchGen - {pattern.value}"
        )

        # 6. Generación del Reporte Técnico de Arquitectura (ADR)
        title = self._generate_title(detected_domain, pattern)
        summary = self._generate_summary(title, pattern, components, load_profile)

        markdown_report = self._generate_markdown_report(
            title=title,
            pattern=pattern,
            summary=summary,
            load_profile=load_profile,
            compliance=compliance,
            target_infra=target_infra,
            components=components,
            relationships=relationships,
            validations=validations,
            pillar_scores=pillar_scores,
            trade_offs=trade_offs,
            mermaid_diagram=mermaid_code,
            docker_compose=docker_compose_code
        )

        return GenerationResult(
            title=title,
            pattern=pattern,
            summary=summary,
            load_profile=load_profile,
            compliance=compliance,
            components=components,
            relationships=relationships,
            validations=validations,
            pillar_scores=pillar_scores,
            trade_offs=trade_offs,
            mermaid_diagram=mermaid_code,
            docker_compose_yaml=docker_compose_code,
            markdown_report=markdown_report
        )

    # --------------------------------------------------------------------------
    # DETECCIÓN DE DOMINIO Y RESOLUCIÓN DE PATRONES
    # --------------------------------------------------------------------------

    def _detect_domain(self, text: str) -> str:
        """Determina el área de dominio a partir del texto de entrada."""
        if not text:
            return "general"

        scores: Dict[str, int] = {domain: 0 for domain in self.domain_keywords}
        for domain, keywords in self.domain_keywords.items():
            for kw in keywords:
                if re.search(rf"\b{re.escape(kw)}\b", text):
                    scores[domain] += 1

        best_domain = max(scores, key=lambda k: scores[k])
        return best_domain if scores[best_domain] > 0 else "general"

    def _resolve_pattern(
        self,
        text: str,
        preferred_pattern: Optional[str],
        domain: str
    ) -> ArchitecturePattern:
        """Resuelve el patrón arquitectónico más adecuado considerando preferencias."""
        # Si el usuario solicitó explícitamente un patrón específico
        if preferred_pattern and preferred_pattern != "Auto-Detectar":
            for p in ArchitecturePattern:
                if preferred_pattern.lower() in p.value.lower() or p.name.lower() in preferred_pattern.lower():
                    return p

        # Heurísticas basadas en texto
        if any(w in text for w in ["event-driven", "eventos", "kafka", "asincrono", "pub/sub", "streaming"]):
            return ArchitecturePattern.EVENT_DRIVEN
        if any(w in text for w in ["cqrs", "event sourcing", "read model", "write model"]):
            return ArchitecturePattern.CQRS_EVENT_SOURCING
        if any(w in text for w in ["hexagonal", "puertos y adaptadores", "clean architecture", "dominio puro"]):
            return ArchitecturePattern.HEXAGONAL
        if any(w in text for w in ["monolito", "modular", "fastapi modular", "django", "laravel"]):
            return ArchitecturePattern.MODULAR_MONOLITH
        if any(w in text for w in ["serverless", "lambda", "cloud functions", "faas"]):
            return ArchitecturePattern.SERVERLESS
        if any(w in text for w in ["pipeline", "etl", "data lake", "spark", "lakehouse"]):
            return ArchitecturePattern.DATA_PIPELINE

        # Reglas por dominio
        if domain in ["ecommerce", "logistics", "social", "saas"]:
            return ArchitecturePattern.MICROSERVICES
        if domain in ["fintech"]:
            return ArchitecturePattern.HEXAGONAL
        if domain in ["iot"]:
            return ArchitecturePattern.EVENT_DRIVEN

        return ArchitecturePattern.MICROSERVICES

    # --------------------------------------------------------------------------
    # SÍNTESIS DE TOPOLOGÍA Y COMPONENTES
    # --------------------------------------------------------------------------

    def _synthesize_topology(
        self,
        text: str,
        domain: str,
        pattern: ArchitecturePattern,
        load_profile: str,
        compliance: str
    ) -> Tuple[List[ComponentSpec], List[RelationshipSpec]]:
        """Construye los nodos y las conexiones de la arquitectura."""
        components: List[ComponentSpec] = []
        relationships: List[RelationshipSpec] = []

        is_high_load = any(term in load_profile.lower() for term in ["alta", "crítica", "extrema", "10k", "100k"])
        is_strict_compliance = any(term in compliance.lower() for term in ["financiero", "pci", "hipaa", "bancario"])

        # 1. Capa de Presentación
        components.append(
            ComponentSpec(
                id="web_portal",
                name="Portal Web SPA",
                layer=Layer.CLIENT,
                component_type=ComponentType.UI,
                technology="React 18 / Next.js / TypeScript",
                description="Frontend responsivo con Server-Side Rendering y gestión de estado.",
                port="3000:3000",
                docker_image="node:20-alpine"
            )
        )
        if "movil" in text or "app" in text or domain in ["ecommerce", "fintech", "logistics", "health"]:
            components.append(
                ComponentSpec(
                    id="mobile_app",
                    name="App Móvil Nativa / Híbrida",
                    layer=Layer.CLIENT,
                    component_type=ComponentType.UI,
                    technology="Flutter / React Native",
                    description="Cliente móvil para iOS y Android con sincronización sin conexión."
                )
            )

        # 2. Capa Edge & API Gateway
        components.append(
            ComponentSpec(
                id="api_gateway",
                name="Edge API Gateway & Reverse Proxy",
                layer=Layer.GATEWAY,
                component_type=ComponentType.GATEWAY,
                technology="Traefik Proxy v3 / Kong Gateway",
                description="Enrutamiento inteligente, terminación TLS, Rate Limiting y validación de tokens.",
                port="80:80, 443:443, 8080:8080",
                docker_image="traefik:v3.0",
                healthcheck="traefik healthcheck --ping"
            )
        )

        # Conectar clientes con el Gateway
        relationships.append(RelationshipSpec("web_portal", "api_gateway", "HTTPS / WSS", "Solicitudes HTTPS y WebSockets"))
        if any(c.id == "mobile_app" for c in components):
            relationships.append(RelationshipSpec("mobile_app", "api_gateway", "HTTPS / REST", "Peticiones móviles seguras"))

        # 3. Capa de Seguridad e Identidad
        components.append(
            ComponentSpec(
                id="auth_service",
                name="Servicio de Autenticación & IAM",
                layer=Layer.SECURITY,
                component_type=ComponentType.AUTH,
                technology="OAuth2 / OIDC / Keycloak / JWT",
                description="Gestión centralizada de identidades, emisión de JWT y control RBAC.",
                port="8081:8080",
                docker_image="quay.io/keycloak/keycloak:24.0",
                env_vars={"KEYCLOAK_ADMIN": "admin", "KEYCLOAK_ADMIN_PASSWORD": "admin_secure_password"},
                depends_on=["postgres_main"]
            )
        )
        relationships.append(RelationshipSpec("api_gateway", "auth_service", "gRPC / REST", "Validación y Firma de Tokens"))

        # 4. Servicios de Dominio según Dominio y Patrón
        domain_services = self._get_domain_services(domain, pattern, text)
        for s in domain_services:
            components.append(s)
            relationships.append(RelationshipSpec("api_gateway", s.id, "HTTP/REST o gRPC", f"Enruta hacia {s.name}"))

        # 5. Capa de Mensajería Asíncrona (Si aplica por patrón o alta concurrencia)
        needs_broker = (
            pattern in [ArchitecturePattern.EVENT_DRIVEN, ArchitecturePattern.CQRS_EVENT_SOURCING, ArchitecturePattern.MICROSERVICES]
            or is_high_load or domain in ["ecommerce", "fintech", "iot", "logistics"]
        )

        broker_id = "message_broker"
        if needs_broker:
            is_streaming = pattern in [ArchitecturePattern.EVENT_DRIVEN, ArchitecturePattern.DATA_PIPELINE] or domain == "iot" or is_high_load
            broker_tech = "Apache Kafka 3.7 (KRaft)" if is_streaming else "RabbitMQ 3.13 (AMQP)"
            broker_image = "confluentinc/cp-kafka:7.5.0" if is_streaming else "rabbitmq:3.13-management-alpine"
            broker_port = "9092:9092" if is_streaming else "5672:5672, 15672:15672"

            components.append(
                ComponentSpec(
                    id=broker_id,
                    name="Bus de Eventos & Mensajería",
                    layer=Layer.MESSAGING,
                    component_type=ComponentType.QUEUE,
                    technology=broker_tech,
                    description="Desacoplamiento asíncrono, buffer de eventos y tolerancia a picos de tráfico.",
                    port=broker_port,
                    docker_image=broker_image,
                    healthcheck="rabbitmq-diagnostics -q ping" if not is_streaming else None
                )
            )

            # Worker Asíncrono de Procesamiento
            components.append(
                ComponentSpec(
                    id="async_worker",
                    name="Motor de Tareas y Notificaciones",
                    layer=Layer.APPLICATION,
                    component_type=ComponentType.WORKER,
                    technology="Python (Celery / FastAPI Worker) o Go Consumer",
                    description="Procesamiento en segundo plano de emails, webhooks y tareas diferidas.",
                    docker_image="python:3.11-slim",
                    depends_on=[broker_id]
                )
            )
            relationships.append(RelationshipSpec(broker_id, "async_worker", "AMQP / Kafka", "Consume eventos y tareas en segundo plano", is_async=True))

            # Conectar servicios al Broker
            for s in domain_services:
                relationships.append(RelationshipSpec(s.id, broker_id, "AMQP / Kafka", "Publica eventos de dominio", is_async=True))

        # 6. Capa de Caché
        cache_id = "cache_layer"
        components.append(
            ComponentSpec(
                id=cache_id,
                name="Caché Distribuida & Sesiones",
                layer=Layer.CACHE,
                component_type=ComponentType.CACHE,
                technology="Redis 7.2 Alpine",
                description="Caché de consultas frecuentes, rate limiting y sesiones volátiles.",
                port="6379:6379",
                docker_image="redis:7.2-alpine",
                healthcheck="redis-cli ping || exit 1",
                volumes=["redis_data:/data"]
            )
        )
        for s in domain_services:
            relationships.append(RelationshipSpec(s.id, cache_id, "RESP / TCP", "Caché L2 de lectura rápida y bloqueo"))

        # 7. Capa de Persistencia Primaria
        db_id = "postgres_main"
        db_tech = "PostgreSQL 16 High-Availability" if not is_strict_compliance else "PostgreSQL 16 con Cifrado en Reposo (TDE)"
        components.append(
            ComponentSpec(
                id=db_id,
                name="Base de Datos Relacional Principal",
                layer=Layer.PERSISTENCE,
                component_type=ComponentType.DATABASE,
                technology=db_tech,
                description="Persistencia ACID con esquema relacional normalizado y soporte JSONB.",
                port="5432:5432",
                docker_image="postgres:16-alpine",
                env_vars={
                    "POSTGRES_DB": "archgen_production",
                    "POSTGRES_USER": "archgen_admin",
                    "POSTGRES_PASSWORD": "archgen_strong_password_dev"
                },
                volumes=["postgres_data:/var/lib/postgresql/data"],
                healthcheck="pg_isready -U archgen_admin -d archgen_production"
            )
        )
        for s in domain_services:
            relationships.append(RelationshipSpec(s.id, db_id, "SQL / Pool Conexiones", "Transacciones ACID y consultas"))

        # Si el dominio es analítico, IoT o maneja documentos no estructurados, agregar almacén especializado
        if domain in ["iot", "social", "ecommerce"] or "nosql" in text or "mongodb" in text:
            components.append(
                ComponentSpec(
                    id="nosql_store",
                    name="Almacén de Documentos y Auditoría",
                    layer=Layer.PERSISTENCE,
                    component_type=ComponentType.DATABASE,
                    technology="MongoDB 7.0 / TimescaleDB",
                    description="Almacenamiento de catálogo dinámico, logs semi-estructurados y telemetría.",
                    port="27017:27017",
                    docker_image="mongo:7.0",
                    volumes=["mongo_data:/data/db"]
                )
            )

        # 8. Observabilidad & DevOps
        components.append(
            ComponentSpec(
                id="prometheus",
                name="Recolección de Métricas (Prometheus)",
                layer=Layer.OBSERVABILITY,
                component_type=ComponentType.MONITORING,
                technology="Prometheus v2.51",
                description="Scraping de métricas de rendimiento, latencia RED y uso de hardware.",
                port="9090:9090",
                docker_image="prom/prometheus:v2.51.0",
                volumes=["prometheus_data:/prometheus"]
            )
        )
        components.append(
            ComponentSpec(
                id="grafana",
                name="Dashboards y Alertas (Grafana)",
                layer=Layer.OBSERVABILITY,
                component_type=ComponentType.MONITORING,
                technology="Grafana Labs v10.4",
                description="Visualización centralizada de SLOs, SLIs y tableros operativos de infraestructura.",
                port="3001:3000",
                docker_image="grafana/grafana:10.4.0",
                volumes=["grafana_data:/var/lib/grafana"],
                depends_on=["prometheus"]
            )
        )
        relationships.append(RelationshipSpec("grafana", "prometheus", "PromQL / HTTP", "Consulta de series de tiempo para dashboards"))

        return components, relationships

    def _get_domain_services(
        self,
        domain: str,
        pattern: ArchitecturePattern,
        text: str
    ) -> List[ComponentSpec]:
        """Genera los servicios de negocio específicos del dominio."""
        services: List[ComponentSpec] = []

        if pattern == ArchitecturePattern.MODULAR_MONOLITH:
            services.append(
                ComponentSpec(
                    id="modular_core",
                    name="Núcleo Monolítico Modular",
                    layer=Layer.APPLICATION,
                    component_type=ComponentType.SERVICE,
                    technology="FastAPI (Python 3.12) / Arquitectura Limpia",
                    description="Monolito estructurado en módulos aislados con boundaries bien definidos.",
                    port="8000:8000",
                    docker_image="python:3.12-slim",
                    depends_on=["postgres_main", "cache_layer"]
                )
            )
            return services

        if domain == "ecommerce":
            services.extend([
                ComponentSpec(
                    id="catalog_service",
                    name="Microservicio de Catálogo & Stock",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="FastAPI / Python o Go Fiber",
                    description="Gestión de inventario, atributos de productos y disponibilidad en tiempo real.",
                    port="8001:8000",
                    docker_image="python:3.11-slim",
                    depends_on=["postgres_main", "cache_layer"]
                ),
                ComponentSpec(
                    id="order_service",
                    name="Microservicio de Gestión de Órdenes",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="Java Spring Boot 3.2 o Node.js / NestJS",
                    description="Orquestación del ciclo de vida de pedidos mediante patrón Saga o eventos.",
                    port="8002:8080",
                    docker_image="eclipse-temurin:21-jre-alpine",
                    depends_on=["postgres_main"]
                ),
                ComponentSpec(
                    id="payment_service",
                    name="Microservicio de Pagos & Facturación",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="Go (Golang) / Microframework",
                    description="Integración segura con pasarelas de pago, tokenización y cumplimiento PCI.",
                    port="8003:8080",
                    docker_image="golang:1.22-alpine",
                    depends_on=["postgres_main"]
                )
            ])
        elif domain == "fintech":
            services.extend([
                ComponentSpec(
                    id="core_ledger_service",
                    name="Servicio de Transacciones y Libro Mayor (Ledger)",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="Java 21 / Quarkus o Rust",
                    description="Contabilidad de doble partida inmutable y procesamiento ACID ultra-estricto.",
                    port="8001:8080",
                    docker_image="eclipse-temurin:21-jre-alpine",
                    depends_on=["postgres_main"]
                ),
                ComponentSpec(
                    id="fraud_detection_service",
                    name="Motor de Detección de Fraude en Tiempo Real",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="Python (FastAPI + ONNX Runtime / ML)",
                    description="Evaluación de patrones de riesgo en menos de 50ms antes de autorizar transferencias.",
                    port="8002:8000",
                    docker_image="python:3.11-slim",
                    depends_on=["cache_layer"]
                ),
                ComponentSpec(
                    id="account_service",
                    name="Servicio de Cuentas y Tarjetahabientes",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="Go / Clean Architecture",
                    description="Gestión de balances, límites operativos y estados de cuentas.",
                    port="8003:8080",
                    docker_image="golang:1.22-alpine",
                    depends_on=["postgres_main"]
                )
            ])
        elif domain == "iot":
            services.extend([
                ComponentSpec(
                    id="ingestion_gateway",
                    name="Gateway de Ingesta Masiva IoT",
                    layer=Layer.GATEWAY,
                    component_type=ComponentType.GATEWAY,
                    technology="Go / EMQX Broker / MQTT",
                    description="Recepción de telemetría de alta frecuencia de miles de dispositivos.",
                    port="1883:1883",
                    docker_image="emqx/emqx:5.5.0"
                ),
                ComponentSpec(
                    id="telemetry_processor",
                    name="Procesador de Streaming y Reglas",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.WORKER,
                    technology="Python / Rust / Flink",
                    description="Cálculo de medias móviles, detección de anomalías y disparo de alarmas.",
                    docker_image="python:3.11-slim"
                ),
                ComponentSpec(
                    id="device_management_service",
                    name="Gestor de Dispositivos & Firmwares",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="Node.js / Express / TypeScript",
                    description="Provisionamiento, aprovisionamiento seguro y actualización OTA.",
                    port="8001:3000",
                    docker_image="node:20-alpine",
                    depends_on=["postgres_main"]
                )
            ])
        elif domain == "health":
            services.extend([
                ComponentSpec(
                    id="ehr_records_service",
                    name="Servicio de Historia Clínica Digital (EHR)",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="Java Spring Boot con estándar HL7 / FHIR",
                    description="Almacenamiento seguro y auditado de registros médicos con cifrado de grado militar.",
                    port="8001:8080",
                    docker_image="eclipse-temurin:21-jre-alpine",
                    depends_on=["postgres_main"]
                ),
                ComponentSpec(
                    id="appointments_service",
                    name="Gestor de Citas Médicas y Agenda",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="FastAPI (Python 3.11)",
                    description="Coordinación de calendarios médicos, disponibilidad de quirófanos y recordatorios.",
                    port="8002:8000",
                    docker_image="python:3.11-slim",
                    depends_on=["postgres_main", "cache_layer"]
                )
            ])
        elif domain == "saas":
            services.extend([
                ComponentSpec(
                    id="tenant_management_service",
                    name="Servicio de Gestión Multi-Tenant & Facturación",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="NestJS / TypeScript",
                    description="Aislamiento lógico por cliente, gestión de suscripciones y control de cuotas.",
                    port="8001:3000",
                    docker_image="node:20-alpine",
                    depends_on=["postgres_main"]
                ),
                ComponentSpec(
                    id="core_business_service",
                    name="Servicio Central de Negocio (Core SaaS)",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="Go Fiber / Hexagonal",
                    description="Lógica operacional específica del producto B2B con alta concurrencia.",
                    port="8002:8080",
                    docker_image="golang:1.22-alpine",
                    depends_on=["postgres_main", "cache_layer"]
                )
            ])
        else:
            # Fallback general balanceado
            services.extend([
                ComponentSpec(
                    id="core_api_service",
                    name="Servicio Central de Negocio (Core API)",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="FastAPI (Python 3.12) / Clean Architecture",
                    description="API RESTful de alto rendimiento que encapsula la lógica principal del sistema.",
                    port="8000:8000",
                    docker_image="python:3.12-slim",
                    depends_on=["postgres_main", "cache_layer"]
                ),
                ComponentSpec(
                    id="operations_service",
                    name="Servicio de Operaciones y Reportes",
                    layer=Layer.DOMAIN,
                    component_type=ComponentType.SERVICE,
                    technology="Node.js / Express / TypeScript",
                    description="Generación de informes, exportación de datos y procesos complementarios.",
                    port="8002:3000",
                    docker_image="node:20-alpine",
                    depends_on=["postgres_main"]
                )
            ])

        return services

    # --------------------------------------------------------------------------
    # AUDITORÍA DE CALIDAD Y WELL-ARCHITECTED
    # --------------------------------------------------------------------------

    def _audit_architecture(
        self,
        components: List[ComponentSpec],
        relationships: List[RelationshipSpec],
        pattern: ArchitecturePattern,
        load_profile: str,
        compliance: str
    ) -> Tuple[List[ValidationFinding], Dict[str, int]]:
        """Evalúa la arquitectura contra las mejores prácticas de ingeniería."""
        validations: List[ValidationFinding] = []
        scores: Dict[str, int] = {
            Pillar.SECURITY.value: 85,
            Pillar.SCALABILITY.value: 85,
            Pillar.RELIABILITY.value: 80,
            Pillar.OBSERVABILITY.value: 90,
            Pillar.MAINTAINABILITY.value: 85
        }

        # 1. Validación de Gateway y Seguridad perimetral
        has_gateway = any(c.component_type == ComponentType.GATEWAY for c in components)
        has_auth = any(c.component_type == ComponentType.AUTH for c in components)

        if has_gateway and has_auth:
            validations.append(
                ValidationFinding(
                    pillar=Pillar.SECURITY,
                    severity=Severity.INFO,
                    title="Control Perimetral Robusto (Edge Security)",
                    description="Se detectó un API Gateway junto con un Servicio de Identidad dedicado.",
                    recommendation="Implementar mTLS (Mutual TLS) entre el Gateway y los microservicios internos."
                )
            )
            scores[Pillar.SECURITY.value] = min(100, scores[Pillar.SECURITY.value] + 10)
        else:
            validations.append(
                ValidationFinding(
                    pillar=Pillar.SECURITY,
                    severity=Severity.CRITICAL,
                    title="Ausencia de Gateway Centralizado",
                    description="Los servicios podrían quedar expuestos directamente sin políticas de rate limiting.",
                    recommendation="Ubicar un API Gateway en la zona desmilitarizada (DMZ)."
                )
            )
            scores[Pillar.SECURITY.value] -= 25

        # 2. Validación de Caching y Escalabilidad
        has_cache = any(c.component_type == ComponentType.CACHE for c in components)
        is_high_load = any(w in load_profile.lower() for w in ["alta", "crítica", "extrema", "10k", "100k"])

        if has_cache:
            validations.append(
                ValidationFinding(
                    pillar=Pillar.SCALABILITY,
                    severity=Severity.INFO,
                    title="Capa de Caché Distribuida Configurada",
                    description="El uso de Redis mitiga la saturación de conexiones hacia la base de datos relacional.",
                    recommendation="Configurar estrategias de invalidación Cache-Aside y políticas de expiración TTL."
                )
            )
            scores[Pillar.SCALABILITY.value] = min(100, scores[Pillar.SCALABILITY.value] + 10)
        elif is_high_load:
            validations.append(
                ValidationFinding(
                    pillar=Pillar.SCALABILITY,
                    severity=Severity.CRITICAL,
                    title="Riesgo de Cuello de Botella en Persistencia",
                    description="Para el perfil de carga solicitado, la ausencia de caché provocará contención de I/O.",
                    recommendation="Integrar Redis o Memcached como capa L2 antes de la base de datos."
                )
            )
            scores[Pillar.SCALABILITY.value] -= 30

        # 3. Validación de Mensajería Asíncrona y Resiliencia
        has_queue = any(c.component_type == ComponentType.QUEUE for c in components)
        if has_queue:
            validations.append(
                ValidationFinding(
                    pillar=Pillar.RELIABILITY,
                    severity=Severity.INFO,
                    title="Desacoplamiento Temporal Mediante Colas/Eventos",
                    description="Las operaciones no críticas se aíslan a través de mensajería asíncrona.",
                    recommendation="Configurar Dead Letter Queues (DLQ) para capturar y reintentar mensajes fallidos."
                )
            )
            scores[Pillar.RELIABILITY.value] = min(100, scores[Pillar.RELIABILITY.value] + 10)
        else:
            validations.append(
                ValidationFinding(
                    pillar=Pillar.RELIABILITY,
                    severity=Severity.WARNING,
                    title="Acoplamiento Síncrono de Servicios",
                    description="La comunicación pura vía HTTP/REST puede provocar fallos en cascada.",
                    recommendation="Implementar un patrón Circuit Breaker y colas para tareas asíncronas."
                )
            )
            scores[Pillar.RELIABILITY.value] -= 15

        # 4. Validación de Observabilidad
        has_monitoring = any(c.component_type == ComponentType.MONITORING for c in components)
        if has_monitoring:
            validations.append(
                ValidationFinding(
                    pillar=Pillar.OBSERVABILITY,
                    severity=Severity.INFO,
                    title="Stack de Telemetría y Métricas Presente",
                    description="Se incluyen componentes dedicados (Prometheus / Grafana) para monitorizar el ciclo de vida.",
                    recommendation="Agregar OpenTelemetry collector para trazabilidad distribuida de requests (Trace IDs)."
                )
            )
        else:
            validations.append(
                ValidationFinding(
                    pillar=Pillar.OBSERVABILITY,
                    severity=Severity.WARNING,
                    title="Falta de Trazabilidad Centralizada",
                    description="Sin observabilidad activa, el diagnóstico de incidentes en producción será complejo.",
                    recommendation="Exponer endpoints `/metrics` y recolectar logs de manera centralizada."
                )
            )
            scores[Pillar.OBSERVABILITY.value] -= 20

        # 5. Cumplimiento Normativo (PCI / HIPAA / Financiero)
        if "financiero" in compliance.lower() or "pci" in compliance.lower() or "hipaa" in compliance.lower():
            validations.append(
                ValidationFinding(
                    pillar=Pillar.SECURITY,
                    severity=Severity.WARNING,
                    title="Requisito de Cifrado Estricto y Auditoría Inmutable",
                    description=f"El perfil '{compliance}' exige cifrado en tránsito (TLS 1.3), cifrado en reposo (AES-256) y pistas de auditoría.",
                    recommendation="Aislar bases de datos en subredes privadas sin IP pública y habilitar auditoría pgaudit en PostgreSQL."
                )
            )

        return validations, scores

    # --------------------------------------------------------------------------
    # EVALUACIÓN DE TRADE-OFFS
    # --------------------------------------------------------------------------

    def _evaluate_trade_offs(
        self,
        pattern: ArchitecturePattern,
        load_profile: str
    ) -> List[TradeOff]:
        """Genera una matriz técnica de compromisos arquitectónicos."""
        trade_offs = []

        if pattern in [ArchitecturePattern.MICROSERVICES, ArchitecturePattern.EVENT_DRIVEN]:
            trade_offs.append(
                TradeOff(
                    concept="Consistencia Eventual vs. Consistencia Fuerte",
                    advantage="Altísima disponibilidad y escalabilidad horizontal independiente por servicio.",
                    drawback="Complejidad en mantener la coherencia de datos entre múltiples bases de datos.",
                    mitigation="Implementar el patrón Saga (Coreografiado u Orquestado) y reconciliación de eventos."
                )
            )
            trade_offs.append(
                TradeOff(
                    concept="Granularidad de Servicios vs. Sobrecarga Operativa DevOps",
                    advantage="Despliegues autónomos, ciclos CI/CD desacoplados y uso eficiente de CPU/RAM.",
                    drawback="Mayor complejidad de redes, monitoreo distribuido y necesidad de orquestadores (K8s).",
                    mitigation="Automatizar con Helm charts, infraestructura como código (Terraform) y service mesh."
                )
            )
        elif pattern == ArchitecturePattern.MODULAR_MONOLITH:
            trade_offs.append(
                TradeOff(
                    concept="Simplicidad Operativa vs. Escalado Holístico",
                    advantage="Despliegue unificado, transacciones ACID nativas y menor latencia de red interna.",
                    drawback="El escalado horizontal duplica todo el monolito en lugar de sólo el cuello de botella.",
                    mitigation="Mantener módulos estrictamente desacoplados con interfaces públicas para futura extracción."
                )
            )
        elif pattern == ArchitecturePattern.HEXAGONAL:
            trade_offs.append(
                TradeOff(
                    concept="Abstracción de Puertos/Adaptadores vs. Curva de Desarrollo",
                    advantage="Negocio 100% independiente de frameworks, base de datos o librerías de terceros.",
                    drawback="Mayor cantidad de código boilerplate, interfaces y transformadores DTO.",
                    mitigation="Usar generadores de código y plantillas limpias de arquitectura para acelerar onboarding."
                )
            )

        trade_offs.append(
            TradeOff(
                concept="Caché Agresiva en Memoria vs. Riesgo de Datos Obsoletos (Stale Data)",
                advantage="Tiempos de respuesta menores a 5ms y protección contra picos de concurrencia.",
                drawback="Riesgo de servir lecturas obsoletas si falla la invalidación de caché.",
                mitigation="Definir TTLs cortos y publicar eventos de invalidación en el bus de mensajes tras mutaciones."
            )
        )

        return trade_offs

    # --------------------------------------------------------------------------
    # GENERADOR DE DIAGRAMA MERMAID.JS
    # --------------------------------------------------------------------------

    def _generate_mermaid(
        self,
        pattern: ArchitecturePattern,
        components: List[ComponentSpec],
        relationships: List[RelationshipSpec]
    ) -> str:
        """
        Produce sintaxis Mermaid.js estilizada, limpia y compatible con renderizadores
        modernos, organizada por subgrafos que representan las capas de software.
        """
        lines: List[str] = [
            "flowchart TB",
            "    %% Diagrama de Arquitectura Generado por ArchGen AI",
            "    %% Patrón: " + pattern.value,
            ""
        ]

        # Agrupar componentes por capa
        layers_map: Dict[Layer, List[ComponentSpec]] = {}
        for c in components:
            layers_map.setdefault(c.layer, []).append(c)

        # Definir subgrafos con etiquetas claras
        layer_labels = {
            Layer.CLIENT: 'subgraph CLIENTS [" 🌐 Capa de Presentación / Clientes "]',
            Layer.GATEWAY: 'subgraph GATEWAYS [" 🛡️ Edge, Gateway & Ingress "]',
            Layer.SECURITY: 'subgraph SEC [" 🔒 Seguridad & Autorización "]',
            Layer.APPLICATION: 'subgraph APPS [" ⚡ Servicios de Aplicación & Workers "]',
            Layer.DOMAIN: 'subgraph DOMAIN [" 🧩 Servicios de Dominio de Negocio "]',
            Layer.MESSAGING: 'subgraph QUEUES [" 📨 Bus de Eventos & Colas "]',
            Layer.CACHE: 'subgraph CACHING [" ⚡ Aceleración en Memoria "]',
            Layer.PERSISTENCE: 'subgraph STORAGE [" 💾 Persistencia de Datos "]',
            Layer.OBSERVABILITY: 'subgraph TELEMETRY [" 📊 Observabilidad & Monitoreo "]'
        }

        # Orden deseado de presentación
        ordered_layers = [
            Layer.CLIENT,
            Layer.GATEWAY,
            Layer.SECURITY,
            Layer.APPLICATION,
            Layer.DOMAIN,
            Layer.MESSAGING,
            Layer.CACHE,
            Layer.PERSISTENCE,
            Layer.OBSERVABILITY
        ]

        for lyr in ordered_layers:
            if lyr in layers_map:
                lines.append(f"    {layer_labels.get(lyr, f'subgraph {lyr.name}')}")
                for comp in layers_map[lyr]:
                    node_repr = self._format_mermaid_node(comp)
                    lines.append(f"        {node_repr}")
                lines.append("    end")
                lines.append("")

        # Relaciones y Flujos de Comunicación
        lines.append("    %% Conexiones e Interacciones")
        for r in relationships:
            sanitized_label = r.label.replace('"', '').replace("'", "")
            if r.is_async:
                # Línea discontinua para comunicación asíncrona
                lines.append(f'    {r.source_id} -.->|"{r.protocol}: {sanitized_label}"| {r.target_id}')
            else:
                # Flecha sólida para llamadas síncronas
                lines.append(f'    {r.source_id} -->|"{r.protocol}: {sanitized_label}"| {r.target_id}')

        # Estilos CSS profesionales de Mermaid
        lines.append("")
        lines.append("    %% Estilos de Alto Contraste para Ingeniería")
        lines.append("    classDef clientClass fill:#1E293B,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC;")
        lines.append("    classDef gatewayClass fill:#312E81,stroke:#818CF8,stroke-width:2px,color:#EEF2FF;")
        lines.append("    classDef serviceClass fill:#0F172A,stroke:#38BDF8,stroke-width:2px,color:#F0F9FF;")
        lines.append("    classDef dbClass fill:#064E3B,stroke:#34D399,stroke-width:2px,color:#ECFDF5;")
        lines.append("    classDef cacheClass fill:#701A75,stroke:#E879F9,stroke-width:2px,color:#FDF4FF;")
        lines.append("    classDef queueClass fill:#78350F,stroke:#FBBF24,stroke-width:2px,color:#FEF3C7;")
        lines.append("    classDef obsClass fill:#334155,stroke:#94A3B8,stroke-width:2px,color:#F8FAFC;")
        lines.append("    classDef secClass fill:#881337,stroke:#FB7185,stroke-width:2px,color:#FFF1F2;")

        # Aplicar clases a los nodos
        for c in components:
            if c.layer == Layer.CLIENT:
                lines.append(f"    class {c.id} clientClass;")
            elif c.layer == Layer.GATEWAY:
                lines.append(f"    class {c.id} gatewayClass;")
            elif c.layer in [Layer.DOMAIN, Layer.APPLICATION]:
                lines.append(f"    class {c.id} serviceClass;")
            elif c.layer == Layer.PERSISTENCE:
                lines.append(f"    class {c.id} dbClass;")
            elif c.layer == Layer.CACHE:
                lines.append(f"    class {c.id} cacheClass;")
            elif c.layer == Layer.MESSAGING:
                lines.append(f"    class {c.id} queueClass;")
            elif c.layer == Layer.OBSERVABILITY:
                lines.append(f"    class {c.id} obsClass;")
            elif c.layer == Layer.SECURITY:
                lines.append(f"    class {c.id} secClass;")

        return "\n".join(lines)

    def _format_mermaid_node(self, c: ComponentSpec) -> str:
        """Formatea un nodo Mermaid con su figura geométrica adecuada según el tipo."""
        clean_name = c.name.replace('"', "'")
        tech = f"({c.technology})"

        if c.component_type in [ComponentType.DATABASE, ComponentType.STORAGE]:
            # Cilindro para bases de datos
            return f'{c.id}[("<b>{clean_name}</b><br/><small>{tech}</small>")]'
        elif c.component_type == ComponentType.QUEUE:
            # Subrutina o bandera para colas
            return f'{c.id}>"<b>{clean_name}</b><br/><small>{tech}</small>"]'
        elif c.component_type == ComponentType.GATEWAY:
            # Hexágono para Gateways / Edge
            return f'{c.id}{{"<b>{clean_name}</b><br/><small>{tech}</small>"}}'
        elif c.component_type == ComponentType.CACHE:
            # Cilindro o estadio para caché
            return f'{c.id}([ "<b>{clean_name}</b><br/><small>{tech}</small>" ])'
        elif c.component_type == ComponentType.UI:
            # Rectángulo redondeado para interfaces
            return f'{c.id}["<b>{clean_name}</b><br/><small>{tech}</small>"]'
        else:
            # Rectángulo estándar para microservicios
            return f'{c.id}["<b>{clean_name}</b><br/><small>{tech}</small>"]'

    # --------------------------------------------------------------------------
    # GENERADOR DE DOCKER COMPOSE
    # --------------------------------------------------------------------------

    def _generate_docker_compose(
        self,
        components: List[ComponentSpec],
        title: str
    ) -> str:
        """
        Genera una especificación de docker-compose.yml completa, robusta y
        autocontenida, con redes aisladas, volúmenes con nombre y healthchecks.
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines: List[str] = [
            f"# ==============================================================================",
            f"# {title}",
            f"# Generado automáticamente por ArchGen AI - {now}",
            f"# Instrucciones de inicio: docker compose up -d",
            f"# ==============================================================================",
            "version: '3.8'",
            "",
            "services:"
        ]

        # Definir servicios de docker
        for c in components:
            if c.component_type == ComponentType.UI and "móvil" in c.name.lower():
                continue  # No se orquesta app nativa en docker compose local

            service_key = c.id.replace("-", "_")
            lines.append(f"  {service_key}:")
            lines.append(f"    container_name: archgen_{service_key}")

            image = c.docker_image or "alpine:latest"
            lines.append(f"    image: {image}")
            lines.append("    restart: unless-stopped")

            # Mapeo de puertos
            if c.port:
                ports = [p.strip() for p in c.port.split(",")]
                lines.append("    ports:")
                for p in ports:
                    lines.append(f'      - "{p}"')

            # Variables de entorno
            env_vars = dict(c.env_vars)
            if c.component_type == ComponentType.SERVICE:
                env_vars.setdefault("APP_ENV", "production")
                env_vars.setdefault("LOG_LEVEL", "info")
                env_vars.setdefault("DATABASE_URL", "postgresql://archgen_admin:archgen_strong_password_dev@postgres_main:5432/archgen_production")
                env_vars.setdefault("REDIS_URL", "redis://cache_layer:6379/0")

            if env_vars:
                lines.append("    environment:")
                for k, v in env_vars.items():
                    lines.append(f"      {k}: '{v}'")

            # Volúmenes
            if c.volumes:
                lines.append("    volumes:")
                for vol in c.volumes:
                    lines.append(f"      - {vol}")

            # Healthcheck
            if c.healthcheck:
                lines.append("    healthcheck:")
                lines.append(f'      test: ["CMD-SHELL", "{c.healthcheck}"]')
                lines.append("      interval: 15s")
                lines.append("      timeout: 5s")
                lines.append("      retries: 4")
                lines.append("      start_period: 20s")

            # Dependencias
            if c.depends_on:
                lines.append("    depends_on:")
                for dep in c.depends_on:
                    lines.append(f"      - {dep.replace('-', '_')}")

            # Redes internas
            lines.append("    networks:")
            if c.layer in [Layer.CLIENT, Layer.GATEWAY]:
                lines.append("      - public_net")
                lines.append("      - backend_net")
            elif c.layer in [Layer.PERSISTENCE, Layer.CACHE]:
                lines.append("      - data_net")
                lines.append("      - backend_net")
            else:
                lines.append("      - backend_net")
                lines.append("      - data_net")

            lines.append("")

        # Redes
        lines.extend([
            "networks:",
            "  public_net:",
            "    driver: bridge",
            "    name: archgen_public_net",
            "  backend_net:",
            "    driver: bridge",
            "    name: archgen_backend_net",
            "  data_net:",
            "    driver: bridge",
            "    internal: true",
            "    name: archgen_data_net",
            ""
        ])

        # Volúmenes declarados
        declared_volumes: Set[str] = set()
        for c in components:
            for vol in c.volumes:
                parts = vol.split(":")
                if len(parts) >= 2 and not parts[0].startswith(".") and not parts[0].startswith("/"):
                    declared_volumes.add(parts[0])

        if declared_volumes:
            lines.append("volumes:")
            for v in sorted(declared_volumes):
                lines.append(f"  {v}:")
                lines.append("    driver: local")

        return "\n".join(lines)

    # --------------------------------------------------------------------------
    # GENERADOR DEL REPORTE TÉCNICO (ADR - ARCHITECTURE DECISION RECORD)
    # --------------------------------------------------------------------------

    def _generate_markdown_report(
        self,
        title: str,
        pattern: ArchitecturePattern,
        summary: str,
        load_profile: str,
        compliance: str,
        target_infra: str,
        components: List[ComponentSpec],
        relationships: List[RelationshipSpec],
        validations: List[ValidationFinding],
        pillar_scores: Dict[str, int],
        trade_offs: List[TradeOff],
        mermaid_diagram: str,
        docker_compose: str
    ) -> str:
        """Sintetiza un documento formal de especificación arquitectónica en Markdown."""
        date_str = datetime.now().strftime("%Y-%m-%d")

        md: List[str] = [
            f"# 📐 Especificación y Registro de Decisiones de Arquitectura (ADR)",
            f"",
            f"**Proyecto:** {title}  ",
            f"**Fecha de Análisis:** {date_str}  ",
            f"**Patrón Principal:** `{pattern.value}`  ",
            f"**Perfil de Carga:** `{load_profile}`  ",
            f"**Marco de Cumplimiento:** `{compliance}`  ",
            f"**Entorno de Despliegue:** `{target_infra}`  ",
            f"**Generado por:** ArchGen AI (Motor Experto de Ingeniería de Software)",
            f"",
            f"---",
            f"",
            f"## 1. Resumen Ejecutivo y Visión General",
            f"",
            f"{summary}",
            f"",
            f"---",
            f"",
            f"## 2. Topología del Sistema y Diagrama C4 / Mermaid",
            f"",
            f"El siguiente diagrama refleja la distribución en capas de los componentes, sus protocolos de red y límites de aislamiento:",
            f"",
            f"```mermaid",
            f"{mermaid_diagram}",
            f"```",
            f"",
            f"---",
            f"",
            f"## 3. Catálogo Detallado de Componentes por Capas",
            f"",
            f"| ID Componente | Nombre | Capa | Tipo | Tecnología Base | Puerto Mapeado |",
            f"|---|---|---|---|---|---|"
        ]

        for c in components:
            port_text = f"`{c.port}`" if c.port else "*Interno*"
            md.append(f"| `{c.id}` | **{c.name}** | {c.layer.value} | {c.component_type.value} | {c.technology} | {port_text} |")

        md.extend([
            f"",
            f"### Descripción de Responsabilidades de Componentes:",
            f""
        ])

        for c in components:
            md.append(f"- **`{c.id}` ({c.name}):** {c.description}")

        md.extend([
            f"",
            f"---",
            f"",
            f"## 4. Auditoría de Calidad Arquitectónica (Marco Well-Architected)",
            f"",
            f"### Puntuaciones de Conformidad Técnica por Pilar:",
            f""
        ])

        for pillar_name, score in pillar_scores.items():
            bar = "█" * (score // 10) + "░" * (10 - (score // 10))
            md.append(f"- **{pillar_name}:** `{score}/100` [{bar}]")

        md.extend([
            f"",
            f"### Hallazgos, Alertas y Recomendaciones:",
            f""
        ])

        for v in validations:
            badge = "🟢 INFO" if v.severity == Severity.INFO else ("🟡 ADVERTENCIA" if v.severity == Severity.WARNING else "🔴 CRÍTICO")
            md.extend([
                f"#### [{badge}] {v.title} *({v.pillar.value})*",
                f"- **Diagnóstico:** {v.description}",
                f"- **Recomendación de Ingeniería:** {v.recommendation}",
                f""
            ])

        md.extend([
            f"---",
            f"",
            f"## 5. Matriz de Compensaciones y Compromisos (Trade-offs)",
            f"",
            f"Toda decisión de arquitectura involucra balances entre atributos de calidad antagónicos:",
            f"",
            f"| Decisión / Concepto | Ventaja Estratégica | Costo o Desventaja | Mitigación Técnica Propuesta |",
            f"|---|---|---|---|"
        ])

        for to in trade_offs:
            md.append(f"| **{to.concept}** | {to.advantage} | {to.drawback} | {to.mitigation} |")

        md.extend([
            f"",
            f"---",
            f"",
            f"## 6. Especificación de Contenedores (`docker-compose.yml`)",
            f"",
            f"Este archivo permite desplegar la arquitectura completa de manera reproducible en entornos de laboratorio o CI/CD:",
            f"",
            f"```yaml",
            f"{docker_compose}",
            f"```",
            f"",
            f"### Guía Rápida de Despliegue DevOps:",
            f"1. Guardar el bloque YAML anterior como `docker-compose.yml`.",
            f"2. Ejecutar en PowerShell o Bash: `docker compose up -d`.",
            f"3. Verificar el estado de salud de los contenedores: `docker compose ps`.",
            f"4. Inspeccionar registros centralizados: `docker compose logs -f --tail=100`.",
            f"",
            f"---",
            f"",
            f"*Documento compilado automáticamente con rigurosidad académica y estándares profesionales por **ArchGen AI**.*"
        ])

        return "\n".join(md)

    # --------------------------------------------------------------------------
    # MÉTODOS DE SOPORTE PARA TEXTO Y RESÚMENES
    # --------------------------------------------------------------------------

    def _generate_title(self, domain: str, pattern: ArchitecturePattern) -> str:
        """Crea un título representativo del sistema."""
        domain_names = {
            "ecommerce": "Plataforma de E-Commerce & Retail Distribuida",
            "fintech": "Core Financiero y Motor de Pagos de Alta Seguridad",
            "iot": "Sistema de Telemetría Masiva y Streaming IoT",
            "health": "Plataforma de Historia Clínica y Salud Digital (HIPAA)",
            "social": "Plataforma de Red Social & Mensajería Reactiva",
            "saas": "Solución SaaS Empresarial Multi-Tenant",
            "logistics": "Sistema de Gestión Logística y Trazabilidad en Tiempo Real",
            "general": "Sistema Empresarial Modular y Escalable"
        }
        return domain_names.get(domain, "Arquitectura de Software Empresarial")

    def _generate_summary(
        self,
        title: str,
        pattern: ArchitecturePattern,
        components: List[ComponentSpec],
        load_profile: str
    ) -> str:
        """Sintetiza un resumen ejecutivo de la solución diseñada."""
        total_comps = len(components)
        db_count = sum(1 for c in components if c.component_type in [ComponentType.DATABASE, ComponentType.STORAGE])
        svc_count = sum(1 for c in components if c.component_type == ComponentType.SERVICE)

        return (
            f"La presente solución formula el diseño para **{title}**, fundamentado en el patrón de "
            f"**{pattern.value}**. La arquitectura está concebida para soportar un régimen de carga **{load_profile}**, "
            f"garantizando desacoplamiento estructural, alta disponibilidad y mantenibilidad continua. "
            f"El sistema articula un total de **{total_comps} componentes clave**, incluyendo **{svc_count} servicios de negocio "
            f"especializados**, **{db_count} motores de persistencia diferenciados**, capas perimetrales de Reverse Proxy/Gateway, "
            f"aceleración en memoria y una plataforma integral de telemetría y observabilidad."
        )


# ==============================================================================
# EJECUCIÓN DIRECTA PARA PRUEBAS RÁPIDAS
# ==============================================================================

if __name__ == "__main__":
    generator = ArchitectureGenerator()
    test_req = (
        "Requiero un sistema de e-commerce con alta concurrencia capaz de soportar Black Friday, "
        "con gestión de carrito, inventario en tiempo real, pasarela de pagos con tarjetas de crédito "
        "y notificaciones asíncronas por correo electrónico y SMS."
    )
    result = generator.analyze_and_generate(
        requirements_text=test_req,
        preferred_pattern="Microservicios Distribuidos",
        load_profile="Alta (10k - 100k RPM)",
        compliance="Financiero / PCI-DSS"
    )
    print(f"=== {result.title} ===")
    print(f"Patrón: {result.pattern.value}")
    print(f"Componentes: {len(result.components)}")
    print(f"Hallazgos de auditoría: {len(result.validations)}")
    print("Salida de prueba generada con éxito.")
