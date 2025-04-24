# Distributed Task Queue System

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un sistema de cola de tareas distribuido que permite ejecutar tareas asíncronas en paralelo mediante workers.

## Características principales

- 🚀 Ejecución concurrente de tareas usando `asyncio`
- ⚡ Procesamiento paralelo con `multiprocessing`
- 🖥️ Interfaz interactiva con menú de opciones
- 📊 Visualización de logs y resultados en tiempo real
- 🔄 Capacidad de limpiar la pantalla cuando sea necesario
- ⏹️ Apagado seguro de workers

## Requisitos

- Python 3.7 o superior
- Sistema operativo: Windows/macOS/Linux

## Instalación

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/distributed-task-queue.git](https://github.com/CirveRescue/Distributed-Task-Queue-System.git)
   cd distributed-task-queue

2. (Opcional) Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

## Uso

Ejecuta el sistema:
```bash
python interactive_task_queue.py
```

### Opciones del menú:
1. **Agregar tarea**: Ingresa segundos a esperar (ej: 3)
2. **Ver resultados**: Muestra los resultados de tareas completadas
3. **Limpiar pantalla**: Borra los logs de la consola
4. **Apagar workers**: Detiene el sistema de forma segura

### Ejemplo de flujo:
```
✅ Se iniciaron 2 workers.
Worker 0 procesando tarea 1...
Tarea 1 completada: 3² = 9

========================================
--- MENÚ PRINCIPAL ---
1. Agregar tarea
2. Ver resultados
3. Limpiar pantalla
4. Apagar workers
Seleccione una opción: _
```

## Estructura del código

```
interactive_task_queue.py
├── DisplayManager          # Manejo de la interfaz visual
├── example_task           # Función de ejemplo (espera n segundos)
├── worker_process         # Lógica del worker (multiprocessing + asyncio)
└── InteractiveTaskQueue   # Sistema principal (cola de tareas/results)
```

## Personalización

Para añadir tus propias tareas:
1. Crea nuevas funciones async:
   ```python
   async def mi_tarea(param1, param2):
       await asyncio.sleep(1)
       return param1 + param2
   ```
2. Modifica el menú para usar tus funciones

