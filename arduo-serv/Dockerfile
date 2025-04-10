# Usa una imagen ligera de Python
FROM python:3.11-slim

# Crear usuario no root
RUN useradd -m appuser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias y script
COPY requirements.txt sender.py /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ajustar permisos
RUN chown -R appuser:appuser /app

# Cambiar al usuario no root
USER appuser

# Comando por defecto: ejecutar el script
CMD ["python", "-u", "sender.py"]
