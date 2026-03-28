from logic.database import DatabaseService

class FarmaService:
    def __init__(self, data_path="farma_ec.db"):
        self.db = DatabaseService(db_path=data_path)

    def get_categorias(self):
        """Retorna una lista única de todas las categorías disponibles desde la DB."""
        cats = self.db.get_all_categorias()
        return ["Todas"] + cats

    def buscar(self, query="", categoria="Todas", limit=50, offset=0):
        """Filtra medicamentos usando consultas SQL con soporte para paginación."""
        return self.db.search(query=query, categoria=categoria, limit=limit, offset=offset)
