# AtlasNode G7 - Solución de problemas

Esta guía reúne los problemas más frecuentes del AtlasNode G7 y cómo resolverlos.

## Significado del LED de estado

- **Verde fijo:** funcionamiento normal.
- **Naranja parpadeante:** el equipo está arrancando o actualizando el firmware.
- **Rojo fijo:** fallo grave de hardware. Contacte con soporte técnico.
- **Rojo parpadeante:** restablecimiento de fábrica en curso.
- **Azul parpadeante:** el túnel VPN WireGuard está intentando conectarse.
- **Apagado:** sin alimentación. Revise el cableado y el fusible.

## No puedo acceder a la interfaz web

Primero compruebe que el ordenador está conectado al puerto LAN1 y no a LAN2, porque en la configuración de fábrica solo LAN1 responde. Verifique que su IP está en el rango 192.168.50.x. Si cambió la dirección IP y la olvidó, realice un restablecimiento de fábrica por hardware manteniendo pulsado el botón RESET durante 10 segundos. Si el navegador no abre la página, asegúrese de usar https y no http.

## El equipo se reinicia solo

Los reinicios inesperados suelen deberse a una alimentación inestable. Mida la tensión en el conector: debe estar entre 12 V y 48 V DC. Si utiliza una sola fuente, considere conectar una segunda en PWR2 para redundancia. Revise también el registro de eventos en Sistema > Registros, donde se anota la causa del último reinicio, por ejemplo un fallo del temporizador de vigilancia (watchdog) o un corte de energía.

## Los dispositivos Modbus no responden

Compruebe estos puntos en orden:

1. Que la velocidad, la paridad y los bits de parada configurados en el G7 coincidan con los del dispositivo. La velocidad predeterminada es 9600 baudios, paridad ninguna y 1 bit de parada.
2. Que la polaridad de los cables A y B del RS-485 sea correcta; si están invertidos, no hay comunicación.
3. Que cada dispositivo tenga una dirección Modbus única entre 1 y 247.
4. Que el último dispositivo de la línea tenga una resistencia de terminación de 120 ohmios.

Si la línea supera los 1200 metros o tiene más de 32 dispositivos, la comunicación será inestable y debe dividirse en segmentos.

## Los mensajes MQTT no llegan al broker

Verifique en Red > Interfaces que LAN2 tiene salida hacia el broker y que el firewall permite el puerto correspondiente, normalmente el 1883, o el 8883 si se usa TLS. Revise el usuario y la contraseña del broker en la configuración MQTT. El estado de la conexión aparece en el panel principal como Conectado o Desconectado. Si el equipo pierde la conexión, almacena hasta 10 000 mensajes en memoria y los envía al recuperarse.

## La actualización de firmware falla

Si aparece el error de suma de verificación, vuelva a descargar el archivo `.atlasfw` y compare de nuevo el SHA-256. Si la actualización se interrumpe, el G7 arranca desde la partición de respaldo con la versión anterior. Reintente la actualización con una alimentación estable.

## Contacto con soporte

Antes de contactar con soporte técnico, descargue el paquete de diagnóstico desde Sistema > Diagnóstico y tenga a mano el número de serie, impreso en la etiqueta lateral del equipo.
