
from multiprocessing import Process, Queue
import signal
import sys
import sensor_archivo_externo
import gps_archivo_externo

def exit_handler(sig, frame):
    global p1, p2
    print("\nFinalizando procesos...")
    p1.terminate()
    p2.terminate()
    sensor_archivo_externo.exit_handler #desconexion del cliente del sensor
    sys.exit(0)
    

global q
q = Queue()

if __name__ == "__main__":
    # Registrar el manejador de la señal Ctrl+C
    signal.signal(signal.SIGINT, exit_handler)

    
    p1 = Process(target=sensor_archivo_externo.process_heart_rate, args=(q,))
    p2 = Process(target=gps_archivo_externo.process_gps, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
