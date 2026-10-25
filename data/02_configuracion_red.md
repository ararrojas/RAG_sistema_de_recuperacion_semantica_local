# AtlasNode G7 - Configuración de red

Este documento explica cómo acceder a la interfaz de administración del AtlasNode G7 y configurar su red.

## Acceso inicial

De fábrica, el puerto LAN1 tiene la dirección IP estática 192.168.50.1 con máscara 255.255.255.0. Para acceder, conecte un ordenador directamente a LAN1 y asígnele una IP del mismo rango, por ejemplo 192.168.50.10. Abra un navegador y entre a https://192.168.50.1. El certificado es autofirmado, por lo que el navegador mostrará una advertencia que debe aceptar.

Las credenciales de fábrica son usuario `admin` y contraseña `atlas-1234`. El sistema obliga a cambiar la contraseña en el primer inicio de sesión. La nueva contraseña debe tener al menos 12 caracteres e incluir una mayúscula, un número y un símbolo.

## Configuración de direcciones IP

En el menú Red > Interfaces puede elegir entre IP estática o DHCP para LAN1 y LAN2. Las dos interfaces deben estar en subredes distintas; el sistema rechaza la configuración si coinciden. Se recomienda mantener LAN1 como red de gestión y usar LAN2 para el tráfico de datos de los sensores.

## Servidor DHCP interno

El G7 puede actuar como servidor DHCP en LAN2. El rango predeterminado es de 192.168.60.100 a 192.168.60.200, con un tiempo de concesión de 24 horas. Este servicio está desactivado de fábrica y debe habilitarse en Red > DHCP.

## Protocolos industriales soportados

El equipo traduce entre varios protocolos: Modbus RTU (por RS-485), Modbus TCP, MQTT versión 3.1.1 y 5.0, y OPC UA en modo servidor. La conversión de Modbus RTU a MQTT es la función más utilizada: el G7 lee los registros de los dispositivos serie y los publica como mensajes en un broker MQTT configurable. El intervalo mínimo de sondeo es de 100 milisegundos.

## Firewall

El firewall integrado viene activo con una política de denegación por defecto en LAN2. En LAN1 solo se permiten los puertos 443 (administración web) y 22 (SSH). El acceso por SSH está deshabilitado de fábrica y se activa en Sistema > Servicios. Cada regla del firewall admite filtrar por IP de origen, puerto y protocolo, y se pueden crear hasta 256 reglas.

## Conexión VPN

El AtlasNode G7 incluye un cliente WireGuard para conectarse de forma segura a la oficina central. Para configurarlo, cargue el archivo de configuración `.conf` en Red > VPN. El túnel se reconecta automáticamente si se pierde la conexión, con reintentos cada 30 segundos.

## Guardar y aplicar cambios

Los cambios de red no se aplican hasta pulsar el botón Aplicar. Si tras aplicar la nueva configuración no se puede acceder al equipo, el G7 revierte automáticamente a la configuración anterior pasados 120 segundos, siempre que no se confirme el cambio. Esta función evita perder el acceso por un error de configuración.
