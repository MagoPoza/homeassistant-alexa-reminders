# Recordatorios alexa al calendario local de homeassistant
Esta guía sirve para agregar automáticamente los recordatorios que creamos en Alexa desde nuestros dispositivos (excepto en la aplicación móvil) al calendario de Home Assistant como eventos. Los añade a un calendario u otro en función de la persona que los ha creado.
# Requisitos previos
Para ello es necesario tener la integración de alexa_media_player instalada en homeassistant: https://github.com/alandtse/alexa_media_player
# Configuración
Lo primero que debemos hacer es agregar estos 3 comandos Shell a nuestro archivo configuration.yaml:
```
shell_command:
  alexa_reminders_new: >
    bash -c "echo '{{ message | replace('\"', '\\\"') }}' > /config/www/recordatorios/alexa_reminders_new.json"
  alexa_reminders_old: >
    bash -c "cp /config/www/recordatorios/alexa_reminders_new.json /config/www/recordatorios/alexa_reminders_old.json"
  compare_reminders: "python3 /config/scripts/compare_reminders.py"
```
Después debemos crear en nuestro directorio de configuración la carpeta scripts y en /config/www la carpeta recordatorios. Quedarían ambas rutas así:

/config/scripts

/config/www/recordatorios

Dentro de la carpeta scripts pegamos el archivo compare_reminders.py

Lo siguiente será detectar el ID de cada persona que vaya a crear recordatorios, para ello vamos a herramientas de desarrolladores/plantillas y pegamos esto:
```
{{ (state_attr('sensor.echo_show_salon_next_reminder', 'sorted_active') | from_json)[0][1]['personProfile']['personId'] }}
```

Sustituyendo 'sensor.echo_show_salon_next_reminder' por el sensor de nuestro dispositivo, si tenemos algún recordatorio creado debería devolver algo como: amzn1.account.ABCDEFGHIJKLMN. 

Ese será el ID de la persona que ha creado el próximo recordatorio en ese dispositivo. OJO no es el último recordatorio creado sino el próximo que nos va a notificar.

Ahora debemos elegir que blueprint tenemos que utilizar en función de las personas que vayamos a agregar. Si vamos a agregar una persona con su ID y calendario elegiremos el blueprint `recordatorios_alexa_1p.yaml`, si vamos a agregar dos personas `recordatorios_alexa_1p.yaml`, etc.

Es importante elegir el blueprint con el número exacto de personas que vamos a agregar (nombre, ID y calendario), ya que todos los campos son obligatorios de rellenar. Si no queremos añadir ninguna persona y que todos los recordatorios vayan a un calendario principal podemos elegir el modelo genérico `recordatorios_alexa_generico.yaml`.

En homeassistant en la sección de plantillas pulsamos en importar plantilla y pegamos la URL del blueprint que hemos elegido como por ejemplo el de dos personas: https://github.com/MagoPoza/homeassistant-alexa-reminders/blob/main/blueprints/recordatorios_alexa_2p.yaml

Por último creamos una automatización a partir de ese blueprint y lo rellenamos con nuestros datos.

Ahora ya podemos pedir a alexa que nos recuerde algo y veremos un nuevo evento en nuestro calendario de homeassistant.
