from nicegui import ui

# Datos de muestra
medicamentos = [
    {"nombre": "Paracetamol", "forma": "Tableta", "concentracion": "500 mg", "categoria": "Analgésico"},
    {"nombre": "Amoxicilina", "forma": "Cápsula", "concentracion": "500 mg", "categoria": "Antibiótico"},
    {"nombre": "Ibuprofeno", "forma": "Tableta", "concentracion": "400 mg", "categoria": "Antiinflamatorio"},
    {"nombre": "Metformina", "forma": "Tableta", "concentracion": "850 mg", "categoria": "Antidiabético"},
    {"nombre": "Losartán", "forma": "Tableta", "concentracion": "50 mg", "categoria": "Antihipertensivo"},
    {"nombre": "Omeprazol", "forma": "Cápsula", "concentracion": "20 mg", "categoria": "Antiulceroso"},
    {"nombre": "Salbutamol", "forma": "Inhalador", "concentracion": "100 mcg", "categoria": "Broncodilatador"},
]

# Definimos explícitamente la ruta raíz '/'
@ui.page('/')
def main_page():
    ui.colors(primary='#2E7D32', secondary='#1565C0', accent='#F9A825')

    with ui.header().classes('items-center justify-between'):
        ui.label('Catálogo de Medicamentos - Ecuador').classes('text-2xl font-bold')
        ui.icon('medical_services').classes('text-3xl')

    with ui.column().classes('w-full items-center p-8'):
        ui.markdown('### Buscador de Medicamentos Registrados')
        
        search = ui.input(label='Escribe el nombre o categoría...', placeholder='Ej: Paracetamol') \
            .classes('w-full max-w-lg').props('outlined rounded')

        container = ui.row().classes('w-full justify-center gap-4 mt-6')

        def actualizar_lista():
            container.clear()
            filtro = search.value.lower()
            
            resultados = [m for m in medicamentos if filtro in m['nombre'].lower() or filtro in m['categoria'].lower()]
            
            if not resultados:
                with container:
                    ui.label('No se encontraron resultados.').classes('text-grey-6 italic')
                return

            for med in resultados:
                with container:
                    with ui.card().tight().classes('w-64 hover:shadow-lg transition-shadow'):
                        with ui.column().classes('p-4'):
                            ui.label(med['nombre']).classes('text-xl font-bold text-primary')
                            ui.badge(med['categoria']).classes('bg-secondary text-white self-start')
                            ui.separator().classes('my-2')
                            ui.label(f"**Forma:** {med['forma']}")
                            ui.label(f"**Conc:** {med['concentracion']}")

        search.on('update:model-value', actualizar_lista)
        actualizar_lista()

# Es vital que ui.run() esté fuera de cualquier función
ui.run(title="Catálogo Farma EC", port=8080, reload=True)