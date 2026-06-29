# Informe del Proyecto

**Sistema de Planificación de Eventos y Gestión de recursos en el sector hotelero**

**Autor:** Omar Alejandro Cuellar Ash
**Lenguaje empleado:** Python 3.13.5
**Dependencias empleadas:** Streamlit 1.53.1

---

## 1. Introducción

El presente proyecto surge con el objetivo de concebir una herramienta funcional destinada a la organización logística de eventos. La aplicación desarrollada, _ÁGORA_, permite a un usuario coordinador gestionar la creación de eventos, administrar un inventario de recursos asociados y, principalmente, **prevenir conflictos de disponibilidad horaria** entre distintos eventos que comparten recursos limitados.

El propósito fundamental del sistema es garantizar la integridad de la programación, evitando la doble reserva **mediante un motor de verificación de solapamientos temporales**. Este informe detalla el alcance del programa, las decisiones de diseño, las lecciones extraídas durante el desarrollo, ejemplos de uso y las dificultades técnicas resueltas a lo largo del proceso.

---

## 2. Definición del dominio: sector hotelero

Para dotar de contexto al sistema, se acotó el dominio de aplicación al **sector de la hotelería y los centros de convenciones**. Este entorno resulta particularmente idóneo para validar la utilidad del sistema, debido a las siguientes características en sus operaciones:

- **Concurrencia de eventos:** Los establecimientos hoteleros suelen albergar múltiples eventos de índole diversa (bodas, congresos empresariales, seminarios, banquetes) de manera simultánea en un mismo día. La ausencia de un control centralizado derivaría en solapamientos logísticos inevitables.

- **Recursos críticos y limitados:** Los activos del hotel —como salones, equipos de proyección, sistemas de sonido y personal de servicio (meseros, técnicos)— son finitos y demandan una asignación eficiente. En este contexto, el término "recurso" se refiere tanto a elementos físicos (salas, datashows) como al personal de alimentos y bebidas.

- **Dependencia temporal estricta:** La actividad hotelera se rige por horarios rigurosos. Un error en la asignación de un salón puede desencadenar una reacción en cadena que afecte la facturación y la reputación del hotel.

- **Oportunidad de negocio:** La visualización clara de los intervalos libres permite al coordinador maximizar la ocupación de los espacios, reduciendo los tiempos muertos y optimizar los ingresos.

Por consiguiente, el sistema _ÁGORA_ modela cada **Evento** como un compromiso contractual con un cliente (con atributos de fecha, hora y duración), y cada **Recurso** como un activo tangible del hotel. El software impide asignaciones que vulneren la disponibilidad de los recursos.

---

## 3. Diseño del sistema y justificación de decisiones técnicas

El desarrollo se estructuró siguiendo con especial énfasis en la claridad, escalabilidad y mantenibilidad del código.

### 3.1. Paradigma de programación orientada a objetos (POO)

Se optó por el paradigma orientado a objetos para representar las entidades del dominio.

- **Clase `Resource`:** Encapsula los atributos identificativos de un activo hotelero (`id`, `nombre`, `tipo`).
- **Clase `Event`:** Contiene los atributos propios de una reserva (`id`, `nombre`, `inicio` como objeto `datetime`, `duracion` en horas flotantes) y una colección de referencias (lista de IDs) a los recursos asignados.
- **Clase `Planification`:** Actúa como el núcleo operativo del sistema. Gestiona los diccionarios maestros (`self.eventos` y `self.recursos`) y alberga los métodos de negocio para la creación, eliminación, asignación y verificación.

La justificación se basa en el principio de responsabilidad única; cualquier modificación futura en la estructura de un evento, por ejemplo, la adición del campo "presupuesto", se ajusta a la clase `Event`, sin afectar a la lógica de asignación de recursos.

### 3.2. Estructuras de Datos: diccionarios vs. listas

Para el almacenamiento en memoria de los registros, **se emplearon diccionarios indexados por un identificador único** (`id` entero autoincremental).

La operación de verificación de disponibilidad de un recurso requiere su recuperación inmediata a partir de su identificador. **La complejidad algorítmica de acceso en un diccionario** es O(1) en media, frente a la O(n) de una búsqueda secuencial en una lista. Dado que la base de datos del sistema puede crecer considerablemente en un entorno hotelero (decenas de salas y centenares de eventos mensuales), esta decisión es crítica para el rendimiento del sistema.

### 3.3. Gestión temporal mediante el Módulo `datetime`

Inicialmente se pensó en el uso de cadenas de texto para representar fechas; no obstante, se implementó el módulo `datetime` por sus ventajas. Este módulo permite el cálculo exacto de la finalización de un evento (`inicio + timedelta(hours=duracion)`) y la comparación directa de franjas horarias mediante operadores relacionales. En el ámbito hotelero, donde los horarios de montaje y desmontaje son estrictos, la precisión temporal es un requisito obligatorio.

### 3.4. Mecanismo de persistencia: serialización JSON personalizada

Se implementó la persistencia de datos mediante el formato JSON, en lugar de un sistema de gestión de bases de datos relacional, para simplificar la arquitectura del primer prototipo. El formato JSON nativo no serializa objetos `datetime`. Para resolver esta limitación, se desarrolló **un encoder y decoder personalizados**. Los objetos `datetime` se convierten a cadenas ISO-8601 durante el volcado y se reconstruyen como objetos temporales al cargar el archivo `Events.json`. Este enfoque asegura que el coordinador pueda interrumpir y reanudar la sesión sin pérdida de información.

### 3.5. Interfaz de Usuario: Aplicación web interactiva con Streamlit

Se decidió implementar una interfaz web interactiva empleando el framework Streamlit, en lugar de la consola. Esta elección obedece a tres razones principales. En primer lugar, el perfil del usuario final (coordinadores de eventos y personal hotelero) que no está familiarizado con entornos de terminal. En segundo lugar, Streamlit ofrece widgets nativos de entrada de fechas, horas y números que incorporan validaciones automáticas, eliminando la necesidad de escribir bucles de limpieza y previniendo errores de tecleo. En tercer lugar, Streamlit permite iterar y depurar visualmente el código en tiempo real, acelerando el tiempo de desarrollo. Además, el uso de Streamlit fue recomendado por los profesores de la asignatura por su relativa sencillez y rápida curva de aprendizaje. La aplicación puede desplegarse en un servidor local y es accesible desde múltiples dispositivos, lo que facilita la colaboración entre distintos departamentos del hotel.

---

## 4. Aprendizajes

Se pueden resumir un conjunto de lecciones aprendidas durante el proceso:

- Se ha interiorizado la necesidad de validar rigurosamente los formatos de entrada de fechas y horas. Es cierto que Streamlit facilita la captura, sin embargo, la comparación sigue siendo crítica en las operaciones temporales.

- La implementación del algoritmo de verificación de solapamientos (`inicio1 < fin2 and inicio2 < fin1`) constituye una aplicación directa de la teoría de conjuntos a intervalos.

- La versión inicial del prototipo almacenaba los datos en archivos de texto planos, lo que dificultaba la extensión de los atributos. **Es importante una planificación adelantada de la estructura de datos para evitar el costo elevado de refactorización en fases posteriores.**

- La habilidad para interpretar los mensajes de excepción de Python ha mejorado. La capacidad de rastrear el origen del error acelera el proceso de depuración.

- Se ha comprendido que el usuario final no posee conocimientos técnicos. Es por eso que se debe prestar especial atención a los mensajes del sistema: descriptivos y orientados a la acción.

- Se ha constatado las bondades de Streamlit como framework de nivel para acelerar la entrega de un producto funcional y presentable.

---

## 5. Guía de uso de ÁGORA (Casos de Ejemplo)

**El sistema se ejecuta como una aplicación web. Para iniciarla, el usuario debe situarse en el directorio del proyecto y ejecutar en la terminal el comando `streamlit run main.py`. Automáticamente se abrirá una pestaña en el navegador predeterminado con la interfaz de ÁGORA.** A continuación, se ilustra un flujo de trabajo típico en un contexto hotelero.

### 5.1. Gestión de recursos físicos presentes en el inventario

En la sección "Gestionar Inventario" del panel lateral se halla una visualización de cada recurso junto con su respectiva cantidad total, además de presentar los botones "Disminuir cantidad" y "Aumentar cantidad" para modificar tales cantidades.

- Al presionar **Disminuir cantidad**, se le presenta al usuario un cajón de selección de activos con la cantidad que pretende restar del inventario. Tras realizarse clic en el botón "Confirmar", el sistema comprueba que la operación que se está llevando a cabo no producirá conflictos en la planificación de eventos En caso de haber conflicros, no se descontará ninguna cantidad del recurso en cuestión del inventario y se informará de los eventos que se vean afectados, recomendando que se modificada la planificación

- Al presionar **Aumentar cantidad**, se muestra un cajón de selección con gran parecido al descrito anteriormente, excepto que no habrá problemáticas que el programa necesite considerar.

**Se pueden añadir otros recursos como Proyectores (tipo Audiovisual) o Equipo de sonido.**

### 5.2. Crear evento

A continuación, se crea un evento. La interfaz presenta un formulario con:

- **Tipo de evento:** _Boda_
- **Descripción del evento:** _Boda de Juan y Josefa_
- **Fechas y horas de inicio y fin del evento:** mediante un selector de fecha y otro de hora (widgets de Streamlit), el usuario elige, por ejemplo, _2026-07-20_ y _18:00_.

**Al pulsar Crear Evento, la aplicación añade el evento a la lista y lo muestra en la sección "Eventos planificados", con su identificador interno (p. ej., ID 101).**

### 5.3. Asignación de recursos y validación de conflictos

En el mismo menú, el coordinador selecciona un evento y los recursos con la cantidad correspondiente que desea incorporar al evento. El programa verifica automáticamente la disponibilidad del recurso en esa franja horaria. Si se dispone de la cantidad requerida, la asignación se completa y se actualiza la vista. En caso contrario, se muestra un mensaje de error, como el siguiente:

> "El recurso 'Proyector 1' ya está ocupado desde las 18:00 hasta las 23:00 (Boda 1). No se puede asignar."

### 5.4. Consulta de la programación de eventos del hotel

El coordinador puede visualizar la planificación completa en la sección "Programa de eventos". Allí se listan todos los eventos con sus horarios y los recursos asignados a cada uno. Esta vista se actualiza dinámicamente tras cada operación, permitiendo tomar decisiones sobre nuevas solicitudes.

---

## 6. Dificultades técnicas encontradas y soluciones

Durante la programación se identificaron varias dificultades técnicas. La mayoría afectaban la lógica de negocio, independientemente de la interfaz utilizada. El uso de Streamlit también tuvo algunos desafíos específicos.

### 6.1. Verificación de solapamiento de intervalos

La primera aproximación para comprobar la disponibilidad consistía en verificar únicamente si la fecha de inicio del nuevo evento se encontraba dentro del rango del evento existente. Sin embargo, esta lógica fallaba cuando el nuevo evento contenía completamente al evento existente (inicio anterior y fin posterior). Para solucionarlo se implementó una función de intersección de intervalos.
