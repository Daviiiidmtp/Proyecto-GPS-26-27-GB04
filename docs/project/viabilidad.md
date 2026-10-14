# Cálculo de la Capacidad del Equipo

En esta sección vamos a calcular las horas reales de trabajo que nuestro equipo puede dedicar al proyecto **El Hogar del Hobbit**. El objetivo es hacer una planificación realista, basándonos en el tiempo que de verdad tenemos disponible para programar después de restar reuniones, descansos y el trabajo de otras asignaturas.

Aquí detallamos las horas diarias de cada integrante para un sprint normal de 5 días:

| Miembro (Rol) | Horas por día | Otros proyectos | Tiempo personal | Actividades gestión | Horas-esfuerzo disponibles |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **David Muñoz Torrero Pérez** (Scrum Master) | 5 | 2 | 1,5 | 0,5 | **1** |
| **Celia González Cerrato** (Product Owner) | 5 | 1,5 | 1 | 0,5 | **2** |
| **Adrián Muñoz Ruiz** (DevOps / QA) | 4 | 1,5 | 0,5 | 1 | **1** |
| **Jose Antonio Ramos Barragán** (Lead Tech) | 5 | 2 | 1 | 1 | **1** |
| **María Belén Muñoz Ortiz** (Developer) | 4,5 | 2 | 1 | 0,5 | **1** |
| **Total / Día** | | | | | **6** |
| **Total / Sprint (5 días)** | | | | | **30** |

> **Nota:** Las "horas-esfuerzo disponibles" salen de coger nuestras horas base y restarles el tiempo que dedicamos a otras asignaturas, asuntos personales y tareas de gestión o reuniones de Scrum.

## Justificación de los Tiempos Descontados

Para cumplir con lo que pide la práctica, no hemos restado el mismo porcentaje de tiempo a todo el mundo de forma automática. Hemos ajustado los descuentos a la situación real y al rol de cada persona:

*   **Horas base y otros proyectos:** Partimos de unas 4 a 5 horas diarias según la disponibilidad de cada uno. A todos nos hemos restado entre 1,5 y 2 horas al día para cubrir la carga de estudio y trabajos de otras asignaturas.
*   **Tareas de gestión según el rol:**
    *   **DevOps/QA (Adrián Muñoz Ruiz) y Lead Tech (Jose Antonio Ramos Barragán):** Se les descuenta 1 hora diaria de programación porque necesitan ese tiempo para organizar cosas técnicas: automatizar las pruebas y tomar decisiones sobre cómo estructurar el código.
    *   **Scrum Master (David Muñoz Torrero Pérez) y Product Owner (Celia González Cerrato):** Tienen un descuento de 0,5 horas al día que usarán para organizar las reuniones del equipo, solucionar bloqueos y mantener al día la lista de tareas del proyecto.
    *   **Developer (María Belén Muñoz Ortiz):** Se le descuenta 0,5 horas diarias para coordinarse técnicamente con el Lead Tech y ayudar a revisar el trabajo de los compañeros.

## Estimación del Proyecto y Viabilidad

Para la estimación del proyecto, se ha elaborado una tabla que refleja las horas totales dedicadas a cada sprint, calculadas sumando las horas estimadas (h-p) de las Historias de Usuario asignadas a lo largo de un ciclo de 3 Sprints.

| Sprint | Horas de desarrollo requeridas |
| :--- | :--- |
| Sprint 1 | 9 |
| Sprint 2 | 9 |
| Sprint 3 | 8,5 |
| **Total** | **26,5** |

Como se puede observar, para realizar el proyecto se van a necesitar unas **22,5 horas netas**. Para confirmar que este volumen de trabajo no satura al equipo, hemos comparado estos datos con nuestro tiempo disponible:

*   **Esfuerzo total necesario:** 22,5 horas.
*   **Capacidad real del equipo (3 Sprints x 30h/semana):** 90,0 horas.
*   **Margen:** 67,5 horas.

**Conclusión:** El proyecto es asumible ya que tenemos un colchón de 67,5 horas que nos va a proteger frente a posibles bloqueos técnicos o retrasos, garantizando que no sobreasignamos tareas a ningún compañero.

## Presupuesto y Costes por Rol

Para calcular la viabilidad económica del sistema, hemos establecido tarifas por hora ajustadas a la realidad del mercado para cada perfil (esta información se ha sacado directamente de google).

| Miembro | Rol Asignado | Gestión (h/día) | Desarrollo (h/día) | Tarifa (€/h) | Coste Semanal (€) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Celia** | Product Owner | 0,5 | 2 | 27 € | 337,50 € |
| **David** | Scrum Master | 0,5 | 1 | 23 € | 172,50 € |
| **Jose Antonio** | Lead Tech | 1 | 1 | 35 € | 350,00 € |
| **Adrián** | DevOps / QA | 1 | 1 | 29 € | 290,00 € |
| **María Belén** | Developer | 0,5 | 1 | 23 € | 172,50 € |
| **Gasto Semanal**| | | | | **1.322,50 €** |

### Método de Cálculo

Para obtener el total semanal de cada integrante, asumimos semanas laborables de 5 días y aplicamos la siguiente fórmula:

**Coste Semanal** = 5 días × (Horas de Gestión + Horas de Desarrollo) × Tarifa por Hora

### Conclusión Final 

El mantenimiento de todo el equipo supone una inversión de **1.322,50 € por cada Sprint**. 

Teniendo en cuenta que haremos exactamente 3 Sprints, el coste total para entregar el software será de **3.967,50 €**. 

Este presupuesto demuestra que "El Hogar del Hobbit" es un proyecto estructurado y viable desde el punto de vista financiero.