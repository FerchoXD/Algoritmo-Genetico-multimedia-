import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cv2 as cv
import numpy as np
import os
## Este programita tiene métodos que permiten animar una gráfica, grabarVideo de una gráfica, 
## Además se incorpora un método para grabar varios videos a partir de varias animaciones
## unirVideos permite unir todos los videos previamente guardados

##Nota: En mi caso no puedo reproducir el video creado directamente en vscode, por algún detalle de compatibilidad
##Entre paquetes o algo así, pero si se reproduce con algún reproductor externo.
def animarPlot(x,y):    
    fig,ax = plt.subplots();    
    def actualizarPlot(i):
        ax.clear()        
        ax.scatter(x[:i],y[:i])
        #Esta es una forma para ajustar los ejes, pero uds pueden usar la que gusten se adapten
        ##mejor a sus gráficas
        ax.set_xlim([1.1*np.min(x),1.1*np.max(x)])
        ax.set_ylim([1.1*np.min(y),1.1*np.max(y)])
    ##Usen interval como 0 en caso que quieran que su animación sea lo más rápida posible
    animar = FuncAnimation(fig, actualizarPlot,range(len(x)),interval=0, cache_frame_data=False, repeat = False)
    #plt.show() #Solo para visualizar, no se requiere para generar los videos
    return fig, animar
def grabarVideo(animacion,nombre_video):
        fig, animar = animacion
        animar.save(nombre_video,writer = 'ffmpeg',fps = 60, dpi = 100)
        plt.close(fig)
def unirVariosVideos(listaAnimaciones, listaVideos):
    # Primero, guardamos los videos de las animaciones
    for i, animacion in enumerate(listaAnimaciones):
        fig, animar = animacion
        animar.save(listaVideos[i], writer='ffmpeg', fps=60, dpi=100)
        plt.close(fig)  # Cierra la figura para liberar memoria

    # Ahora, preparamos para combinar los videos
    videos = []
    for video_path in listaVideos:
        videos.append(cv.VideoCapture(video_path))

    # Verifica que los videos se hayan abierto correctamente
    if not all(video.isOpened() for video in videos):
        print("Error al abrir uno o más videos")
        return

    # Configuración para el video combinado
    frame_width = int(videos[0].get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(videos[0].get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = videos[0].get(cv.CAP_PROP_FPS)
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video_combinado = cv.VideoWriter('video_final.mp4', fourcc, fps, (frame_width, frame_height))

    # Combinar los videos
    for video in videos:
        while True:
            ret, frame = video.read()
            if not ret:
                break
            video_combinado.write(frame)

    # Liberar todos los recursos de VideoCapture
    for video in videos:
        video.release()
    
    # Liberar el recurso del video combinado
    video_combinado.release()

    # Eliminar los archivos de video originales
    for video_path in listaVideos:
        os.remove(video_path)

    # Limpiar las listas
    listaAnimaciones.clear()
    listaVideos.clear()
def reproducirVideo(nombre_video):
    video = cv.VideoCapture(nombre_video)
    while True:
        ret, frame = video.read()
        if not ret:
            break
        cv.imshow('Video Final', frame)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    video.release()
    cv.destroyAllWindows()