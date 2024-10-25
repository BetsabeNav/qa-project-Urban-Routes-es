**Proyecto Urban Routes
Betsabé Navarro Loyo. Grupo 14. Sprint8**

**Descripción del Proyecto**
Urban Routes es una aplicación que permite solicitar un taxi en línea, con opciones para seleccionar 
diferentes tarifas y servicios adicionales. 
Este proyecto tiene como objetivo probar de manera automatizada el flujo completo de pedir un taxi,
desde la configuración de la dirección hasta la asignación del conductor.

El objetivo de estas pruebas es asegurar que el proceso de solicitud de taxi funcione correctamente,
incluyendo la selección de tarifas, el ingreso de datos de contacto y pago, y la confirmación de la 
reserva del taxi.

**Fuente de información**
https://cnt-c2927419-35cd-4479-8608-2d1bc5c5d984.containerhub.tripleten-services.com?lng=es

**Tecnologías Utilizadas**
* Python
* pytest
* Selenium
* WebDriver

**Ejecución de Pruebas**
* Para ejecutar las pruebas, asegúrate de tener instalados los paquetes pytest y Selenium. 
   - pip install pytest
   - pip install selenium
* Las pruebas utilizarán el navegador Chrome, así que asegúrate de tenerlo instalado.
  (Puedes ajustar las configuraciones del navegador en el método setup_class de la clase TestUrbanRoutes.)
* Para ejecutar las Pruebas Asegúrate de estar en el directorio "main.py", donde se encuentran las pruebas.
Luego, ejecuta las pruebas utilizando pytest
* Al finalizar las pruebas, pytest mostrará un resumen de los resultados en la terminal.

Asegúrate de que tu entorno de prueba esté correctamente configurado y de que las direcciones, números de teléfono 
y datos de tarjeta sean válidos.
Considera utilizar un entorno virtual para evitar conflictos de dependencias.
Con estas instrucciones, deberías poder ejecutar tus pruebas de manera efectiva. Si tienes más preguntas o necesitas 
más ayuda, ¡no dudes en preguntar!

Ruta de archivo: Users/betsabenavarro/Desktop/Proyectos/qa-project-Urban-Routes-es


**Funcionalidad de las Pruebas**
Las pruebas automatizadas cubren los siguientes pasos del flujo de solicitud de un taxi:

1. Configurar la dirección: Se simula la configuración de la dirección de origen del viaje (esta parte ya está 
implementada).
2. Seleccionar la tarifa Comfort.
3. Rellenar el número de teléfono.
4. Agregar una tarjeta de crédito: Se simula la interacción con el modal de "Agregar una tarjeta" y se asegura que el 
campo CVV (id="code" class="card-input") pierda el enfoque para habilitar el botón de enlace.
5. Escribir un mensaje para el conductor.
6. Solicitar una manta y pañuelos.
7. Pedir 2 helados.
8. Esperar la búsqueda de un taxi: Se asegura que el modal de búsqueda de conductor aparezca correctamente y que la 
cuenta regresiva se inicie.
