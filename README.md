# Herramienta de Recorte por Figuras Geométricas (PyQt5)

Una aplicación visual que permite cargar una imagen, superponer múltiples figuras geométricas (rectángulos), moverlas libremente sin salirse de la imagen, y exportar cada área como imágenes recortadas.

---

## Funcionalidades principales

- Cargar imágenes (PNG, JPG, JPEG)
- Dibujar múltiples figuras geométricas (rectángulos)
- Establecer tamaño personalizado antes de crear
- Mover figuras con el mouse (limite dentro de la imagen)
- Eliminar con tecla `Suprimir`
- Zoom in/out con rueda del ratón
- Zoom centrado en el cursor
- Botón "Resetear Zoom"
- Guardar recortes individualmente
- Los recortes se guardan en una carpeta con el nombre de la imagen

---

## Cómo ejecutar el programa

### Requisitos

- Python 3.7 o superior
- PyQt5
- Pillow

Instalar dependencias:

```bash
pip install -r requirements.txt
```
Ejecutar:
```bash
python main.py
```


## Estructura de salida al guardar recortes

/ruta_seleccionada/nombre_imagen/
|--nombre_imagen_recorte_1.jpg
|--nombre_imagen_recorte_2.jpg
|--...

## Autor

- Samuel Pérez
- Hecho con Python