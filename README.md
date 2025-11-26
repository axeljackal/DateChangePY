# 📅 Modificador de Fechas de Archivos

Aplicación de escritorio liviana para Windows que permite modificar las fechas de creación y modificación de archivos de forma simple mediante interfaz gráfica.

## ✨ Características

- 🖱️ **Drag & Drop**: Arrastrá archivos o carpetas directamente a la ventana
- 📁 **Selección múltiple**: Procesá archivos individuales o carpetas completas
- 🇦🇷 **Formato argentino**: Formato de fecha DD-MM-AAAA por defecto
- 🌍 **Formato internacional**: También disponible el formato AAAA-MM-DD
- ⚡ **Procesamiento en lote**: Modificá múltiples archivos a la vez
- 📊 **Progreso visual**: Barra de progreso y estado en tiempo real
- 🔒 **Confirmación de cambios**: Previene modificaciones accidentales
- 🛡️ **Manejo de errores**: Reporta archivos con problemas sin detener el proceso

## 📋 Requisitos

- **Python 3.7 o superior**
- **Windows** (para modificar fechas de creación)
- Dependencias Python (se instalan automáticamente):
  - `tkinterdnd2` - Para drag & drop
  - `pywin32` - Para modificar fechas de creación en Windows

## 🚀 Instalación

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/axeljackal/DateChangePY.git
cd DateChangePY
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python DateChangeMain.py
```

## 📖 Uso

### Métodos para agregar archivos

1. **Arrastrar y soltar**: Arrastrá archivos o carpetas directamente a la lista
2. **Botón "Agregar Archivos"**: Seleccioná archivos mediante el explorador
3. **Botón "Agregar Carpeta"**: Agregá todos los archivos de una carpeta

### Configurar fechas

1. **Seleccionar formato**: Elegí entre formato Argentino (DD-MM-AAAA) o Internacional (AAAA-MM-DD)
2. **Ingresar fechas**: Escribí las fechas manualmente o usá el botón "Ahora"
3. **Formato de entrada**:
   - 🇦🇷 Argentino: `26-11-2025 15:30:00`
   - 🌍 Internacional: `2025-11-26 15:30:00`

### Aplicar cambios

1. Verificá que los archivos y fechas sean correctos
2. Hacé clic en "✅ Aplicar Cambios a Todos los Archivos"
3. Confirmá la operación
4. Esperá a que termine el procesamiento

## ⚙️ Opciones

- **Mantener fecha de último acceso**: Si está marcado, conserva la fecha de acceso original del archivo
- **Quitar seleccionados**: Eliminá archivos específicos de la lista sin aplicar cambios
- **Limpiar lista**: Vaciá toda la lista de archivos

## 🖼️ Capturas de pantalla

![Interfaz principal](docs/screenshot.png)

## ⚠️ Advertencias

- ⚠️ **Los cambios son irreversibles**: No se puede deshacer la modificación de fechas
- ⚠️ **Permisos de administrador**: Algunos archivos del sistema pueden requerir permisos elevados
- ⚠️ **Solo Windows**: La modificación de fechas de creación solo funciona en Windows
- ⚠️ **Archivos en uso**: No se pueden modificar archivos que estén siendo usados por otro programa

## 🔧 Solución de problemas

### Error: "No module named 'tkinterdnd2'"

```bash
pip install tkinterdnd2
```

### Error: "No module named 'win32file'"

```bash
pip install pywin32
```

### La aplicación no se abre

- Verificá que tengas Python 3.7 o superior instalado
- Ejecutá `python --version` para confirmar la versión

### No se puede modificar la fecha de creación

- Esto es normal en sistemas que no son Windows
- La fecha de modificación sí se aplicará correctamente

## 🤝 Contribuir

Las contribuciones son bienvenidas! Para contribuir:

1. Hacé un fork del proyecto
2. Creá una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Hacé commit de tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Hacé push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abrí un Pull Request

## 📝 Licencia

Este proyecto está licenciado bajo la [MIT License](./LICENSE).

Si usás este código (total o parcialmente), te pido que:

- Mantengas el aviso de copyright.
- Incluyas una referencia a este repositorio con un link:
  `https://github.com/axeljackal/DateChangePY`

## 👨‍💻 Autor

github.com/axeljackal - Hecho con ❤️ y ☕.

## 🔄 Changelog

### v1.0.0 (2025-11-26)

- ✨ Lanzamiento inicial
- ✅ Formato de fecha argentino por defecto
- ✅ Selector de formato configurable
- ✅ Drag & drop de archivos y carpetas
- ✅ Procesamiento en lote
- ✅ Barra de progreso
- ✅ Manejo de errores

---

**Nota**: Esta aplicación modifica metadatos del sistema de archivos. Usala con precaución y asegurate de tener respaldos de tus archivos importantes.
