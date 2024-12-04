import os
#import locale
from models.tables import *
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import Request, HTTPException, status
from schemas.user import User
from starlette.responses import JSONResponse
from typing import Optional

#locale.setlocale(locale.LC_TIME, 'es_ES')
load_dotenv('.env')

smtp_password = os.getenv("SMTP_PASSWORD")
smpt_from = os.getenv("SMTP_FROM")

conf = ConnectionConfig(
    MAIL_USERNAME=smpt_from,
    MAIL_PASSWORD=smtp_password,
    MAIL_FROM=smpt_from,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="SIS",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

async def send_posture_recommendation_email(email: str, username: str, request: Request):
    # Futuristic email template with modern design
    template = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="utf-8">
            <title>Optimización Postural | Sistema de Bienestar Inteligente</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --primary-color: #0077BE;
                    --secondary-color: #00A4EF;
                    --background-light: #F4F7F9;
                    --background-dark: #0A192F;
                    --text-dark: #1A2C3B;
                    --text-light: #F4F7F9;
                }}
                body {{
                    font-family: 'Inter', sans-serif;
                    background-color: var(--background-light);
                    margin: 0;
                    padding: 0;
                    color: var(--text-dark);
                    line-height: 1.6;
                }}
                @media (prefers-color-scheme: dark) {{
                    body {{
                        background-color: var(--background-dark);
                        color: var(--text-light);
                    }}
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: linear-gradient(145deg, rgba(255,255,255,0.95) 0%, rgba(240,245,250,0.95) 100%);
                    border-radius: 15px;
                    overflow: hidden;
                    box-shadow: 0 10px 30px rgba(0,119,190,0.2);
                    border: 1px solid rgba(0,119,190,0.3);
                }}
                @media (prefers-color-scheme: dark) {{
                    .email-container {{
                        background: linear-gradient(145deg, rgba(15,25,50,0.9) 0%, rgba(25,35,60,0.9) 100%);
                        box-shadow: 0 10px 30px rgba(0,245,255,0.2);
                        border: 1px solid rgba(0,245,255,0.3);
                    }}
                }}
                .email-header {{
                    background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
                    color: var(--text-light);
                    padding: 20px;
                    text-align: center;
                }}
                @media (prefers-color-scheme: dark) {{
                    .email-header {{
                        color: var(--background-dark);
                    }}
                }}
                .email-header h1 {{
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                }}
                .email-content {{
                    padding: 30px;
                }}
                .email-content h2 {{
                    color: var(--primary-color);
                    border-bottom: 2px solid rgba(0,119,190,0.3);
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                @media (prefers-color-scheme: dark) {{
                    .email-content h2 {{
                        color: #00F5FF;
                        border-bottom: 2px solid rgba(0,245,255,0.3);
                    }}
                }}
                .recommendation-list {{
                    background-color: rgba(240,245,250,0.7);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                    border: 1px solid rgba(0,119,190,0.2);
                }}
                @media (prefers-color-scheme: dark) {{
                    .recommendation-list {{
                        background-color: rgba(25,35,60,0.5);
                        border: 1px solid rgba(0,245,255,0.2);
                    }}
                }}
                .recommendation-list li {{
                    margin-bottom: 15px;
                    position: relative;
                    padding-left: 30px;
                    color: var(--text-dark);
                }}
                @media (prefers-color-scheme: dark) {{
                    .recommendation-list li {{
                        color: var(--text-light);
                    }}
                }}
                .recommendation-list li:before {{
                    content: '▶';
                    color: var(--primary-color);
                    position: absolute;
                    left: 0;
                    top: 0;
                }}
                @media (prefers-color-scheme: dark) {{
                    .recommendation-list li:before {{
                        color: #00F5FF;
                    }}
                }}
                .cta-button {{
                    display: block;
                    width: 100%;
                    text-align: center;
                    padding: 15px;
                    background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
                    color: var(--text-light);
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    transition: transform 0.3s ease;
                }}
                .cta-button:hover {{
                    transform: scale(1.05);
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    font-size: 12px;
                    color: rgba(26,44,59,0.6);
                    background-color: rgba(240,245,250,0.8);
                }}
                @media (prefers-color-scheme: dark) {{
                    .footer {{
                        color: rgba(230,230,230,0.6);
                        background-color: rgba(10,25,47,0.8);
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>Sistema de monitoreo lumbar</h1>
                </div>
                <div class="email-content">
                    <h2>Análisis de Postura, {username}</h2>
                    
                    <p>Estimado {username}, nuestro sistema de monitoreo inteligente ha detectado áreas de mejora en tu ergonomía.</p>
                    
                    <div class="recommendation-list">
                        <h3>Recomendaciones Optimizadas:</h3>
                        <ul>
                            <li>Alinea tu columna vertebral con precisión durante actividades prolongadas</li>
                            <li>Distribuye uniformemente tu peso para reducir la tensión muscular</li>
                            <li>Implementa micro-pausas de estiramiento cada 45 minutos</li>
                            <li>Calibra tu entorno de trabajo para máximo rendimiento ergonómico</li>
                        </ul>
                    </div>
                    
                    <a href="#" class="cta-button">Iniciar Protocolo de Optimización</a>
                    
                    <p style="margin-top: 20px; font-size: 14px; color: var(--primary-color);">
                        Tu bienestar es nuestra prioridad. Continúa monitoreando y mejorando tu postura.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2024 Sistema de monitoreo lumbar</p>
                </div>
            </div>
        </body>
        </html>
    """

    message = MessageSchema(
        subject=f"Informe de Optimización Postural - {username}",
        recipients=[email],
        body=template,
        subtype="html",
    )
    # Enviar mensaje
    fm = FastMail(conf)
    try:
        await fm.send_message(message=message)
        return JSONResponse(status_code=200, content={"message": "El correo electrónico con recomendaciones avanzadas ha sido enviado"})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al enviar el correo electrónico: {str(e)}"
        )
    
async def send_welcome_email(email: str, username: str, request: Request):
    # Futuristic welcome email template with modern design
    template = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="utf-8">
            <title>Bienvenido a Monitoreo Lumbar | Sistema de Bienestar Inteligente</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --primary-color: #0077BE;
                    --secondary-color: #00A4EF;
                    --background-light: #F4F7F9;
                    --background-dark: #0A192F;
                    --text-dark: #1A2C3B;
                    --text-light: #F4F7F9;
                }}
                body {{
                    font-family: 'Inter', sans-serif;
                    background-color: var(--background-light);
                    margin: 0;
                    padding: 0;
                    color: var(--text-dark);
                    line-height: 1.6;
                }}
                @media (prefers-color-scheme: dark) {{
                    body {{
                        background-color: var(--background-dark);
                        color: var(--text-light);
                    }}
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: linear-gradient(145deg, rgba(255,255,255,0.95) 0%, rgba(240,245,250,0.95) 100%);
                    border-radius: 15px;
                    overflow: hidden;
                    box-shadow: 0 10px 30px rgba(0,119,190,0.2);
                    border: 1px solid rgba(0,119,190,0.3);
                }}
                @media (prefers-color-scheme: dark) {{
                    .email-container {{
                        background: linear-gradient(145deg, rgba(15,25,50,0.9) 0%, rgba(25,35,60,0.9) 100%);
                        box-shadow: 0 10px 30px rgba(0,245,255,0.2);
                        border: 1px solid rgba(0,245,255,0.3);
                    }}
                }}
                .email-header {{
                    background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
                    color: var(--text-light);
                    padding: 20px;
                    text-align: center;
                }}
                @media (prefers-color-scheme: dark) {{
                    .email-header {{
                        color: var(--background-dark);
                    }}
                }}
                .email-header h1 {{
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                }}
                .email-content {{
                    padding: 30px;
                }}
                .email-content h2 {{
                    color: var(--primary-color);
                    border-bottom: 2px solid rgba(0,119,190,0.3);
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                @media (prefers-color-scheme: dark) {{
                    .email-content h2 {{
                        color: #00F5FF;
                        border-bottom: 2px solid rgba(0,245,255,0.3);
                    }}
                }}
                .welcome-message {{
                    background-color: rgba(240,245,250,0.7);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 20px 0;
                    border: 1px solid rgba(0,119,190,0.2);
                }}
                @media (prefers-color-scheme: dark) {{
                    .welcome-message {{
                        background-color: rgba(25,35,60,0.5);
                        border: 1px solid rgba(0,245,255,0.2);
                    }}
                }}
                .welcome-message p {{
                    margin-bottom: 15px;
                    color: var(--text-dark);
                }}
                @media (prefers-color-scheme: dark) {{
                    .welcome-message p {{
                        color: var(--text-light);
                    }}
                }}
                .cta-button {{
                    display: block;
                    width: 100%;
                    text-align: center;
                    padding: 15px;
                    background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
                    color: var(--text-light);
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    transition: transform 0.3s ease;
                }}
                .cta-button:hover {{
                    transform: scale(1.05);
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    font-size: 12px;
                    color: rgba(26,44,59,0.6);
                    background-color: rgba(240,245,250,0.8);
                }}
                @media (prefers-color-scheme: dark) {{
                    .footer {{
                        color: rgba(230,230,230,0.6);
                        background-color: rgba(10,25,47,0.8);
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>Sistema de Monitoreo Lumbar</h1>
                </div>
                <div class="email-content">
                    <h2>¡Bienvenido, {username}!</h2>
                    <div class="welcome-message">
                        <p>¡Hola <strong>{username}</strong>!</p>
                        <p>Te damos la bienvenida a nuestra plataforma de Monitoreo Lumbar. Nos alegra que te hayas unido a nosotros para llevar un control adecuado de tu postura y bienestar.</p>
                        <p>A través de nuestra aplicación podrás:</p>
                        <ul>
                            <li>Monitorear tu postura y recibir recomendaciones personalizadas.</li>
                            <li>Obtener alertas cuando detectemos una mala postura.</li>
                            <li>Acceder a contenido educativo sobre ergonomía y salud lumbar.</li>
                        </ul>
                        <p>¡Estamos aquí para ayudarte a mantener una postura saludable y evitar molestias musculares!</p>
                    </div>
                    <a href="#" class="cta-button">Comienza a explorar</a>
                </div>
                <div class="footer">
                    <p>© 2024 Monitoreo Lumbar | Todos los derechos reservados</p>
                </div>
            </div>
        </body>
        </html>
    """

    message = MessageSchema(
        subject=f"Bienvenido a Monitoreo Lumbar, {username}",
        recipients=[email],
        body=template,
        subtype="html",
    )

    # Enviar mensaje
    fm = FastMail(conf)
    try:
        await fm.send_message(message=message)
        return JSONResponse(status_code=200, content={"message": "El correo electrónico de bienvenida ha sido enviado"})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al enviar el correo electrónico: {str(e)}"
        )
