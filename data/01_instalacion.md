# AtlasNode G7 - Guía de instalación

El AtlasNode G7 es un gateway industrial de la empresa ficticia Meridian Systems, diseñado para conectar sensores y PLCs a una red corporativa. Este documento describe la instalación física del equipo.

## Contenido de la caja

La caja incluye: el gateway AtlasNode G7, un riel DIN de 35 mm con su clip de montaje, un conector de alimentación de cuatro pines, un cable Ethernet CAT6 de 1,5 metros y una guía rápida impresa. No se incluye fuente de alimentación; debe adquirirse por separado.

## Requisitos ambientales

El AtlasNode G7 opera con temperaturas ambientales entre -20 °C y 60 °C. La humedad relativa admitida va del 5 % al 95 % sin condensación. El equipo tiene una clasificación de protección IP30, por lo que debe instalarse dentro de un armario eléctrico y nunca a la intemperie. Debe dejarse un espacio libre mínimo de 5 cm por encima y por debajo del equipo para permitir la ventilación pasiva, ya que el G7 no tiene ventiladores.

## Alimentación eléctrica

El equipo acepta una tensión continua de entrada de 12 V a 48 V DC. El consumo típico es de 8 W y el máximo, bajo carga completa, es de 15 W. El conector de alimentación de cuatro pines admite dos entradas redundantes, identificadas como PWR1 y PWR2. Si se conectan ambas fuentes, el equipo conmuta automáticamente a la secundaria cuando falla la principal, sin reiniciarse. Se recomienda usar un fusible de 2 A en cada línea de alimentación.

## Montaje en riel DIN

1. Fije el clip de montaje en la parte trasera del equipo con los dos tornillos incluidos.
2. Enganche la parte superior del clip en el riel DIN.
3. Empuje el equipo hacia abajo y hacia el riel hasta escuchar un clic.
4. Compruebe tirando suavemente que el equipo queda firme.

Para desmontarlo, utilice un destornillador plano para tirar de la lengüeta inferior del clip y levante el equipo.

## Puertos físicos

El G7 dispone de dos puertos Ethernet Gigabit, etiquetados LAN1 y LAN2, un puerto serie RS-485 y un puerto USB-C reservado para servicio técnico. El puerto LAN1 es el de gestión: en la primera puesta en marcha, el equipo responde únicamente por este puerto. El puerto RS-485 permite conectar hasta 32 dispositivos Modbus RTU en una misma línea, con una longitud máxima de cable de 1200 metros.

## Primera puesta en marcha

Tras conectar la alimentación, el LED de estado parpadea en color naranja durante unos 45 segundos mientras el sistema arranca. Cuando el LED queda fijo en verde, el equipo está listo para ser configurado. Continúe con la guía de configuración de red.
