import sqlite3
import os

class DatabaseService:
    def __init__(self, db_path="farma_ec.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Inicializa la base de datos y crea la tabla si no existe."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medicamentos (
                    registro TEXT PRIMARY KEY,
                    nombre TEXT,
                    forma TEXT,
                    concentracion TEXT,
                    categoria TEXT,
                    titular TEXT,
                    fabricante TEXT,
                    forma_venta TEXT,
                    estado TEXT,
                    ultima_actualizacion TEXT
                )
            ''')
            # Índice para búsquedas rápidas por nombre y categoría
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_nombre ON medicamentos(nombre)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_categoria ON medicamentos(categoria)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_titular ON medicamentos(titular)')
            conn.commit()

    def save_batch(self, batch):
        """Guarda un lote de medicamentos de forma eficiente."""
        query = '''
            INSERT OR REPLACE INTO medicamentos 
            (registro, nombre, forma, concentracion, categoria, titular, fabricante, forma_venta, estado, ultima_actualizacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        data = [
            (
                m.get('registro'),
                m.get('nombre'),
                m.get('forma'),
                m.get('concentracion'),
                m.get('categoria'),
                m.get('titular'),
                m.get('fabricante'),
                m.get('forma_venta'),
                m.get('estado'),
                m.get('ultima_actualizacion')
            )
            for m in batch
        ]
        with self._get_connection() as conn:
            conn.executemany(query, data)
            conn.commit()

    def get_all_categorias(self):
        """Retorna una lista única de categorías."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT categoria FROM medicamentos WHERE categoria IS NOT NULL ORDER BY categoria')
            return [row[0] for row in cursor.fetchall()]

    def get_stats(self):
        """Retorna estadísticas generales para el dashboard."""
        stats = {
            'total': 0,
            'vigentes': 0,
            'categorias_count': 0,
            'laboratorios': 0,
            'estados': {} # {estado: count}
        }
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Total
            cursor.execute('SELECT COUNT(*) FROM medicamentos')
            stats['total'] = cursor.fetchone()[0]
            # Vigentes
            cursor.execute("SELECT COUNT(*) FROM medicamentos WHERE estado = 'VIGENTE'")
            stats['vigentes'] = cursor.fetchone()[0]
            # Categorías
            cursor.execute('SELECT COUNT(DISTINCT categoria) FROM medicamentos')
            stats['categorias_count'] = cursor.fetchone()[0]
            # Laboratorios
            cursor.execute('SELECT COUNT(DISTINCT titular) FROM medicamentos')
            stats['laboratorios'] = cursor.fetchone()[0]
            # Distribución por estado
            cursor.execute('SELECT estado, COUNT(*) FROM medicamentos GROUP BY estado')
            stats['estados'] = {row[0]: row[1] for row in cursor.fetchall()}
            
        return stats

    def get_top_categories(self, limit=10):
        """Retorna las N categorías con más fármacos."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT categoria, COUNT(*) as total 
                FROM medicamentos 
                WHERE categoria IS NOT NULL 
                GROUP BY categoria 
                ORDER BY total DESC 
                LIMIT ?
            ''', (limit,))
            return [{'name': row[0], 'count': row[1]} for row in cursor.fetchall()]

    def search(self, query="", categoria="Todas", limit=50, offset=0):
        """Realiza una búsqueda filtrada con soporte para paginación."""
        sql = "SELECT * FROM medicamentos WHERE 1=1"
        params = []

        if categoria != "Todas":
            sql += " AND categoria = ?"
            params.append(categoria)

        if query:
            sql += " AND (nombre LIKE ? OR registro LIKE ? OR titular LIKE ? OR categoria LIKE ?)"
            search_val = f"%{query}%"
            params.extend([search_val, search_val, search_val, search_val])

        sql += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def count_results(self, query="", categoria="Todas"):
        """Cuenta el total de resultados para una búsqueda (para paginación)."""
        sql = "SELECT COUNT(*) FROM medicamentos WHERE 1=1"
        params = []

        if categoria != "Todas":
            sql += " AND categoria = ?"
            params.append(categoria)

        if query:
            sql += " AND (nombre LIKE ? OR registro LIKE ? OR titular LIKE ? OR categoria LIKE ?)"
            search_val = f"%{query}%"
            params.extend([search_val, search_val, search_val, search_val])

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchone()[0]
