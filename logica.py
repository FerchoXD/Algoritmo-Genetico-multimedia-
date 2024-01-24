import random
import numpy as np
import matplotlib.pyplot as plt
import os
from moviepy.editor import ImageSequenceClip
import re
import pandas as pd
import grabarPlots

def main():

    #datos estaticos para mayor facilidad de pruebas
    initial_poblation = 3
    max_poblation = 20
    generations_number = 100
    a = -5
    b = 5
    option = 'MAX'
    probability_individual = 0.9
    probability_gen = 0.9
    resolution = 0.0625

    r = b - a
    #calcula el nuemero de saltos para calcular los bits
    number_jumps = (r / resolution) +1
    n = 1
    while not (2*n - 1 <= number_jumps <= 2**n):
        n += 1
    bits = n
    delta_x = r/(2**bits-1)
    poblation = []
    stadistics = []
    generations = []
    for _ in range(initial_poblation):
        binario = ''.join(random.choice('01') for _ in range(bits))
        i = binary_to_decimal(binario)
        x = calculate_x(a, i, delta_x)
        individual = {
            "Individual": binario,
            "i": i,
            "x": x,
            "f(x)": calculate_fx(x)
        }
        poblation.append(individual)
        
    # Punto de Corte
    cross_point = 2
    
    #carga de poblacion inicial calcula el mejor y al resto de poblacion le aplica un punto de corte fijo
    for _ in range(generations_number):
        couples = []
        best_guy = get_best_individual(poblation, option)
        rest_of_population = [individuo for individuo in poblation if individuo != best_guy]
        for rest in rest_of_population:
            son1, son2 = cross_with_fixed_point(best_guy['Individual'], rest['Individual'], cross_point)
            couples.append(son1)
            couples.append(son2)

         #empieza la mutacion dependiendo la probability_individual o probability_gen   
        for i in range(len(couples)):
            individuo = couples[i]
            if (random.uniform(0,100)/100) <= probability_individual:
                individuo_mutado = ""
                for gen in individuo:
                    if (random.uniform(0,100)/100) <= probability_gen:
                        gen_mutado = '1' if gen == '0' else '0'
                    else:
                        gen_mutado = gen
                    individuo_mutado += gen_mutado
                couples[i] = individuo_mutado
        
        #actualiza los valores de las parejas obteniendo los demas valores x,el decimal, f(x)
        for couple in couples:
            decimal = binary_to_decimal(couple)
            x = calculate_x(a, decimal, delta_x)
            individual = {
                "Individual": couple,
                "i": decimal,
                "x": x,
                "f(x)": calculate_fx(x)
            }
            poblation.append(individual)
        if option == "MIN":
            poblation = sorted(poblation, key=lambda individuo: individuo["f(x)"])
        else:
            poblation = sorted(poblation, key=lambda individuo: individuo["f(x)"], reverse=True)
            
        # poblation ya ordenada y actualizada
        best_fx = poblation[0]["f(x)"]  # Valor de f(x) del mejor individuo
        worst_fx = poblation[-1]["f(x)"]  # Valor de f(x) del peor individuo
        average_fx = sum(individuo["f(x)"] for individuo in poblation) / len(poblation)
        # Crear el objeto JSON con los resultados
        results = {
            "Mejor f(x)": best_fx,
            "Peor f(x)": worst_fx,
            "Promedio f(x)": average_fx
        }
        stadistics.append(results)
        
        # Guardamos la generacion completa antes de la poda
        generations.append(poblation)
        
        unique_fx_values = set()
        population_without_duplicates = []
        for individuo in poblation:
            if individuo["f(x)"] not in unique_fx_values:
                population_without_duplicates.append(individuo)
                unique_fx_values.add(individuo["f(x)"])
        
        
        # PODA
        poblation = population_without_duplicates
        # Reducir el tamaño de la población si es necesario
        if len(poblation) > max_poblation:
            poblation = poblation[:max_poblation]
    
    # Extraer los valores de 'best_fx', 'worst_fx' y 'average_fx' de 'stadistics'
    best_fx = [resultado["Mejor f(x)"] for resultado in stadistics]
    worst_fx = [resultado["Peor f(x)"] for resultado in stadistics]
    average_fx = [resultado["Promedio f(x)"] for resultado in stadistics]

    # Asegúrate de que la longitud de 'generaciones' coincida con la longitud de estos arrays
    generaciones = range(1, len(stadistics) + 1)


    # Paso 1: Crear los videos de cada generación
    lista_animaciones = []
    lista_videos = []

    # Crear la carpeta 'graficas' si no existe
    carpeta_imagenes = 'graficas'
    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)
    # este for es el que itera por las generaciones y es el que me genera los sets de informacion
    for i, generation in enumerate(generations):
        #obtengo la lista de valores en X y Y para graficar
        x = [individuo["x"] for individuo in generation]
        y = [individuo["f(x)"] for individuo in generation]
        #  Crear la animación
        animacion = grabarPlots.animarPlot(x, y)
        #  Guardar la animación en un video
        nombre_video = f"video_generacion_{i+1}.mp4"
        grabarPlots.grabarVideo(animacion, nombre_video)
        # Guardar la animación y el nombre del video en listas
        lista_animaciones.append(animacion)
        lista_videos.append(nombre_video)

        print("Generacion: ", i+1)
        df = pd.DataFrame(generation)
        print(df)
        
        # Extraer los valores de 'x' y 'f(x)'
        valores_x = df['x']
        valores_fx = df['f(x)']

        # Identificar el mejor y el peor individuo
        mejor_x = df.iloc[0]['x']
        mejor_fx = df.iloc[0]['f(x)']
        peor_x = df.iloc[-1]['x']
        peor_fx = df.iloc[-1]['f(x)']

        # Crear la gráfica
        plt.figure(figsize=(10, 6))

        # Graficar todos los individuos excepto el mejor y el peor
        plt.scatter(valores_x[1:-1], valores_fx[1:-1], color='blue', label='Individuos')

        # Graficar el mejor y el peor individuo
        plt.scatter([mejor_x], [mejor_fx], color='green', label='Mejor', zorder=5)
        plt.scatter([peor_x], [peor_fx], color='red', label='Peor', zorder=5)
        plt.xlabel('Valor de x')
        plt.ylabel('f(x)')
        plt.title(f'Distribución de los Individuos de la Generación {i + 1}')
        plt.xlim(a, b)
        plt.legend()

        # Guardar la gráfica en la carpeta especificada
        nombre_archivo = f'generacion_{i + 1}.png'
        ruta_archivo = os.path.join(carpeta_imagenes, nombre_archivo)
        plt.savefig(ruta_archivo)
        plt.close()

    # Paso 2: Unir los vídeos
    grabarPlots.unirVariosVideos(lista_animaciones, lista_videos)

    # Paso 3: Reproducir o exportar el vídeo final
    grabarPlots.reproducirVideo("video_final.mp4")

    # Ruta a la carpeta donde se guardaron las imágenes
    carpeta_imagenes = './graficas'

    nombres_imagenes = [img for img in os.listdir(carpeta_imagenes) if img.endswith(".png")]
    nombres_imagenes_ordenados = sorted(nombres_imagenes, key=extraer_numero)
    rutas_imagenes = [os.path.join(carpeta_imagenes, img) for img in nombres_imagenes_ordenados]

    # Crear un clip de video a partir de las imágenes
    fps = 2  # Fotogramas por segundo, ajusta según sea necesario
    clip = ImageSequenceClip(rutas_imagenes, fps=fps)

    # Especificar el nombre del archivo de salida y guardar el video
    nombre_video = 'generaciones.mp4'
    clip.write_videofile(nombre_video)

    # Graficar los resultados
    plt.plot(generaciones, best_fx, label='Mejor f(x)', color='green')
    plt.plot(generaciones, worst_fx, label='Peor f(x)', color='red')
    plt.plot(generaciones, average_fx, label='Promedio f(x)', color='blue')
    plt.xlabel('Generación')
    plt.ylabel('f(x)')
    plt.title('Evolución de f(x) a lo largo de las generaciones')
    plt.legend()
    plt.show()
    
        
def calculate_x(a, i, delta_x):
    """
    Regresa el valor de x dependiendo de la posicion de i y usando delta_x
    """
    return a + i * delta_x  # Corregir aquí, i es un índice, no una función

def calculate_fx(x):
    """
    Regresa el valor de f(x) usando la formula
    NOTA: Aca se tiene que modificar la formula
    """
    return np.sin(x**2)
    #return np.sin(x) * np.cos(x) * np.log(1 + np.abs(x) ** 7/5)
    #return 6 * np.log(0.1 + np.abs(x)**3) + np.cos(x**2)
    #return np.sin(x) + np.sin(3 * x) / 3 + np.sin(5 * x) / 5

def binary_to_decimal(binario):
    """
    Funcion para transformar un binario a decimal
    """
    return int(binario, 2)

def get_best_individual(poblation, option):
    if option == "MIN":
        return min(poblation, key=lambda individuo: individuo["f(x)"])
    else:
        return max(poblation, key=lambda individuo: individuo["f(x)"])

def cross_with_fixed_point(individuo1, individuo2, cross_point):
    new_individuo1 = individuo1[:cross_point] + individuo2[cross_point:]
    new_individuo2 = individuo2[:cross_point] + individuo1[cross_point:]
    return new_individuo1, new_individuo2

def extraer_numero(archivo):
    numeros = re.findall(r'\d+', archivo)
    return int(numeros[0]) if numeros else 0

main()