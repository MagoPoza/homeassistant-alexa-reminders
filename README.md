# Homeassistant-alexa-reminders
Siguiendo esta guía conseguimos que los recordatorios que creamos en Alexa desde nuestros dispositivos (excepto en la aplicación móvil) pasen automáticamente al calendario de Home Assistant como eventos asignándolos a un calendario u otro en función de la persona que los ha creado.
# REQUISITOS PREVIOS
Para ello es necesario tener la integración de alexa_media_player instalada en homeassistant: https://github.com/alandtse/alexa_media_player
# CONFIGURACIÓN
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

Ahora en homeassistant agregamos uno de los blueprints de este repositorio en función de las personas que queramos añadir. Si no queremos añadir ninguna persona y que todos los recordatorios vayan a un calendario principal podemos elegir el modelo genérico nombrado como recordatorios_alexa_generico.yaml
Es importante elegir el blueprint con el número de personas que vamos a agregar nombre, ID y calendario ya que todos los campos son obligatorios de rellenar.
