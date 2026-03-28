# Diseño de Evolución v2: Dashboard Analítico Farma EC

**Fecha:** 2026-03-28  
**Estado:** Propuesta Aprobada  
**Enfoque:** Dashboard con Barra Lateral y Paginación (SQLite)  
**Estética:** Dark Glassmorphism / Dashboard Industrial (Premium)

## 1. Visión General
Transformar la aplicación en un centro de control farmacéutico profesional. La interfaz permitirá navegar más de 15,000 registros mediante una barra lateral organizada por categorías genéricas y un dashboard estadístico que resume el estado del catálogo nacional (RF1.1 - RF4.3).

## 2. Decisiones de Arquitectura
Se mantiene la estructura modular sobre SQLite para garantizar alto rendimiento con miles de registros:

- **Capa de Persistencia (`farma_ec.db`):** Base de datos SQLite optimizada con índices en `nombre` y `categoria`.
- **Servicios (`logic/`):**
  - `SyncService`: Refactorizado para extraer `categoria` desde los campos `Nombre_generico` o `Clasificacion_atc` del archivo ARCSA.
  - `DatabaseService`: Incorpora métodos estadísticos para el Dashboard (conteo por estado, por categoría, etc.).
- **Interfaz (`app.py` + `ui/`):**
  - **Layout Principal:** División `ui.left_drawer` (Barra Lateral) y `ui.scroll_area` (Contenido Principal).
  - **Dashboard dinámico:** Tarjetas KPI y gráficos de estado generados mediante NiceGUI.

## 3. Especificaciones Visuales (Branding)
- **Tema:** Oscuro (Dark Mode) con degradados sutiles.
- **Efectos:** Glassmorphism (fondos semi-transparentes con `backdrop-blur`).
- **Paleta de Colores:**
  - Primario: `#4CAF50` (Éxito/Vigente)
  - Alerta: `#FF5252` (Crítico/No Vigente)
  - Fondo: `#121212` (Gris profundo) con tarjetas en `#1E1E1E`.
- **Tipografía:** Montserrat o Roboto para títulos, Inter para datos técnicos.

## 4. Funcionalidades Detalladas
- **Barra Lateral (RF1.3):**
  - Enlace a "Resumen General" (Dashboard).
  - Listado de las 10 categorías con mayor volumen de fármacos.
  - Buscador de categorías para filtrar el catálogo rápidamente.
- **Dashboard Estadístico:**
  - Resumen de 4 KPIs (Total, Vigentes, Categorías, Fabricantes).
  - Gráfico de barras horizontales NiceGUI para la distribución de estados.
- **Catálogo con Paginación:**
  - Carga inicial de 50 registros.
  - Botón "Cargar más" que consulta la base de datos con `OFFSET` para visualizar el catálogo completo (15k+).

## 5. Estructura de Archivos
```text
AgenteAsistencia/
├── app.py                # Layout de Dashboard y Sidebar
├── farma_ec.db           # Base de datos SQLite (15k+ registros)
├── logic/
│   ├── database.py       # Consultas estadísticas y CRUD
│   ├── sync_svc.py       # Extracción ARCSA robusta
│   └── farma_svc.py      # Puente entre UI y DB
└── ui/
    ├── components.py     # KPI Cards, Sidebar Menu, Medicine Cards
    └── styles.py         # Clases CSS para Glassmorphism
```

## 6. Plan de Verificación
- **Métricas:** Comparar los totales del Dashboard con `SELECT COUNT(*)` en SQLite.
- **Navegación:** Asegurar que al hacer clic en "Antibióticos" en el Sidebar, el catálogo se filtre correctamente.
- **Botón Actualizar:** Verificar que el trigger de descarga y procesamiento (streaming) actualiza los KPIs del Dashboard sin recargar la página completa.
