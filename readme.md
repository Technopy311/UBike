# Protocolo funcionamiento Módulo de estacionamiento de bicicletas (Trabajo en proceso)

## Componentes

El módulo consistira de los siguentes componentes: 
- Microcontrolador Raspberry Pi Pico W
- Lector RFID compatible con microcontroladores
- Buzzer activo
- Led RGB
- Sistema de seguridad primaria
- Relé
- Pestillo solenoide


Nota: por el momento, todo el software del proyecto será desarrollado en Python, usando librerias externas como Django

### Metodo de funcionamiento:
- Se dispondrá de una serie de modulos, cada uno propio de un estacionamiento
- Todos los modulos se contectarán a un servidor local en común, el cual será el encargado de gestionar la autenticación, otorgar permisos, registrar, entre otros
- La autenticación será realizada por medio del UID de cada tarjeta/llavero, se considera el uso de una clave de autenticación o cifrado de la misma por motivos de seguridad
- Una vez realizada la autenticación, y la confirmación por parte de el servidor, el solenoide se contrae durante un periodo de tiempo, permitiendo así tener acceso al estacionamiento o bicicleta
- Es necesario realizar autenticación al llegar y al irse con la bicicleta, por motivos de registro, seguridad y posible catastro
- El LED indicará por medio de 6 colores el estado del estacionamiento o dispositivo en caso de algun inconveniente, por medio de un codigo de color

### Sistema de seguridad primaria
Cada modulo vendra equipado con un sistema de seguridad, que se activará en posibles casos como por ejemplo:
- Manipulación indebida del módulo
- Corte de energia
- Intento de robo

Bajo estos eventos, se activará el modo de seguridad, que impide el desbloqueo de la cerradura solenoide a toda costa, a menos que un encargado designado solucione el conflicto