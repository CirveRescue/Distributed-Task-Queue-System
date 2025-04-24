import asyncio
import multiprocessing
from multiprocessing import Queue, Process
import signal
import os
from typing import Callable, Any
import threading
import time

# --- Configuración de pantalla ---
class DisplayManager:

    def clear_logs(self):
        """Limpia todos los logs almacenados"""
        self.logs = []
        self._refresh_display()

    def __init__(self):
        self.logs = []
        self.last_menu = ""
    
    def add_log(self, message):
        self.logs.append(message)
        self._refresh_display()
    
    def show_menu(self, menu_text):
        self.last_menu = menu_text
        self._refresh_display()
    
    def _refresh_display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n".join(self.logs[-10:]))  # Muestra los últimos 10 logs
        print("\n" + "="*40)
        print(self.last_menu)

display = DisplayManager()

# --- Task Function ---
async def example_task(seconds: int) -> int:
    """Tarea de ejemplo: espera 'seconds' segundos y devuelve el cuadrado."""
    await asyncio.sleep(seconds)
    return seconds ** 2

# --- Worker Process ---
def worker_process(
    worker_id: int,
    task_queue: Queue,
    result_queue: Queue,
    shutdown_event: multiprocessing.Event,
    log_queue: Queue
):
    """Worker que procesa tareas asíncronas."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def run():
        while not shutdown_event.is_set():
            try:
                if not task_queue.empty():
                    task_id, func, args = task_queue.get_nowait()
                    log_queue.put(f"Worker {worker_id} procesando tarea {task_id}...")
                    try:
                        result = await func(*args)
                        result_queue.put((task_id, result))
                        log_queue.put(f"Tarea {task_id} completada: {args[0]}² = {result}")
                    except Exception as e:
                        result_queue.put((task_id, f"Error: {e}"))
                        log_queue.put(f"Error en tarea {task_id}: {e}")
                else:
                    await asyncio.sleep(0.1)
            except Exception as e:
                log_queue.put(f"Worker {worker_id} error: {e}")

    loop.run_until_complete(run())
    loop.close()

# --- Interactive Master ---
class InteractiveTaskQueue:
    def __init__(self, num_workers: int = 2):
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.log_queue = Queue()
        self.shutdown_event = multiprocessing.Event()
        self.workers = []
        self.task_counter = 0
        self.num_workers = num_workers
        self.log_thread = None

    def start_workers(self):
        """Inicia los workers."""
        for i in range(self.num_workers):
            p = Process(
                target=worker_process,
                args=(i, self.task_queue, self.result_queue, self.shutdown_event, self.log_queue),
            )
            p.start()
            self.workers.append(p)
        
        display.add_log(f"✅ Se iniciaron {self.num_workers} workers.")
        
        # Hilo para mostrar logs
        self.log_thread = threading.Thread(target=self._monitor_logs, daemon=True)
        self.log_thread.start()

    def _monitor_logs(self):
        """Monitoriza la cola de logs en segundo plano."""
        while not self.shutdown_event.is_set():
            try:
                while not self.log_queue.empty():
                    log = self.log_queue.get_nowait()
                    display.add_log(log)
            except:
                pass
            time.sleep(0.1)

    async def add_task(self, func: Callable, *args: Any) -> int:
        """Añade una tarea y devuelve su ID."""
        self.task_counter += 1
        self.task_queue.put((self.task_counter, func, args))
        display.add_log(f"✅ Tarea {self.task_counter} agregada (esperará {args[0]} segundos).")
        return self.task_counter

    async def show_results(self):
        """Muestra resultados pendientes."""
        results = []
        while not self.result_queue.empty():
            task_id, result = self.result_queue.get_nowait()
            results.append(f"📦 Resultado de tarea {task_id}: {result}")
        
        if results:
            for msg in results:
                display.add_log(msg)
        else:
            display.add_log("No hay resultados nuevos.")

    def _get_menu_text(self):
        return """--- MENÚ PRINCIPAL ---
1. Agregar tarea (ej: esperar N segundos)
2. Ver resultados
3. Limpiar pantalla
4. Apagar workers y salir
Seleccione una opción: """

    async def menu(self):
        """Menú interactivo."""
        while True:
            display.show_menu(self._get_menu_text())
            choice = input().strip()

            if choice == "1":
                try:
                    seconds = int(input("Ingrese segundos a esperar (ej: 2): ").strip())
                    await self.add_task(example_task, seconds)
                except ValueError:
                    display.add_log("❌ Error: Ingrese un número válido.")

            elif choice == "2":
                await self.show_results()

            elif choice == "3":  # Nueva opción para limpiar pantalla
                display.clear_logs()
                display.add_log("✅ Pantalla limpiada")

            elif choice == "4":
                display.add_log("\n🛑 Apagando workers...")
                self.shutdown_event.set()
                for p in self.workers:
                    p.join(timeout=1)
                display.add_log("Saliendo del programa.")
                break

            else:
                display.add_log("❌ Opción no válida.")

# --- Main ---
if __name__ == "__main__":
    system = InteractiveTaskQueue(num_workers=2)
    system.start_workers()

    # Manejar Ctrl+C para apagar workers
    def signal_handler(sig, frame):
        display.add_log("\n🛑 Recibida señal de interrupción (Ctrl+C).")
        system.shutdown_event.set()
        for p in system.workers:
            p.join(timeout=0.5)
        os._exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Iniciar menú interactivo
    asyncio.run(system.menu())