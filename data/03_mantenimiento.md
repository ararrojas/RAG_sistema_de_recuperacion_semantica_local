# AtlasNode G7 - Mantenimiento

Este documento describe las tareas de mantenimiento periódico del AtlasNode G7: actualizaciones de firmware, copias de seguridad y restablecimiento.

## Actualización de firmware

Meridian Systems publica actualizaciones de firmware aproximadamente cada tres meses. La versión instalada se consulta en Sistema > Información. Para actualizar:

1. Descargue el archivo `.atlasfw` desde el portal de soporte de Meridian Systems.
2. Verifique su suma SHA-256 con la publicada en el portal.
3. En Sistema > Firmware, pulse Subir y seleccione el archivo.
4. Espere a que termine la instalación. El equipo se reinicia solo y el proceso dura unos 4 minutos.

Durante la actualización no debe cortarse la alimentación, ya que podría dejar el equipo inutilizable. El G7 mantiene dos particiones de firmware: si la nueva versión no arranca correctamente tres veces seguidas, el sistema vuelve automáticamente a la versión anterior.

## Copias de seguridad de la configuración

Desde Sistema > Copia de seguridad se puede exportar la configuración completa en un archivo `.atlascfg` cifrado con una contraseña elegida por el usuario. Se recomienda hacer una copia antes de cada actualización de firmware y después de cualquier cambio importante. Para restaurarla, se sube el archivo en la misma pantalla y se introduce la contraseña. Una configuración exportada desde una versión de firmware nueva no puede restaurarse en una versión anterior.

## Restablecimiento de fábrica

Existen dos maneras de restablecer el equipo a su estado de fábrica:

- **Por software:** en Sistema > Restablecer, seleccione Restablecimiento de fábrica y confirme.
- **Por hardware:** con el equipo encendido, mantenga pulsado el botón RESET, ubicado en un orificio junto al puerto USB-C, durante 10 segundos con un clip o herramienta fina. El LED parpadeará en rojo y el equipo se reiniciará.

El restablecimiento borra todas las configuraciones, certificados y claves, y restaura la IP 192.168.50.1 y la contraseña de fábrica. Los registros de eventos también se eliminan.

## Registros y diagnóstico

El G7 guarda los registros de eventos en una memoria interna de 512 MB, con rotación automática cuando se llena. Pueden consultarse en Sistema > Registros o enviarse a un servidor syslog remoto. Para diagnóstico avanzado, la sección Sistema > Diagnóstico ofrece herramientas de ping, traceroute y captura de paquetes de hasta 60 segundos.

## Limpieza y revisión física

Cada seis meses se recomienda revisar que las rejillas de ventilación estén libres de polvo, limpiándolas con aire comprimido seco. Compruebe también que los conectores de alimentación y RS-485 estén bien apretados. No utilice disolventes ni líquidos sobre la carcasa.

## Garantía

El AtlasNode G7 cuenta con una garantía de 3 años desde la fecha de compra. La garantía no cubre daños por sobretensión fuera del rango de 12 V a 48 V DC ni por instalación a la intemperie.
