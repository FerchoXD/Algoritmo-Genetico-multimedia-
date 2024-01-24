import os
import shutil

carpeta = './graficas'
archivo_mp4 = './generaciones.mp4'

if os.path.exists(carpeta):
    shutil.rmtree(carpeta)
    print(f"La carpeta {carpeta} ha sido eliminada.")
else:
    print(f"La carpeta {carpeta} no existe o ya fue eliminada.")

if os.path.exists(archivo_mp4):
    os.remove(archivo_mp4)
    print(f"El archivo {archivo_mp4} ha sido eliminado.")
else:
    print(f"El archivo {archivo_mp4} no existe o ya fue eliminado.")
