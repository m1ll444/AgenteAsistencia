from nicegui import ui

# Paleta de Colores Moderna (Vibrante y Profesional)
PRIMARY = '#4CAF50'      # Verde Salud
SECONDARY = '#1565C0'    # Azul Confianza
ACCENT = '#9C27B0'       # Púrpura Energético
DARK = '#121212'         # Fondo Principal
CARD_BG = '#1E1E1E'      # Fondo Tarjetas
TEXT_LIGHT = '#F5F5F5'
TEXT_MUTED = '#BDBDBD'

def apply_styles():
    """Aplica estilos globales de CSS para el efecto Glassmorphism y temas oscuros."""
    ui.query('body').style(f'background-color: {DARK}; color: {TEXT_LIGHT}; font-family: "Inter", sans-serif;')
    
    ui.add_head_html('''
        <style>
            .glass-card {
                background: rgba(30, 30, 30, 0.7) !important;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .glass-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .sidebar-item {
                border-radius: 8px;
                margin: 4px 8px;
                transition: background 0.2s;
            }
            .sidebar-item:hover {
                background: rgba(76, 175, 80, 0.1);
            }
            .sidebar-active {
                background: rgba(76, 175, 80, 0.2) !important;
                border-left: 4px solid #4CAF50;
            }
            .kpi-badge {
                padding: 4px 12px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 0.8rem;
            }
            /* Scrollbar personalizado */
            ::-webkit-scrollbar {
                width: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #121212;
            }
            ::-webkit-scrollbar-thumb {
                background: #333;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #444;
            }
        </style>
    ''')
