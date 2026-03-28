from nicegui import ui
from logic.farma_svc import FarmaService
from logic.sync_svc import SyncService
from ui.components import medicine_card, kpi_card, sidebar_item, dashboard_stats
from ui.styles import apply_styles, PRIMARY, DARK, TEXT_LIGHT, TEXT_MUTED, SECONDARY
import math

# Inicializar servicios
svc = FarmaService()
sync_svc = SyncService()

ITEMS_PER_PAGE = 24  # 24 tarjetas por página (6x4 grid)

@ui.page('/')
async def main_page():
    # Estado de la navegación
    state = {'view': 'dashboard', 'category': 'Todas', 'query': '', 'page': 1}
    
    apply_styles()

    # --- HEADER ---
    with ui.header().classes('p-4 justify-between items-center shadow-lg border-b border-white/10').style(f'background-color: {DARK}'):
        with ui.row().classes('items-center gap-4'):
            ui.button(on_click=lambda: left_drawer.toggle()).props('flat round icon=menu color=white')
            ui.icon('health_and_safety', color=PRIMARY).classes('text-3xl')
            with ui.column().classes('gap-0'):
                ui.label('FARMA EC v2').classes('text-xl font-bold text-white tracking-widest')
                ui.label('Sistema Nacional de Gestión Farmacéutica').classes('text-[10px] text-green-100 opacity-60 uppercase')
        
        with ui.row().classes('items-center gap-2'):
            search_input = ui.input(placeholder='Buscar en catálogo...', on_change=lambda: handle_search()) \
                .props('dark borderless dense clearable input-class="text-sm"').classes('bg-white/5 px-4 rounded-full w-64')
            search_input.props('debounce=500')
            
            ui.button(icon='refresh', on_click=lambda: handle_sync()) \
                .props('flat round color=primary').classes('ml-2')

    # --- SIDEBAR (LEFT DRAWER) ---
    with ui.left_drawer(value=True, fixed=True).classes('bg-neutral-900 border-r border-white/5 p-0') as left_drawer:
        with ui.column().classes('w-full gap-0'):
            ui.label('NAVEGACIÓN').classes('px-6 py-4 text-[10px] font-bold text-muted opacity-40 uppercase tracking-widest')
            
            nav_dashboard = ui.column().classes('w-full')
            with nav_dashboard:
                sidebar_item('Resumen General', 'dashboard', lambda: switch_view('dashboard'), active=(state['view'] == 'dashboard'))
            
            ui.label('CATEGORÍAS TOP').classes('px-6 py-4 text-[10px] font-bold text-muted opacity-40 uppercase tracking-widest')
            
            categories_container = ui.column().classes('w-full gap-0')
            def update_sidebar():
                categories_container.clear()
                top_cats = svc.db.get_top_categories(limit=12)
                for cat in top_cats:
                    with categories_container:
                        sidebar_item(
                            cat['name'], 'label', 
                            lambda c=cat['name']: switch_view('catalog', c),
                            count=cat['count'],
                            active=(state['category'] == cat['name'])
                        )
            update_sidebar()

    # --- CONTENIDO PRINCIPAL ---
    main_container = ui.column().classes('w-full p-8 gap-8 items-center min-h-screen')

    async def switch_view(view, category='Todas'):
        state['view'] = view
        state['category'] = category
        state['page'] = 1
        state['query'] = ''
        search_input.set_value('')
        await update_ui()
        update_sidebar()

    async def handle_search():
        if search_input.value:
            state['view'] = 'catalog'
            state['query'] = search_input.value
            state['page'] = 1
        await update_ui()

    async def go_to_page(page):
        state['page'] = page
        await update_ui()

    async def update_ui():
        main_container.clear()
        
        if state['view'] == 'dashboard':
            with main_container:
                ui.label('Panel de Control Ciudadano').classes('text-3xl font-bold self-start mb-4')
                stats = svc.db.get_stats()
                dashboard_stats(stats)
                
                with ui.row().classes('w-full gap-6 mt-4'):
                    with ui.card().classes('glass-card p-6 flex-grow'):
                        ui.label('Distribución por Estado Administrativo').classes('text-sm font-bold opacity-60 mb-6 uppercase')
                        ui.echart({
                            'xAxis': {'type': 'category', 'data': list(stats['estados'].keys()), 'axisLabel': {'color': '#999'}},
                            'yAxis': {'type': 'value', 'splitLine': {'lineStyle': {'color': 'rgba(255,255,255,0.05)'}}},
                            'series': [{'data': list(stats['estados'].values()), 'type': 'bar', 'itemStyle': {'color': PRIMARY, 'borderRadius': [4,4,0,0]}}],
                            'tooltip': {'trigger': 'axis'}
                        }).classes('w-full h-64')
                    
                    with ui.card().classes('glass-card p-6 w-1/3'):
                        ui.label('Sincronización ARCSA').classes('text-sm font-bold opacity-60 mb-4 uppercase')
                        with ui.column().classes('items-center py-4'):
                            ui.icon('cloud_done', color=PRIMARY, size='64px')
                            ui.label('Base de Datos Actualizada').classes('mt-4 font-bold')
                            ui.label('Fuente: Portal de Consultas Públicas').classes('text-[10px] opacity-40')
                            ui.button('Sincronizar Ahora', on_click=lambda: handle_sync()).props('outline color=primary icon=sync').classes('mt-6 w-full')

        elif state['view'] == 'catalog':
            with main_container:
                # Contar total de resultados
                total_count = svc.db.count_results(state['query'], state['category'])
                total_pages = max(1, math.ceil(total_count / ITEMS_PER_PAGE))
                current_page = min(state['page'], total_pages)
                offset = (current_page - 1) * ITEMS_PER_PAGE

                # Header con info de paginación
                with ui.row().classes('w-full justify-between items-end mb-4'):
                    with ui.column().classes('gap-0'):
                        title = state['category'] if state['category'] != 'Todas' else state['query']
                        ui.label(f"Explorando: {title}").classes('text-3xl font-bold')
                        ui.label(f"{total_count:,} registros encontrados · Página {current_page} de {total_pages}").classes('text-sm opacity-60')
                
                # Grid de tarjetas
                items = svc.buscar(state['query'], state['category'], limit=ITEMS_PER_PAGE, offset=offset)
                
                if not items:
                    with ui.column().classes('items-center w-full mt-20 opacity-40'):
                        ui.icon('search_off', size='80px', color=PRIMARY)
                        ui.label('No se encontraron registros.').classes('text-xl italic mt-4')
                else:
                    with ui.row().classes('w-full justify-center gap-6 flex-wrap'):
                        for item in items:
                            medicine_card(item)

                # --- PAGINACIÓN NUMÉRICA ---
                if total_pages > 1:
                    with ui.row().classes('w-full justify-center items-center gap-1 mt-8'):
                        # Botón Anterior
                        ui.button(icon='chevron_left', on_click=lambda: go_to_page(current_page - 1)) \
                            .props(f'flat round color=primary {"disable" if current_page == 1 else ""}')
                        
                        # Números de página (mostrar máximo 7 páginas)
                        pages_to_show = _get_page_range(current_page, total_pages)
                        
                        prev_p = None
                        for p in pages_to_show:
                            if prev_p is not None and p - prev_p > 1:
                                ui.label('...').classes('px-2 opacity-40')
                            
                            if p == current_page:
                                ui.button(str(p), on_click=lambda pg=p: go_to_page(pg)) \
                                    .props('color=primary').classes('min-w-[40px]')
                            else:
                                ui.button(str(p), on_click=lambda pg=p: go_to_page(pg)) \
                                    .props('flat color=white').classes('min-w-[40px] opacity-60')
                            prev_p = p
                        
                        # Botón Siguiente
                        ui.button(icon='chevron_right', on_click=lambda: go_to_page(current_page + 1)) \
                            .props(f'flat round color=primary {"disable" if current_page == total_pages else ""}')

    async def handle_sync():
        ui.notify('Sincronizando con ARCSA...', type='info', icon='cloud_download', spinner=True)
        url = sync_svc.find_latest_excel_url()
        if sync_svc.download_catalog(url):
            res = sync_svc.process_excel()
            if "error" not in res:
                ui.notify(f"Éxito: {res['total']} fármacos procesados.", type='positive')
                await switch_view('dashboard')
            else:
                ui.notify(res['error'], type='negative')

    await update_ui()

def _get_page_range(current, total):
    """Calcula qué números de página mostrar (máx 7, con elipsis)."""
    if total <= 7:
        return list(range(1, total + 1))
    
    pages = set()
    pages.add(1)
    pages.add(total)
    
    # Páginas alrededor de la actual
    for i in range(max(1, current - 2), min(total + 1, current + 3)):
        pages.add(i)
    
    return sorted(pages)

# Iniciar App
ui.run(title="FarmaEC v2 - Inteligencia Farmacéutica", port=8080, dark=True, favicon='💊')
