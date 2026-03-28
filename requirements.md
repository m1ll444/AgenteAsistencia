# Documento de Especificación de Requerimientos - Catálogo de Medicamentos Ecuador

## 1. Identificación del Proyecto

### Nombre del Proyecto
**Catálogo de Medicamentos - Ecuador (Catálogo Farma EC)**

### Carrera Objetivo
Ingeniería en Sistemas / Ingeniería Informática - Especializado en aplicaciones de salud digital y gestión farmacéutica/ Química Farmacéutica.

### Tipo de Aplicación
Aplicación web interactiva para consulta y búsqueda de medicamentos registrados en Ecuador.

---

## 2. Problemática Identificada

### Contexto
En Ecuador, los usuarios reciben prescripciones médicas con nombres de medicamentos pero carecen de una herramienta accesible para buscar información rápida y confiable sobre:
- Formas farmacéuticas disponibles
- Concentraciones específicas
- Categoría terapéutica del medicamento
- Disponibilidad en el mercado nacional

### Impacto
Esta falta de información genera:
1. **Confusión en la medicación:** Pacientes no pueden verificar si están tomando el medicamento correcto.
2. **Acceso limitado:** No existe un catálogo unificado de fácil consulta.
3. **Tiempo de búsqueda:** Requiere recurrir a múltiples fuentes para validar información.
4. **Incertidumbre:** Pacientes desconocen categorías terapéuticas (analgésicos, antibióticos, etc.).

### Solución Propuesta
Crear una herramienta de búsqueda rápida y eficiente que permita a ciudadanos ecuatorianos acceder al catálogo nacional de medicamentos registrados con información clara y organizada.

---

## 3. Funcionalidades Principales (MVP)

### Módulo 1: Búsqueda y Filtrado
* **RF1.1:** Búsqueda por nombre de medicamento (búsqueda en tiempo real - real-time search).
* **RF1.2:** Filtrado por categoría terapéutica (Analgésicos, Antibióticos, Antiinflamatorios, etc.).
* **RF1.3:** Búsqueda combinada (nombre + categoría simultáneamente).

* **RF1.4:** Sincronización automática con la base de datos oficial de ARCSA (descarga de Excel dinámico).

### Módulo 2: Visualización de Medicamentos
* **RF2.1:** Presentación de cada medicamento en tarjetas informativas enriquecidas con:
  - Nombre del medicamento y Fabricante (Titular)
  - Forma farmacéutica y Concentración
  - Categoría terapéutica (con badge distintivo)
  - Número de Registro Sanitario
  - Estado de Vigencia (Badge dinámico: Verde para vigente, Rojo para no vigente)
* **RF2.2:** Interfaz responsiva que se adapta a diferentes tamaños de pantalla.
* **RF2.3:** Efectos visuales mejorados (hover effect, transiciones suaves).

### Módulo 3: Base de Datos de Medicamentos
* **RF3.1:** Catálogo inicial con medicamentos ecuatorianos comunes (MVP con 7+ medicamentos de prueba).
* **RF3.2:** Estructura de datos flexible para fácil expansión.

### Módulo 4: Experiencia de Usuario
* **RF4.1:** Mensaje de retroalimentación cuando no se encuentran resultados.
* **RF4.2:** Header con branding nacional (icono médico, colores institucionales).
* **RF4.3:** Interfaz intuitiva sin curva de aprendizaje.

---

## 4. Stack Tecnológico Utilizado

### Frontend
* **Framework:** **NiceGUI** (Python-based UI framework)
  - Razón: Permite crear interfaces web modernas con Python, sin necesidad de JavaScript/HTML/CSS complejo.
  - Desarrollo rápido de prototipos
  - Facilita integración con backend Python

### Backend
* **Lenguaje:** **Python 3.x**
  - Razón: Simplifica la lógica de búsqueda, filtrado y gestión de datos farmacéuticos.

### Base de Datos (Actual)
* **Formato:** Datos en memoria (JSON-like structure) - MVP sin persistencia
  - Razón: Suficiente para etapa inicial de demostración.
  
### Hosting y Despliegue
* **Servidor:** NiceGUI UI Server (desarrollo local)
  - Puerto: 8080
  - Reload automático habilitado para desarrollo ágil

### Diseño y Estilo
* **Colores Institucionales:**
  - Primary: #2E7D32 (Verde - salud/medicina)
  - Secondary: #1565C0 (Azul - confianza)
  - Accent: #F9A825 (Amarillo/Dorado - énfasis)
* **Componentes UI:** Cards, Badges, Separadores, Inputs con validación

---

## 5. Requerimientos No Funcionales

* **RNF1 (Performance):** La búsqueda debe ejecutarse instantáneamente al escribir (búsqueda en tiempo real sin lag).
* **RNF2 (Usabilidad):** La interfaz debe ser intuitiva y usable sin capacitación previa.
* **RNF3 (Responsividad):** Debe funcionar en web browsers (Chrome, Firefox, Safari, Edge).
* **RNF4 (Escalabilidad futura):** Arquitectura preparada para migración a base de datos SQL (PostgreSQL) sin rediseño mayor.
* **RNF5 (Accesibilidad):** Texto legible, contraste adecuado, navegación por teclado.

---

## 6. Estructura de Datos (Medicamentos)

```json
{
  "nombre": "string",
  "forma": "string (Tableta, Cápsula, Inhalador, Jarabe, etc.)",
  "concentracion": "string (ej: 500 mg, 100 mcg)",
  "categoria": "string (Analgésico, Antibiótico, Antiinflamatorio, etc.)"
}
```

### Medicamentos Iniciales en Catálogo
1. Paracetamol - Tableta 500 mg - Analgésico
2. Amoxicilina - Cápsula 500 mg - Antibiótico
3. Ibuprofeno - Tableta 400 mg - Antiinflamatorio
4. Metformina - Tableta 850 mg - Antidiabético
5. Losartán - Tableta 50 mg - Antihipertensivo
6. Omeprazol - Cápsula 20 mg - Antiulceroso
7. Salbutamol - Inhalador 100 mcg - Broncodilatador

---

## 7. Próximas Fases (Futuro)

### Fase II: Expansión
- [ ] Backend en FastAPI o Flask para gestión más robusta
- [ ] Persistencia en PostgreSQL
- [ ] API REST para futuras aplicaciones móviles
- [ ] Autenticación de usuarios (opcional)

### Fase III: Mejoras Avanzadas
- [ ] Integración con ARCSA (Agencia de Regulación y Control Sanitario)
- [ ] Historial de búsquedas del usuario
- [ ] Sistema de ratings para medicamentos
- [ ] Información de efectos secundarios y contraindicaciones

---

**Última actualización:** Marzo 26, 2026
