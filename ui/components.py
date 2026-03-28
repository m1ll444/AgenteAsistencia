from nicegui import ui
from ui.styles import PRIMARY, SECONDARY, ACCENT, TEXT_LIGHT, TEXT_MUTED, CARD_BG

def kpi_card(title, value, icon, color=PRIMARY):
    """Crea una tarjeta KPI elegante con Glassmorphism."""
    with ui.card().classes('glass-card p-6 flex-grow min-w-[200px] items-center text-center'):
        with ui.row().classes('items-center mb-2 gap-4'):
            ui.icon(icon, color=color, size='32px')
            ui.label(title).classes('text-xs font-bold uppercase tracking-wider text-muted').style(f'color: {TEXT_MUTED}')
        ui.label(value).classes('text-4xl font-extrabold').style(f'color: {TEXT_LIGHT}')

def sidebar_item(label, icon, on_click, count=None, active=False):
    """Crea un ítem interactivo para la barra lateral."""
    classes = 'sidebar-item w-full px-4 py-3 cursor-pointer flex items-center gap-4 transition-all'
    if active:
        classes += ' sidebar-active'
    
    with ui.row().classes(classes).on('click', on_click):
        ui.icon(icon, size='sm', color=PRIMARY if active else TEXT_MUTED)
        ui.label(label).classes('text-sm font-medium flex-grow' + (' text-primary' if active else ' text-white'))
        if count is not None:
            ui.badge(str(count)).classes('kpi-badge').style(f'background: rgba(255,255,255,0.05); color: {TEXT_MUTED};')

def show_detail_dialog(med):
    """Abre un diálogo modal con todos los detalles del medicamento."""
    estado = med.get('estado', 'VIGENTE').upper()
    is_vigente = 'VIGENTE' in estado and 'NO' not in estado
    color_estado = PRIMARY if is_vigente else '#FF5252'

    with ui.dialog() as dialog, ui.card().classes('w-full max-w-2xl p-0 overflow-hidden').style(f'background: {CARD_BG}; border: 1px solid rgba(255,255,255,0.1);'):
        # Barra superior de color
        with ui.row().classes('w-full h-2').style(f'background: {color_estado}'):
            pass

        with ui.column().classes('p-8 gap-6 w-full'):
            # Header del diálogo
            with ui.row().classes('w-full justify-between items-start'):
                with ui.column().classes('gap-1 flex-grow'):
                    ui.label(med.get('nombre', 'N/A').title()).classes('text-2xl font-bold text-white')
                    ui.label(med.get('registro', 'N/A')).classes('text-sm').style(f'color: {TEXT_MUTED}')
                ui.badge('VIGENTE' if is_vigente else 'NO VIGENTE') \
                    .classes('px-3 py-1 text-xs') \
                    .style(f'background: {color_estado}22; color: {color_estado}; border: 1px solid {color_estado}44;')

            ui.separator().classes('bg-white/10')

            # Información detallada en grid
            detail_fields = [
                ('Categoría / Principio Activo', med.get('categoria', 'Sin Categoría'), 'category', SECONDARY),
                ('Forma Farmacéutica', med.get('forma', 'N/A'), 'medication_liquid', TEXT_MUTED),
                ('Concentración', med.get('concentracion', 'N/A'), 'science', TEXT_MUTED),
                ('Forma de Venta', med.get('forma_venta', 'N/A'), 'storefront', TEXT_MUTED),
                ('Titular del Registro', med.get('titular', 'N/A'), 'business', ACCENT),
                ('Fabricante', med.get('fabricante', 'N/A'), 'factory', TEXT_MUTED),
                ('Estado Administrativo', med.get('estado', 'N/A'), 'verified', color_estado),
                ('Última Actualización', med.get('ultima_actualizacion', 'N/A'), 'update', TEXT_MUTED),
            ]

            with ui.grid(columns=2).classes('w-full gap-4'):
                for label, value, icon, color in detail_fields:
                    with ui.card().classes('p-4').style('background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px;'):
                        with ui.row().classes('items-center gap-2 mb-1'):
                            ui.icon(icon, size='16px', color=color)
                            ui.label(label).classes('text-[10px] font-bold uppercase tracking-wider').style(f'color: {TEXT_MUTED}')
                        ui.label(str(value) if value else 'N/A').classes('text-sm text-white break-words')

            # Botón de cerrar
            with ui.row().classes('w-full justify-end'):
                ui.button('Cerrar', on_click=dialog.close) \
                    .props('flat color=primary').classes('mt-2')

    dialog.open()

def medicine_card(med):
    """Crea una tarjeta compacta para un fármaco con botón Ver Detalles funcional."""
    estado = med.get('estado', 'VIGENTE').upper()
    is_vigente = 'VIGENTE' in estado and 'NO' not in estado
    color_estado = PRIMARY if is_vigente else '#FF5252'
    
    with ui.card().classes('glass-card p-0 overflow-hidden w-full max-w-sm'):
        # Cabecera con indicación de estado
        with ui.row().classes('w-full h-1').style(f'background: {color_estado}'):
            pass
            
        with ui.column().classes('p-6 gap-3'):
            with ui.row().classes('w-full justify-between items-start no-wrap'):
                with ui.column().classes('gap-0 truncate'):
                    ui.label(med.get('nombre', 'N/A').title()).classes('text-xl font-bold truncate w-full text-white')
                    ui.label(med.get('registro', 'N/A')).classes('text-xs').style(f'color: {TEXT_MUTED}')
                
                ui.badge('VIGENTE' if is_vigente else 'NO VIGENTE') \
                    .classes('px-2 py-1 text-[10px]') \
                    .style(f'background: {color_estado}22; color: {color_estado}; border: 1px solid {color_estado}44;')

            ui.separator().classes('bg-white/10')
            
            with ui.column().classes('gap-2 text-sm'):
                with ui.row().classes('w-full gap-2 items-center'):
                    ui.icon('category', size='16px', color=SECONDARY)
                    ui.label(med.get('categoria', 'Sin Categoría')).classes('font-medium text-blue-200')
                
                with ui.row().classes('w-full gap-2 items-center'):
                    ui.icon('factory', size='16px', color=TEXT_MUTED)
                    ui.label(med.get('fabricante', 'N/A')).classes('truncate text-xs opacity-80')

                with ui.row().classes('w-full gap-2 items-center'):
                    ui.icon('science', size='16px', color=TEXT_MUTED)
                    ui.label(med.get('concentracion', 'N/A')).classes('text-[11px] opacity-70')
            
            with ui.row().classes('w-full justify-end mt-2'):
                ui.button('Ver Detalles', icon='visibility', 
                          on_click=lambda m=med: show_detail_dialog(m)) \
                    .props('flat dense color=primary').classes('text-xs')

def dashboard_stats(stats):
    """Renderiza el grid de métricas del dashboard."""
    with ui.row().classes('w-full gap-6 justify-between'):
        kpi_card('Fármacos Registrados', f"{stats['total']:,}", 'inventory_2', PRIMARY)
        kpi_card('Estados Vigentes', f"{stats['vigentes']:,}", 'check_circle', '#81C784')
        kpi_card('Categorías Únicas', str(stats['categorias_count']), 'category', SECONDARY)
        kpi_card('Laboratorios', str(stats['laboratorios']), 'business', ACCENT)
