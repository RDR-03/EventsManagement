### Sistema de Planificación de Eventos y Gestión de recursos en el sector hotelero

**Lenguaje empleado:** Python 3.13.5
**Dependencias empleadas:** Streamlit 1.53.1

---

## 1. Introducción

El presente proyecto surge con el objetivo de concebir una herramienta funcional destinada a la organización logística de eventos. La aplicación desarrollada, permite a un usuario coordinador gestionar la creación de eventos, administrar un inventario de recursos asociados y, principalmente, **prevenir conflictos de disponibilidad horaria** entre distintos eventos que comparten recursos limitados.

El propósito fundamental del sistema es garantizar la integridad de la programación, evitando la doble reserva **mediante un motor de verificación de solapamientos temporales**. Este informe detalla el alcance del programa, las decisiones de diseño, las lecciones extraídas durante el desarrollo, ejemplos de uso y las dificultades técnicas resueltas a lo largo del proceso.

---

## 2. Definición del dominio: sector hotelero

Para dotar de contexto al sistema, se acotó el dominio de aplicación al **sector de la hotelería y los centros de convenciones**. Este entorno resulta particularmente idóneo para validar la utilidad del sistema, debido a las siguientes características en sus operaciones:

- **Concurrencia de eventos:** Los establecimientos hoteleros suelen albergar múltiples eventos de índole diversa (bodas, congresos empresariales, seminarios, banquetes) de manera simultánea en un mismo día. La ausencia de un control centralizado derivaría en solapamientos logísticos inevitables.

- **Recursos críticos y limitados:** Los activos del hotel —como salones, equipos de proyección, sistemas de sonido y personal de servicio (meseros, técnicos)— son finitos y demandan una asignación eficiente. En este contexto, el término "recurso" se refiere tanto a elementos físicos (salas, datashows) como al personal de alimentos y bebidas.

- **Dependencia temporal estricta:** La actividad hotelera se rige por horarios rigurosos. Un error en la asignación de un salón puede desencadenar una reacción en cadena que afecte la facturación y la reputación del hotel.

- **Oportunidad de negocio:** La visualización clara de los intervalos libres permite al coordinador maximizar la ocupación de los espacios, reduciendo los tiempos muertos y optimizar los ingresos.

Por consiguiente, el sistema modela cada **Evento** como un compromiso contractual con un cliente (con atributos de fecha, hora y duración), y cada **Recurso** como un activo tangible del hotel. El software impide asignaciones que vulneren la disponibilidad de los recursos.

---

## 3. Diseño del sistema y justificación de decisiones técnicas

El desarrollo se estructuró siguiendo con especial énfasis en la claridad, escalabilidad y mantenibilidad del código.

### 3.1. Estructura del proyecto

```text
Proyecto/
├── core/
│ ├── _init_.py
│ ├── resources.py
│ ├── events.py
│ └── planification.py
├── UI/
│ └── menus/
│   ├── event_creation.py
│   ├── see_inventory.py
│   └── see_schedule.py
├── data/
│ ├── Events.json
│ └── Inventory.json
└── main.py
```

### 3.2. Paradigma de programación orientada a objetos (POO)

Se optó por el paradigma orientado a objetos para representar las entidades del dominio.

- **Clase `Resource`:** Encapsula los atributos identificativos de un activo hotelero (`nombre`, `cantidad total`,`disponibilidad`). Además de que contiene los atributos `conflictos`y `dependencias`, que se encargan de difinir las reglas del dominio.
- **Clase `Event`:** Contiene los atributos propios de una reserva (`tipo`, `inicio` y `fin` como objetos `datetime`), un diccionario con los recursos asignados al evento como llaves y con las cantidades como valores (`recursos necesarios`), y un campo de `descripción` opcional para diferenciar de otros eventos de la misma categoría (`tipo`)
- **Clase `Planification`:** Actúa como el núcleo operativo del sistema. Gestiona la lista de todos los eventos agendados (`self.events`) y alberga los métodos de negocio para la creación, eliminación, asignación y verificación.

La justificación se basa en el principio de responsabilidad única; cualquier modificación futura en la estructura de un evento, por ejemplo, la adición del campo "presupuesto", se ajusta a la clase `Event`, sin afectar a la lógica de asignación de recursos.

### 3.3. Estructuras de Datos: diccionarios y listas

Se optó por mantener una lista **(self.events)** ordenada por fecha de inicio (beginning). Esto simplifica drásticamente la visualización secuencial de los eventos planificados y optimiza los algoritmos de verificación de disponibilidad **(resource_availability)**, permitiendo romper los bucles de búsqueda de forma temprana, tan pronto como se supera la ventana temporal evaluada.

El acceso al inventario global de recursos de la sesión se realiza mediante un diccionario indexado por nombre.

### 3.4. Gestión temporal mediante el Módulo `datetime`

Inicialmente se pensó en el uso de cadenas de texto para representar fechas; sin embargo, se implementó el módulo `datetime` por sus ventajas. Este módulo permite el cálculo exacto de la finalización de un evento (`inicio + timedelta(hours=duracion)`) y la comparación directa de franjas horarias mediante operadores relacionales. En el ámbito hotelero, donde los horarios de montaje y desmontaje son estrictos, la precisión temporal es un requisito obligatorio.

### 3.5. Mecanismo de persistencia: serialización con JSON

Se implementó la persistencia de datos mediante el formato JSON, en lugar de un sistema de gestión de bases de datos, para simplificar la arquitectura del primer prototipo. El formato JSON nativo no serializa objetos `datetime`. Para resolver esta limitación, se desarrolló **un encoder y decoder personalizados**. Los objetos `datetime` se convierten a cadenas ISO-8601 durante el volcado y se reconstruyen como objetos temporales al cargar el archivo `Events.json`. Este enfoque asegura que el coordinador pueda interrumpir y reanudar la sesión sin pérdida de información.

### 3.6. Interfaz de Usuario: Aplicación web interactiva con Streamlit

Se decidió implementar una interfaz web interactiva empleando el framework Streamlit, en lugar de la consola. Esta elección obedece a tres razones principales. En primer lugar, el perfil del usuario final (coordinadores de eventos y personal hotelero) que no está familiarizado con entornos de terminal. En segundo lugar, Streamlit ofrece widgets nativos de entrada de fechas, horas y números que incorporan validaciones automáticas, eliminando la necesidad de escribir bucles de limpieza y previniendo errores de tecleo. En tercer lugar, Streamlit permite iterar y depurar visualmente el código en tiempo real, acelerando el tiempo de desarrollo. Además, el uso de Streamlit fue recomendado por los profesores de la asignatura por su relativa sencillez y rápida curva de aprendizaje. La aplicación puede desplegarse en un servidor local y es accesible desde múltiples dispositivos, lo que facilita la colaboración entre distintos departamentos del hotel.

---

## 4. Aprendizajes

Se pueden resumir un conjunto de lecciones aprendidas durante el proceso:

- Se ha interiorizado la necesidad de validar rigurosamente los formatos de entrada de fechas y horas. Es cierto que Streamlit facilita la captura, sin embargo, la comparación sigue siendo crítica en las operaciones temporales.

- La implementación del algoritmo de verificación de solapamientos (`inicio1 < fin2 and inicio2 < fin1`) constituye una aplicación directa de la teoría de conjuntos a intervalos.

- La versión inicial del prototipo almacenaba los datos en archivos de texto planos, lo que dificultaba la extensión de los atributos. **Es importante una planificación adelantada de la estructura de datos para evitar el costo elevado de refactorización en fases posteriores.**

- La habilidad para interpretar los mensajes de excepción de Python ha mejorado. La capacidad de rastrear el origen del error acelera el proceso de depuración.

- Se debe prestar especial atención a los mensajes del sistema.

---

## 5. Guía de uso (Casos de Ejemplo)

**El sistema se ejecuta como una aplicación web. Para iniciarla, el usuario debe situarse en el directorio del proyecto y ejecutar en la terminal el comando `streamlit run main.py`. Automáticamente se abrirá una pestaña en el navegador predeterminado con la interfaz de ÁGORA.** A continuación, se ilustra un flujo de trabajo típico en un contexto hotelero.

### 5.1. Gestión de recursos físicos presentes en el inventario

En la sección "Gestionar Inventario" del panel lateral se halla una visualización de cada recurso junto con su respectiva cantidad total, además de presentar los botones "Disminuir cantidad" y "Aumentar cantidad" para modificar tales cantidades.

- Al presionar **Disminuir cantidad**, se le presenta al usuario un cajón de selección de activos con la cantidad que pretende restar del inventario. Tras realizarse clic en el botón "Confirmar", el sistema comprueba que la operación que se está llevando a cabo no producirá conflictos en la planificación de eventos En caso de haber conflicros, no se descontará ninguna cantidad del recurso en cuestión del inventario y se informará de los eventos que se vean afectados, recomendando que se modificada la planificación

- Al presionar **Aumentar cantidad**, se muestra un cajón de selección con gran parecido al descrito anteriormente, excepto que no habrá problemáticas que el programa necesite considerar.

### 5.2. Crear evento

Para el proceso de crear un evento, se le presenta al gestor una interfaz de un formulario para rellenar los datos siguientes:

- **Tipo de evento:** _Boda_
- **Descripción del evento:** _Boda de Juan y Josefa_
- **Fechas y horas de inicio y fin del evento:** el usuario elige mediante un selector de fecha y hora (widget de Streamlit), por ejemplo, _2026-07-20_, _18:00_.

**Al pulsar Crear Evento, la aplicación añade el evento a la lista y lo muestra en la sección "Eventos planificados".**

### 5.3. Asignación de recursos y validación de conflictos

En el mismo menú, el coordinador selecciona un evento y los recursos con la cantidad correspondiente que desea incorporar al evento. Si se omite la búsqueda automática de horarios, el programa tras la introducción de las fechas y horas de inicio y finalización,verifica automáticamente la disponibilidad del recurso en esa franja horaria. Si se dispone de la cantidad requerida, la asignación se completa y se actualiza la vista. En caso contrario, se muestra un mensaje de error como el siguiente:

> "No puede registrar el evento por falta de disponibilidad en las fechas seleccionadas. Ajuste las fechas o use el asistente."

### 5.4. Consulta de la programación de eventos del hotel

El coordinador puede visualizar la planificación completa en la sección "Eventos Planificados". Allí se listan todos los eventos con sus horarios y los recursos asignados a cada uno. Esta vista se actualiza dinámicamente tras cada operación, permitiendo tomar decisiones sobre nuevas solicitudes.

---

## 6. Dificultades técnicas encontradas y soluciones

Durante la programación se identificaron varias dificultades técnicas. La mayoría afectaban la lógica de negocio, independientemente de la interfaz utilizada. El uso de Streamlit también tuvo algunos desafíos específicos.

### 6.1. Verificación de solapamiento de intervalos

La primera aproximación para comprobar la disponibilidad consistía en verificar únicamente si la fecha de inicio del nuevo evento se encontraba dentro del rango del evento existente. Sin embargo, esta lógica fallaba cuando el nuevo evento contenía completamente al evento existente (inicio anterior y fin posterior). Para solucionarlo se implementó una función de intersección de intervalos.

---

### 6.2. Gestión del estado en Streamlit

Streamlit redibuja toda la página en cada interacción, lo que provoca que las variables no persistentes se reinicien. Inicialmente, los datos se perdían al añadir un recurso o evento. Para resolverlo se almacenaron los diccionarios de eventos y recursos en `st.session_state`. De esta forma, las modificaciones persisten entre recargas de la interfaz, garantizando la consistencia de la sesión.

## 6.3. Objetos datetime en formato JSON

**Problema:** El módulo `json` no admite la serialización directa de objetos `datetime`, lanzando la excepción `TypeError: Object of type datetime is not JSON serializable`.

Para la deserialización, se implementó un proceso inverso que itera sobre la estructura de datos cargada y convierte las cadenas ISO en objetos `datetime` mediante `datetime.fromisoformat()` antes de reconstruir las instancias de la clase `Evento`.

## 6.4. Mantenimiento de la integridad cuando se le daba baja a recursos en el inventario

La reducción de las cantidades de un recurso que se encontraba asignado a uno o varios eventos dejaba referencias a recursos inexistentes en las listas de asignación de los eventos, corrompiendo la integridad de la agenda. Para solucionarlo se implementó un mecanismo de verificación previa a la eliminación:

1. El sistema consulta si el recurso está presente en algún evento.
2. En caso afirmativo, tras un temporal decrecimiento, se vuelve a comprobar que las cantidades disponibles del recurso durante los eventos, no sean menores que las cantidades requeridas para la realización de tales actividades.
3. Si existen eventos que presenten problemas en el punto anterior, se le notifica al usuario de ellos y se le recomienda que atienda los conflictos en la agenda, sin realizar la disminución en el inventario. De lo contrario, se procede normalmente con la reducción y el sistema muestra un mensaje de éxito

De esta forma se garantiza que la agenda se mantenga consistente y libre de referencias inválidas.

## 6.5. Adaptación de la interfaz a las validaciones de fechas

Como Streamlit proporciona widgets para la selección de fechas y horas (objetos `datetime`), propició mayor comodidad para:

- Forzar que el input del usuario tenga un formato correcto de fecha y hora
- Establecer la comprobacion de que la hora de inicio sea posterior al momento actual, con el fin de impedir reservas en el pasado.
- Recibir como valores por defecto las fechas sugeridas por `find_space()`, en caso de haber acudido al _Asistente de Disponibilidad_.

## 7. Conclusiones

El proyecto ha proporcionado un sistema funcional para la planificación de eventos en el sector hotelero. El desarrollo ha permitido consolidar conocimientos en programación orientada a objetos, manejo de estructuras de datos, gestión temporal y persistencia de información. La capacidad del sistema para detectar y prevenir conflictos de agenda de manera eficiente constituye su valor más significativo.
