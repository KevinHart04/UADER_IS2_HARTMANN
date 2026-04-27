# Memoria de Desarrollo - TP Ingeniería de Software

## Avance 1: Implementación de Patrón Singleton (Calculadora de Factorial)

**Descripción:**
Se inició el desarrollo con la creación de un módulo en Python destinado al cálculo matemático (factoriales), estructurado bajo principios de diseño orientado a objetos y patrones creacionales.

**Acciones realizadas:**
* **Implementación del Patrón Singleton:** Se definió la clase `Factorial` controlando su instanciación mediante la sobrescritura del método mágico `__new__`. Esto asegura de forma estricta que solo exista una única instancia de la calculadora en memoria durante el ciclo de vida del programa.
* **Desarrollo del algoritmo de cálculo:** Se construyó el método `calcular_factorial(n)` utilizando una aproximación iterativa en lugar de recursiva.
* **Manejo de Excepciones:** Se incorporó validación de datos de entrada, levantando un `ValueError` preventivo en caso de recibir números negativos.
* **Prueba de concepto (Main):** Se estructuró el bloque de ejecución principal (`main`) para:
  1. Demostrar empíricamente la efectividad del Singleton verificando la identidad en memoria de dos variables distintas (`factorial_calculator1 is factorial_calculator2`).
  2. Implementar una interfaz CLI básica para la ingesta de datos del usuario y la demostración funcional del cálculo.
3. ## Avance 2: Expansión del Patrón Singleton (Calculadora de Impuestos)

## Avance 2: Expansión del Patrón Singleton (Calculadora de Impuestos)

**Descripción:**
Continuando con la arquitectura basada en patrones creacionales, se desarrolló un módulo de cálculo financiero destinado a procesar el precio final de productos o servicios, automatizando la aplicación de la carga tributaria correspondiente.

**Acciones realizadas:**
* **Refinamiento del Singleton:** Se construyó la clase `CalculadoraImpuestos` manteniendo la restricción de instancia única. En esta iteración, se robusteció la sobrescritura del método `__new__` incorporando `*args` y `**kwargs`, permitiendo una inicialización más segura y escalable si la clase muta en el futuro.
* **Modelado de Lógica de Negocio:** Se codificó el método `calcular_precio_final(precio_base)` que implementa la cascada impositiva estándar: IVA (21%), Ingresos Brutos (5%) y Tasas Municipales (1.2%).
* **Control de Excepciones:** Se blindó el flujo de ejecución principal con un bloque `try-except` orientado a capturar específicamente `ValueError`, evitando caídas del sistema ("crashes") ante ingresos de caracteres alfabéticos o nulos en el prompt de precios.
* **Formateo de Interfaz (CLI):** Se optimizó la presentación de los datos monetarios en la terminal, forzando la salida a dos decimales flotantes para cumplir con los estándares de visualización de divisas.
## Avance 3: Implementación de Patrón Factory (Gestión de Entregas)

**Descripción:**
Se escaló la arquitectura del sistema introduciendo el patrón de diseño Factory, con el objetivo de desacoplar y centralizar la lógica de selección de los diferentes métodos de entrega para los pedidos.

**Acciones realizadas:**
* **Modelado del Dominio:** Se estructuró la clase `FastFood` para encapsular la entidad base del pedido y definir sus comportamientos de entrega asociados (mostrador, retiro, delivery).
* **Despliegue del Patrón Factory:** Se implementó la clase creadora `DeliveryFactory` encargada de abstraer la lógica de decisión y devolver dinámicamente el comportamiento solicitado.
* **Optimización mediante *Dispatching*:** Se reemplazó la clásica estructura de control condicional (`if/elif`) por un diccionario de mapeo de métodos. Esto reduce drásticamente la complejidad ciclomática y facilita la incorporación de futuros métodos de entrega sin modificar la lógica central.
* **Aplicación de Decoradores:** Se utilizó `@staticmethod` en la función constructora, optimizando el uso de memoria al indicar que el método no necesita instanciar la clase Factory ni acceder a su estado interno para operar.
* **Validación Dinámica:** Se construyó un bloque de prueba en el `main` que itera sobre un array de opciones predefinidas, comprobando el correcto enrutamiento y la ejecución de los métodos de instancia retornados por el Factory.
## Avance 4: Patrón Factory con Herencia (Sistema de Facturación)

**Descripción:**
Se profundizó en los patrones creacionales combinando Factory con una jerarquía de herencia clásica. El objetivo fue modelar el dominio de facturación adaptado a las diferentes categorías impositivas de los clientes (Responsable Inscripto, No Inscripto, Exento).

**Acciones realizadas:**
* **Jerarquía de Clases y Polimorfismo:** Se definió una superclase `Invoice` que encapsula los atributos compartidos (importe y condición) y estandariza la salida mediante el método mágico `__str__`. A partir de ella, se extendieron las subclases `ResponsibleInvoice`, `NonRegisteredInvoice` y `ExemptInvoice` para setear el estado interno específico de cada condición.
* **Evolución del Patrón Factory:** Se implementó `InvoiceFactory` con el método estático `create_invoice`. A diferencia de la iteración anterior, este Factory utiliza un diccionario para almacenar referencias directas a las clases (no instancias ni métodos), instanciando y retornando el objeto correspondiente al vuelo.
* **Manejo Estricto de Errores:** Se añadió una validación explícita en el Factory que levanta un `ValueError` si se solicita una condición impositiva inexistente, protegiendo la integridad del sistema.
* **Interfaz de Usuario (CLI) Interactiva:** Se construyó un menú interactivo en la función `main` que captura la selección del usuario mediante un mapeo numérico de opciones, aislando la lógica de entrada de la lógica de negocio subyacente.
## Avance 5: Implementación de Patrón Builder (Línea de Ensamblaje Aeronáutica)

**Descripción:**
Se avanzó en la resolución de problemas de instanciación compleja mediante la aplicación del patrón Builder. Este enfoque permite construir objetos paso a paso y aislar el algoritmo de ensamblaje de las partes que componen el producto final, facilitando la creación de distintas variantes (ej. aviones comerciales vs. militares) bajo el mismo proceso.

**Acciones realizadas:**
* **Definición del Producto Complejo:** Se creó la clase `Airplane`, representando el objeto final compuesto por múltiples partes (fuselaje, turbinas, alas, tren de aterrizaje) y se sobrescribió su método `__str__` para una visualización clara del ensamblaje.
* **Abstracción del Constructor:** Se diseñó la clase base `AirplaneBuilder` que actúa como interfaz, estableciendo el contrato y los pasos secuenciales obligatorios (`build_body`, `build_turbines`, etc.) que cualquier constructor específico deberá respetar.
* **Implementación del Constructor Concreto:** Se codificó `CommercialAirplaneBuilder` heredando de la base. Esta clase contiene la lógica específica para ensamblar las características particulares de un avión de pasajeros, manipulando directamente el estado de su instancia de `Airplane`.
* **Orquestación mediante el Director:** Se introdujo la clase `Director`, cuya única responsabilidad es conocer el orden exacto del algoritmo de construcción. Al recibir un `builder` por inyección de dependencias en su constructor, ejecuta los métodos en la secuencia correcta sin necesidad de conocer los detalles internos de las piezas.
* **Ejecución Cliente (Main):** Se integraron todos los componentes en el flujo principal, instanciando el constructor concreto, pasándolo al director para ejecutar la secuencia de armado y finalmente extrayendo el producto terminado mediante `get_result()`.
## Avance 6: Implementación de Patrón Prototype (Clonación de Objetos)

**Descripción:**
Se abordó el problema de la creación repetitiva de instancias mediante el patrón Prototype. Este diseño permite delegar el proceso de instanciación al propio objeto, generando nuevos elementos a partir de la clonación de un "prototipo" preexistente, garantizando un estado base idéntico pero con total independencia en memoria.

**Acciones realizadas:**
* **Implementación de Clonación Profunda:** Se integró el módulo nativo `copy` de Python, utilizando la función `deepcopy()` dentro del método `clone()`. Esto asegura que los objetos mutables anidados (como la lista `data`) se dupliquen por completo en memoria, mitigando los riesgos asociados a las copias superficiales (*shallow copies*).
* **Definición de la Entidad Prototipo:** Se construyó la clase `Prototype`, equipada con la capacidad de auto-replicarse y con la sobrescritura del método `__str__` para exponer en consola tanto el estado de sus atributos como su identificador único de memoria (`id()`).
* **Validación de Independencia Mutacional:** En el flujo principal, se instanció un objeto original y se ejecutó una cascada de clonaciones (incluyendo la clonación de un clon). Se alteró el estado interno de las réplicas (modificando el atributo `name` y agregando elementos a `data`) para demostrar que el prototipo original permanece inmutable.
* **Comprobación Empírica de Identidad:** Se incluyeron verificaciones finales utilizando el operador de identidad `is`, confirmando técnicamente que los objetos resultantes no comparten referencias en memoria con sus predecesores.
## Avance 7: Implementación de Patrón Abstract Factory (E-commerce Multi-Región)

**Descripción:**
Se escaló la arquitectura de creación de objetos para soportar "familias" de productos relacionados o dependientes entre sí. Mediante el patrón Abstract Factory, el sistema de comercio electrónico puede alternar entre distintas configuraciones regionales (Argentina o Estados Unidos) garantizando la cohesión interna sin que el cliente conozca las clases concretas.

**Acciones realizadas:**
* **Definición de Interfaces de Productos:** Se crearon las clases base abstractas `Invoice`, `Currency` y `TaxCalculator`. Se utilizó el levantamiento de `NotImplementedError` en sus métodos para simular el comportamiento de interfaces formales, obligando a las subclases a definir su propia lógica.
* **Implementación de Productos Concretos:** Se desarrollaron dos ecosistemas de clases cerrados:
  1. *Variante Argentina:* `ArgentinaInvoice`, `PesoCurrency` ($) y `ArgentinaTaxCalculator` (IVA 21%).
  2. *Variante USA:* `USAInvoice`, `DollarCurrency` (USD) y `USATaxCalculator` (Tax 7%).
* **Creación de Fábricas (Abstracta y Concretas):** Se definió el contrato maestro en `EcommerceFactory` que dicta la creación obligatoria de factura, moneda e impuesto. Luego, se derivaron `ArgentinaFactory` y `USAFactory`, encargadas de instanciar y retornar exclusivamente los productos de su respectiva región.
* **Desacoplamiento del Cliente:** Se diseñó la clase `EcommerceSystem` para que dependa únicamente de las interfaces abstractas. Recibe una fábrica concreta por inyección en su constructor, asegurando que el proceso de *checkout* (cálculo de subtotales, impuestos y totales) opere de manera agnóstica a la región seleccionada.
* **Resolución en Tiempo de Ejecución (Main):** El script principal delega la decisión de qué fábrica instanciar al usuario mediante un prompt por terminal. Una vez inyectada la fábrica correspondiente en el sistema, la lógica de negocio fluye sin condicionales adicionales.