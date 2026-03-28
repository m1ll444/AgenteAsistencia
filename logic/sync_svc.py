import requests
import os
import sqlite3
import re
import html
from datetime import datetime
from logic.database import DatabaseService

class SyncService:
    def __init__(self, data_path="farma_ec.db"):
        self.db = DatabaseService()
        self.temp_file = "catalogo_temp.xls"

    def find_latest_excel_url(self):
        """Retorna el endpoint de reporte masivo del portal de consultas."""
        return "https://aplicaciones.controlsanitario.gob.ec/publico/consultas/reporte/1"

    def download_catalog(self, url):
        """Descarga el reporte masivo de ARCSA."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, stream=True, timeout=60, headers=headers)
            response.raise_for_status()
            with open(self.temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Error descargando: {e}")
            return False

    def process_excel(self):
        """Procesa el archivo descargado. Detecta si es HTML y usa streaming para archivos grandes."""
        if not os.path.exists(self.temp_file):
            return {"error": "Archivo no encontrado"}

        try:
            # Detectar si es HTML
            with open(self.temp_file, 'r', encoding='utf-8', errors='ignore') as f:
                first_lines = "".join([f.readline() for _ in range(10)]).lower()
                if "<table" in first_lines or "<html" in first_lines or "<tr>" in first_lines:
                    return self._process_html_streaming()
            
            return {"error": "Formato no soportado (se esperaba HTML Table)"}

        except Exception as e:
            return {"error": f"Error procesando archivo: {str(e)}"}
        finally:
            if os.path.exists(self.temp_file):
                try: os.remove(self.temp_file)
                except: pass

    def _process_html_streaming(self):
        """Procesa una tabla HTML gigante de forma eficiente."""
        headers = []
        batch = []
        count = 0
        
        # Regex básico para extraer contenido entre tags
        re_td = re.compile(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', re.IGNORECASE | re.DOTALL)
        
        with open(self.temp_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Separar por <tr>
        rows = re.split(r'<tr>', content, flags=re.IGNORECASE)
        
        for row_content in rows:
            if not row_content.strip(): continue
            
            cells = [html.unescape(m.group(1)).strip() for m in re_td.finditer(row_content)]
            
            if not cells: continue

            if not headers:
                headers = [self._clean_header(c.lower()) for c in cells]
                continue
            
            item = self._map_columns(headers, cells)
            if item.get('nombre') and item.get('registro'):
                item['ultima_actualizacion'] = datetime.now().strftime("%Y-%m-%d")
                if not item.get('categoria'):
                    item['categoria'] = self._infer_category(item)
                
                batch.append(item)
                count += 1
                
                if len(batch) >= 1000:
                    self.db.save_batch(batch)
                    batch = []

        if batch:
            self.db.save_batch(batch)

        return {"nuevos": count, "actualizados": 0, "total": count}

    def _infer_category(self, item):
        """Infiere una categoría amigable basada en palabras clave si no hay nombre genérico."""
        nombre = item.get('nombre', '').upper()
        if 'AMOXICILINA' in nombre: return 'ANTIBIÓTICO'
        if 'PARACETAMOL' in nombre: return 'ANALGÉSICO'
        if 'VITAMINA' in nombre: return 'VITAMINAS'
        if 'SOLUCIÓN' in nombre: return 'SOLUCIONES'
        return 'Sin Categoría'

    def _clean_header(self, text):
        """Limpia caracteres de control y espacios extras."""
        return re.sub(r'[\r\n\t\s]+', '_', text.strip()).lower()

    def _map_columns(self, headers, cells):
        """Mapea columnas usando los nombres EXACTOS del archivo ARCSA.
        
        Headers reales (42 columnas):
          0: numero_registro_sanitario    24: nombre_producto
          4: estado                       9: titular_producto
          11: nombre_fabricante           26: forma_farmaceutica
          31: forma_venta                 34: concentracion_principio_activo
          35: principios_activos          38: clasificacion_producto
        """
        item = {}
        for i, h in enumerate(headers):
            if i >= len(cells): break
            val = cells[i].strip()
            if not val or val == "N/A": continue
            
            # Mapeo exacto con nombres reales del catálogo ARCSA
            if h == "nombre_producto": 
                item['nombre'] = val
            elif h == "numero_registro_sanitario": 
                item['registro'] = val
            elif h == "titular_producto" or h == "nombre_razon_social_solicitante": 
                item['titular'] = val
            elif h == "nombre_fabricante": 
                item['fabricante'] = val
            elif h == "forma_farmaceutica": 
                item['forma'] = val
            elif h == "concentracion_principio_activo": 
                item['concentracion'] = val
            elif h == "forma_venta": 
                item['forma_venta'] = val
            elif h == "estado": 
                item['estado'] = val
            elif h == "principios_activos":
                # Extraer el principio activo del texto largo
                # Formato típico: "Cada 100 gramos contiene:\nAciclovir ......... 5g"
                cat = self._extract_active_ingredient(val)
                if cat:
                    item['categoria'] = cat
            elif h == "clasificacion_producto" and not item.get('categoria'):
                item['categoria'] = val.strip().title()
        return item

    def _extract_active_ingredient(self, text):
        """Extrae el nombre del principio activo de la descripción larga."""
        # Buscar después de "contiene:" o "contienen:"
        match = re.search(r'contiene[n]?\s*:?\s*(.+)', text, re.IGNORECASE | re.DOTALL)
        if match:
            remainder = match.group(1).strip()
        else:
            remainder = text.strip()
        
        # Tomar la primera línea significativa (ignorar líneas vacías)
        lines = [l.strip() for l in remainder.split('\n') if l.strip()]
        if not lines:
            return None
        
        first_line = lines[0]
        # Limpiar puntos suspensivos, cantidades, y porcentajes
        name = re.split(r'[\.\d]+\s*(mg|g|ml|%|mcg|ui|usp)', first_line, flags=re.IGNORECASE)[0]
        name = name.strip(' .\t*$')
        
        if len(name) < 3 or len(name) > 50:
            return None
        
        return name.title()
