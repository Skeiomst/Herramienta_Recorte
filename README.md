# Herramienta de Recorte por Figuras Geométricas (PyQt5)

Una aplicación visual que permite cargar una imagen, superponer múltiples figuras geométricas (rectángulos), moverlas libremente sin salirse de la imagen, y exportar cada área como imágenes recortadas.

---

## Instalar directamente

https://github.com/Skeiomst/Herramienta_Recorte/releases/download/v1.1.0/Herramienta_Recorte.exe

## Funcionalidades principales

- Cargar imágenes (PNG, JPG, JPEG)
- Dibujar múltiples figuras geométricas (rectángulos)
- Establecer tamaño personalizado antes de crear
- Mover figuras con el mouse (limite dentro de la imagen)
- Eliminar con tecla `Suprimir`
- Zoom in/out con rueda del ratón
- Zoom centrado en el cursor
- Botón "Resetear Zoom"
- Movimiento de figura seleciconada con teclas de flecha
- Guardar recortes individualmente
- Los recortes se guardan en una carpeta con el nombre de la imagen

## Instrucciones de uso

- Seleccionar imagen a recortar
- Con `clic derecho` se colocan las figuras del tamaño establecido en la parte superior.
- Con `clic izquierdo` se selecciona una figura ya puesta (se le da foco).
- Manteniendo presionado el `clic izquierdo`, se arrastra la figura seleccionada.
- Con `flechas` se puede arrastrar la figura seleccionada.
- Para hacer zoom, mantener presionado `Ctrl + rueda`.
- Se puede desplazar usando `rueda` (vertical) o `Alt + rueda` (horizontal).
- El botón de *Resetear Zoom*, devuelve el zoom de la imagen a su estado original.
- El botón de *Guardar Recortes*, guardará en formato .jpg, los recortes creados por las figuras establecidas anteriormente.
---

## Cómo ejecutar el programa mediante código fuente

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
