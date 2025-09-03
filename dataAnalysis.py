import imaplib
import email
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CONFIGURACIÓN
EMAIL_EMISOR = "victoralejandromc010@gmail.com"
EMAIL_RECEPTOR = "victor_alejandromc@hotmail.com"
CONTRASENA_APP = "cwbq tgez jxnm jpdi"  # Contraseña de aplicación de Gmail

RUTA_CSV = "data.csv"
UMBRAL_ALERTA = 2  # Cambia según el umbral deseado
URL_PAGINA = "http://127.0.0.1:5500/index.html#"
ASUNTO_BUSQUEDA = "Alerta de Clientes Raspberry"

def descargar_csv_desde_correo():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_EMISOR, CONTRASENA_APP)
        mail.select("inbox")

        # Buscar correos con el asunto deseado
        result, data = mail.search(None, f'(SUBJECT "{ASUNTO_BUSQUEDA}")')
        ids = data[0].split()
        if not ids:
            print("No se encontró ningún correo con el asunto esperado.")
            return False

        # Tomar el último correo recibido
        ultimo_id = ids[-1]
        result, msg_data = mail.fetch(ultimo_id, "(RFC822)")

        raw_email = msg_data[0][1]
        mensaje = email.message_from_bytes(raw_email)

        # Buscar y guardar el archivo CSV adjunto
        for parte in mensaje.walk():
            if parte.get_content_maintype() == 'multipart':
                continue
            if parte.get('Content-Disposition') is None:
                continue

            nombre_archivo = parte.get_filename()
            if nombre_archivo and nombre_archivo.endswith(".csv"):
                with open(RUTA_CSV, 'wb') as f:
                    f.write(parte.get_payload(decode=True))
                print(f"Archivo CSV descargado: {nombre_archivo}")
                return True

        print("No se encontró ningún archivo CSV adjunto.")
        return False

    except Exception as e:
        print(f"Error al leer el correo: {e}")
        return False

def enviar_correo(mensaje_texto, mensaje_html):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_EMISOR
        msg['To'] = EMAIL_RECEPTOR
        msg['Subject'] = "🚨 Alerta de Clientes por Nombre - Sistema Raspberry"

        part1 = MIMEText(mensaje_texto, 'plain')
        part2 = MIMEText(mensaje_html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(EMAIL_EMISOR, CONTRASENA_APP)
        servidor.send_message(msg)
        servidor.quit()

        print("Correo de alerta enviado.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# MAIN
if descargar_csv_desde_correo():
    try:
        df = pd.read_csv(RUTA_CSV)
        df['Nombre'] = df['Nombre'].fillna('Desconocido').astype(str).str.strip().str.title()
        clientes_por_nombre = df['Nombre'].value_counts()

        alertas = clientes_por_nombre[clientes_por_nombre > UMBRAL_ALERTA]

        if not alertas.empty:
            mensaje_alerta_texto = ""
            mensaje_alerta_html = "<html><body>"

            for nombre, cantidad in alertas.items():
                linea_texto = f"Alerta: El nombre '{nombre}' aparece {cantidad} veces, supera el umbral de {UMBRAL_ALERTA}.\n"
                linea_html = f"<p>Alerta: El nombre <strong>{nombre}</strong> aparece <strong>{cantidad}</strong> veces.</p>"

                mensaje_alerta_texto += linea_texto
                mensaje_alerta_html += linea_html

            mensaje_alerta_texto += f"\nConsulta el análisis completo aquí: {URL_PAGINA}"
            mensaje_alerta_html += f'<p>Consulta el análisis completo <a href="{URL_PAGINA}">aquí</a>.</p>'
            mensaje_alerta_html += "</body></html>"

            enviar_correo(mensaje_alerta_texto, mensaje_alerta_html)
        else:
            print("No hay alertas. Ningún nombre supera el umbral.")

    except Exception as e:
        print(f"Ocurrió un error al procesar el CSV: {e}")
    finally:
        # Eliminar el archivo después del análisis
        if os.path.exists(RUTA_CSV):
            os.remove(RUTA_CSV)
            print("Archivo CSV eliminado después del análisis.")
else:
    print("No se pudo continuar con el análisis por falta del archivo CSV.")
