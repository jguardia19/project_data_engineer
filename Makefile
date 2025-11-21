
# ============================================================================
# MAKEFILE PARA PROYECTO YOLO + HIVE ETL
# Ingeniero: Andrés Felipe Rojas Parra
# Maestria en Big Data y Data Science - 2024-2025
# ============================================================================

# =========================
# CONFIGURACIÓN DEL PROYECTO
# =========================
PROJECT_NAME := yolo_hive_project
PYTHON_VERSION := 3.10
VENV_PATH := enviroments/project_final

# Detectar sistema operativo
ifeq ($(OS),Windows_NT)
    PYTHON_BIN := py -3.10
    VENV_PYTHON := $(VENV_PATH)/Scripts/python.exe
    VENV_PIP := $(VENV_PATH)/Scripts/pip.exe
    ACTIVATE := $(VENV_PATH)/Scripts/activate
else
    PYTHON_BIN := python3.10
    VENV_PYTHON := $(VENV_PATH)/bin/python
    VENV_PIP := $(VENV_PATH)/bin/pip
    ACTIVATE := $(VENV_PATH)/bin/activate
endif

# =========================
# CONFIGURACIÓN DE HIVE
# =========================
HIVE_USER := jose_dev
HIVE_DB := yolo_project
HIVE_TABLE := yolo_objects
HIVE_HOST := localhost
HIVE_PORT := 10000

# =========================
# DIRECTORIOS DEL PROYECTO
# =========================
DIRS := imagenes_entrada videos_entrada data data/logs sql tests src

# =========================
# TARGETS PRINCIPALES
# =========================

.PHONY: help setup clean test lint format run-all run-classification run-etl

help:
    @echo "🎯 MAKEFILE PARA PROYECTO YOLO + HIVE ETL"
    @echo "=========================================="
    @echo ""
    @echo "📋 COMANDOS DISPONIBLES:"
    @echo "  setup              - Configurar entorno virtual y dependencias"
    @echo "  clean              - Limpiar archivos temporales"
    @echo "  create-dirs        - Crear estructura de directorios"
    @echo ""
    @echo "🚀 EJECUCIÓN:"
    @echo "  run-all            - Pipeline completo (clasificación + ETL)"
    @echo "  run-classification - Solo sistema YOLO"
    @echo "  run-etl           - Solo sistema ETL"
    @echo ""
    @echo "🧪 DESARROLLO:"
    @echo "  test              - Ejecutar pruebas unitarias"
    @echo "  lint              - Verificar código con pylint"
    @echo "  format            - Formatear código con black"
    @echo ""
    @echo "🗄️ HIVE:"
    @echo "  show-hive-config  - Mostrar configuración de Hive"
    @echo "  create-hive-table - Crear tabla en Hive"
    @echo "  run-queries       - Ejecutar consultas analíticas"
    @echo ""
    @echo "📊 VERIFICACIÓN:"
    @echo "  check-services    - Verificar HDFS y Hive"
    @echo "  show-stats        - Mostrar estadísticas del proyecto"

# =========================
# CONFIGURACIÓN INICIAL
# =========================

setup: create-dirs create-venv install-deps
    @echo "✅ Configuración completa del proyecto"

create-dirs:
    @echo "📁 Creando estructura de directorios..."
    @mkdir -p $(DIRS)
    @echo "✅ Directorios creados"

create-venv:
    @echo "🐍 Creando entorno virtual..."
    @if [ ! -d "$(VENV_PATH)" ]; then \
        $(PYTHON_BIN) -m venv $(VENV_PATH); \
        echo "✅ Entorno virtual creado en: $(VENV_PATH)"; \
    else \
        echo "ℹ️  Entorno virtual ya existe"; \
    fi

install-deps: create-venv
    @echo "📦 Instalando dependencias..."
    @$(VENV_PIP) install --upgrade pip setuptools wheel
    @$(VENV_PIP) install -r requirements.txt
    @echo "✅ Dependencias instaladas"

# =========================
# EJECUCIÓN DEL PROYECTO
# =========================

run-all: check-venv
    @echo "🚀 Ejecutando pipeline completo..."
    @$(VENV_PYTHON) main.py
    @echo "✅ Pipeline completado"

run-classification: check-venv
    @echo "🤖 Ejecutando solo clasificación YOLO..."
    @$(VENV_PYTHON) src/sistema_clasificacion_con_batches.py
    @echo "✅ Clasificación completada"

run-etl: check-venv
    @echo "📊 Ejecutando solo sistema ETL..."
    @$(VENV_PYTHON) src/sistema_batch_etl.py
    @echo "✅ ETL completado"

# =========================
# DESARROLLO Y PRUEBAS
# =========================

test: check-venv
    @echo "🧪 Ejecutando pruebas unitarias..."
    @$(VENV_PYTHON) -m pytest tests/ -v --tb=short
    @echo "✅ Pruebas completadas"

test-coverage: check-venv
    @echo "📊 Ejecutando pruebas con cobertura..."
    @$(VENV_PYTHON) -m pytest tests/ --cov=src --cov-report=html --cov-report=term
    @echo "✅ Reporte de cobertura generado en htmlcov/"

lint: check-venv
    @echo "🔍 Verificando código con pylint..."
    @$(VENV_PYTHON) -m pylint src/ --disable=C0114,C0116,R0903 || true
    @echo "✅ Linting completado"

format: check-venv
    @echo "🎨 Formateando código con black..."
    @$(VENV_PYTHON) -m black src/ tests/ *.py
    @echo "✅ Código formateado"

# =========================
# HIVE Y BASE DE DATOS
# =========================

show-hive-config:
    @echo "🗄️ CONFIGURACIÓN DE HIVE:"
    @echo "========================="
    @echo "Usuario: $(HIVE_USER)"
    @echo "Host: $(HIVE_HOST):$(HIVE_PORT)"
    @echo "Base de datos: $(HIVE_DB)"
    @echo "Tabla: $(HIVE_TABLE)"

create-hive-table: check-venv
    @echo "🗄️ Creando tabla en Hive..."
    @$(VENV_PYTHON) -c "from src.sistema_batch_etl import SistemaBatchETL; etl = SistemaBatchETL(); etl.conectar_hive(); etl.crear_base_datos_y_tabla(); etl.cerrar_conexion()"
    @echo "✅ Tabla creada en Hive"

run-queries: check-venv
    @echo "📈 Ejecutando consultas analíticas..."
    @$(VENV_PYTHON) sql/ejecutar_queries.py
    @echo "✅ Consultas ejecutadas"

# =========================
# VERIFICACIÓN Y DIAGNÓSTICO
# =========================

check-services:
    @echo "🔍 Verificando servicios..."
    @echo "HDFS:"
    @hdfs dfsadmin -report | head -5 || echo "❌ HDFS no disponible"
    @echo ""
    @echo "Hive:"
    @jps | grep -E "(HiveServer2|RunJar)" || echo "❌ Hive no disponible"

show-stats: check-venv
    @echo "📊 Estadísticas del proyecto:"
    @echo "============================="
    @echo "Imágenes en entrada: $$(ls imagenes_entrada/ 2>/dev/null | wc -l)"
    @echo "Videos en entrada: $$(ls videos_entrada/ 2>/dev/null | wc -l)"
    @echo "CSVs generados: $$(ls data/*.csv 2>/dev/null | wc -l)"
    @if [ -f "$(VENV_PYTHON)" ]; then \
        echo "Registros en Hive:"; \
        $(VENV_PYTHON) -c "from src.sistema_batch_etl import SistemaBatchETL; etl = SistemaBatchETL(); etl.conectar_hive(); etl.mostrar_estadisticas(); etl.cerrar_conexion()" 2>/dev/null || echo "❌ No se pudo conectar a Hive"; \
    fi

# =========================
# LIMPIEZA
# =========================

clean:
    @echo "🧹 Limpiando archivos temporales..."
    @rm -rf __pycache__ src/__pycache__ tests/__pycache__
    @rm -rf .pytest_cache htmlcov/ .coverage
    @rm -rf *.pyc src/*.pyc tests/*.pyc
    @rm -rf data/*.csv data/logs/*.log
    @echo "✅ Limpieza completada"

clean-all: clean
    @echo "🧹 Limpieza completa (incluyendo entorno virtual)..."
    @rm -rf $(VENV_PATH)
    @echo "✅ Limpieza completa terminada"

# =========================
# UTILIDADES
# =========================

check-venv:
    @if [ ! -f "$(VENV_PYTHON)" ]; then \
        echo "❌ Entorno virtual no encontrado. Ejecuta: make setup"; \
        exit 1; \
    fi

install-dev: check-venv
    @echo "🛠️ Instalando herramientas de desarrollo..."
    @$(VENV_PIP) install pytest pylint black coverage pytest-cov
    @echo "✅ Herramientas de desarrollo instaladas"

# =========================
# INFORMACIÓN DEL SISTEMA
# =========================

info:
    @echo "ℹ️  INFORMACIÓN DEL SISTEMA:"
    @echo "=========================="
    @echo "SO: $(shell uname -s 2>/dev/null || echo Windows)"
    @echo "Python: $(PYTHON_BIN)"
    @echo "Entorno virtual: $(VENV_PATH)"
    @echo "Proyecto: $(PROJECT_NAME)"
    @echo "Hive: $(HIVE_USER)@$(HIVE_HOST):$(HIVE_PORT)/$(HIVE_DB)"

# Target por defecto
.DEFAULT_GOAL := help
