# Proyectos
Automatiza la captura y análisis de datos desde Excel en OneDrive usando Power Automate y Python en Raspberry Pi. Integra inteligencia artificial para generar reportes con análisis, referencias y visualizaciones, además de enlazar datos con Google Drive y Power BI. Enfocado en prototipado local, control de costos y escalabilidad.

Este proyecto busca automatizar el flujo de datos desde fuentes de Excel alojadas en OneDrive, facilitando la captura, análisis y gestión de registros nuevos mediante una integración entre Power Automate, Python y una Raspberry Pi. La solución incluye además una capa de inteligencia artificial para enriquecer las alertas y reportes generados, aportando análisis detallados, referencias y visualizaciones que facilitan la toma de decisiones.

Componentes Principales:

Power Automate: Ejecuta flujos periódicos para extraer datos nuevos de tablas Excel en OneDrive, generando archivos CSV con registros recientes y enviándolos automáticamente por correo electrónico a una cuenta Gmail específica.

Python en Raspberry Pi: Programa un script que se ejecuta periódicamente (usando cron), conecta vía IMAP a la cuenta de correo para descargar los archivos CSV, y analiza los datos con pandas. Si se detectan condiciones que superan ciertos umbrales, el sistema envía alertas automatizadas vía email a responsables humanos.

Inteligencia Artificial (OpenAI u otros modelos): Cuando se detectan alertas, se llama a un servidor externo vía API REST que utiliza IA para generar reportes HTML detallados, que incluyen análisis de la problemática, recomendaciones, enlaces a fuentes originales y referencias para validación. Estos reportes son accesibles desde una página web dedicada para revisión humana.

Integración con APIs externas:

Google Drive API para acceder a documentación y datos relevantes, que enriquecen el contexto del análisis.

APIs de búsqueda web para obtener información actualizada en tiempo real y mejorar la calidad del contenido generado.

Power BI para incluir enlaces a dashboards y visualizaciones oficiales que complementan los reportes generados.

Beneficios y Enfoque:

Reduce el trabajo manual y el error humano en el procesamiento de grandes volúmenes de datos.

Proporciona análisis automatizados con soporte documental y contextual, facilitando decisiones informadas.

Permite prototipar localmente con herramientas gratuitas o de bajo costo, como Flask para backend y Raspberry Pi para ejecución de scripts.

Controla y optimiza el uso de servicios de IA mediante gestión de llamadas y aprovechamiento de créditos gratuitos iniciales.

Aborda aspectos de seguridad y privacidad, controlando los datos sensibles enviados a servicios externos.

Próximos Pasos:

Desarrollo de la API REST para integración completa con el backend y la IA.

Creación y mejora de plantillas HTML para reportes uniformes y fácilmente revisables.

Implementación de validación humana semiautomática para supervisar resultados generados por IA.

Optimización del flujo de trabajo para garantizar robustez y escalabilidad.
