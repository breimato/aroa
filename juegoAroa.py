import random


#esta funcion inicializa el tablero con colores aleatorios
def inicializar_tablero(filas=10, columnas=15):
    colores = ['r', 'g', 'b', ' ']
    tablero = [[random.choice(colores) for _ in range(columnas)] for _ in range(filas)]
    return tablero

#esta funcion muestra el tablero
def mostrar_tablero(tablero):
    # Este bucle 'for' recorre cada fila en el tablero
    for fila in tablero:
        # ' '.join(fila) convierte la lista 'fila' en una cadena, donde cada ficha en la fila se separa por un espacio
        # Luego, la función 'print' imprime esta cadena, mostrando una fila del tablero en la consola
        print(' '.join(fila))
    # Después de imprimir todas las filas del tablero, la función 'print' imprime una línea vacía para separar el tablero de cualquier salida posterior
    print()

def encontrar_grupos(tablero):
    # Inicializamos un conjunto para llevar un registro de las fichas que ya hemos visitado
    visitados = set()
    # Inicializamos una lista para almacenar los grupos de fichas del mismo color que encontramos
    grupos = []
    # Recorremos cada ficha en el tablero
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            # Si la ficha no ha sido visitada y no está vacía (es decir, su color no es ' ')
            if (i, j) not in visitados and tablero[i][j] != ' ':
                # Comenzamos a explorar el grupo de fichas del mismo color que incluye a esta ficha
                # Inicializamos una lista para almacenar las fichas de este grupo
                grupo = [(i, j)]
                # Inicializamos una pila con la ficha actual para comenzar la búsqueda en profundidad
                stack = [(i, j)]
                # Marcamos la ficha actual como visitada
                visitados.add((i, j))
                # Mientras la pila no esté vacía, continuamos explorando el grupo
                while stack:
                    # Sacamos una ficha de la pila
                    x, y = stack.pop()
                    # Para cada ficha adyacente a la ficha actual
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        # Calculamos las coordenadas de la ficha adyacente
                        #Por ejemplo, si la ficha actual está en las coordenadas (3, 4), y dx es -1 y dy es 0, entonces nx será 3 + (-1) = 2 y ny será 4 + 0 = 4.
                        # Por lo tanto, (nx, ny) será (2, 4), que son las coordenadas de la ficha que está directamente encima de la ficha actual en el tablero.
                        nx, ny = x + dx, y + dy
                        # Si la ficha adyacente está dentro del tablero, es del mismo color que la ficha actual, y no ha sido visitada
                        if (0 <= nx < len(tablero) and 0 <= ny < len(tablero[0]) and
                            tablero[nx][ny] == tablero[i][j] and (nx, ny) not in visitados):
                            # Añadimos la ficha adyacente a la pila para explorarla después
                            stack.append((nx, ny))
                            # Añadimos la ficha adyacente al grupo actual
                            grupo.append((nx, ny))
                            # Marcamos la ficha adyacente como visitada
                            visitados.add((nx, ny))
                # Cuando la pila está vacía, hemos terminado de explorar un grupo
                # Si el grupo contiene más de una ficha, lo añadimos a la lista de grupos
                if len(grupo) > 1:
                    grupos.append(grupo)
    # Devolvemos la lista de grupos
    return grupos

# La función eliminar_grupo toma dos argumentos: el tablero del juego y un grupo de fichas para eliminar
def eliminar_grupo(tablero, grupo):
    # El argumento grupo es una lista de duplas, donde cada dupla contiene las coordenadas de una ficha en el tablero
    # El bucle for recorre cada ficha en el grupo
    for i, j in grupo:
        # Para cada ficha en el grupo, establece la ficha en las coordenadas (i, j) del tablero a ' '
        # Esto es equivalente a "eliminar" la ficha del tablero, ya que ' ' representa una ficha vacía
        tablero[i][j] = ' '

def comprimir_tablero(tablero):
    # Recorremos cada columna en el tablero. 'range(len(tablero[0]))' genera una secuencia de números desde 0 hasta el número de columnas en el tablero.
    for j in range(len(tablero[0])):
        # Creamos una lista 'columna' que contiene todas las fichas en la columna actual.
        columna = [tablero[i][j] for i in range(len(tablero))]
        # Reordenamos la lista 'columna' de modo que todos los espacios vacíos (' ') estén al principio y las fichas restantes al final.
        columna = [' '] * columna.count(' ') + [c for c in columna if c != ' ']
        # Colocamos las fichas reordenadas de vuelta en la columna del tablero.
        for i in range(len(tablero)):
            tablero[i][j] = columna[i]
    # Finalmente, eliminamos las filas que están completamente vacías. 'any(c != ' ' for c in fila)' devuelve True si hay al menos una ficha no vacía en la fila.
    tablero = [fila for fila in tablero if any(c != ' ' for c in fila)]
    # Devolvemos el tablero comprimido.
    return tablero

def juego_terminado(tablero):
    # La función 'all' de Python devuelve True si todos los elementos del iterable (en este caso, una generador) son verdaderos.
    # El generador produce un valor True para cada ficha en el tablero que está vacía (es decir, su color es ' '), y False de lo contrario.
    # Por lo tanto, 'all(tablero[i][j] == ' ' for i in range(len(tablero)) for j in range(len(tablero[0])))' devuelve True si todas las fichas en el tablero están vacías, y False de lo contrario.
    return all(tablero[i][j] == ' ' for i in range(len(tablero)) for j in range(len(tablero[0])))

def obtener_entrada_usuario(grupos):
    # Iniciamos un bucle infinito. Este bucle continuará hasta que se encuentre un 'return' o se produzca una excepción.
    while True:
        # Solicitamos al usuario que introduzca las coordenadas de la ficha que quiere eliminar.
        entrada = input("Por favor, introduce las coordenadas de la ficha del grupo que quieres eliminar (formato: fila,columna): ")
        try:
            # Intentamos dividir la entrada del usuario en dos partes (fila y columna) y convertirlas en enteros.
            # Si la entrada del usuario no puede dividirse en dos partes o no puede convertirse en enteros, se producirá una excepción ValueError.
            fila, columna = map(int, entrada.split(','))
            # Recorremos cada grupo en la lista de grupos.
            for grupo in grupos:
                # Si las coordenadas introducidas por el usuario están en el grupo actual, devolvemos ese grupo y salimos de la función.
                if (fila, columna) in grupo:
                    return grupo
            # Si llegamos a este punto, significa que las coordenadas introducidas por el usuario no están en ninguno de los grupos.
            # Imprimimos un mensaje de error y volvemos al principio del bucle para solicitar una nueva entrada al usuario.
            print("No hay un grupo válido en las coordenadas proporcionadas. Por favor, inténtalo de nuevo.")
        except ValueError:
            # Si se produce una excepción ValueError (porque la entrada del usuario no pudo dividirse en dos partes o no pudo convertirse en enteros),
            # imprimimos un mensaje de error y volvemos al principio del bucle para solicitar una nueva entrada al usuario.
            print("Formato de entrada inválido. Por favor, introduce las coordenadas como dos números separados por una coma.")

def jugar():
    # Inicializa el tablero del juego llamando a la función 'inicializar_tablero'
    # Esta función devuelve una lista bidimensional que representa el tablero del juego,
    # y la asigna a la variable 'tablero'
    tablero = inicializar_tablero()

    # Entra en un bucle que se ejecuta mientras el juego no haya terminado
    # La función 'juego_terminado' comprueba si todas las fichas en el tablero están vacías
    # Si todas las fichas están vacías, el juego ha terminado y el bucle se detiene
    while not juego_terminado(tablero):

        # Muestra el estado actual del tablero llamando a la función 'mostrar_tablero'
        mostrar_tablero(tablero)

        # Encuentra todos los grupos de fichas del mismo color en el tablero llamando a la función 'encontrar_grupos'
        # Esta función devuelve una lista de grupos, donde cada grupo es una lista de fichas del mismo color
        # Asigna esta lista a la variable 'grupos'
        grupos = encontrar_grupos(tablero)

        # Si no hay grupos en el tablero, rompe el bucle y termina el juego
        if not grupos:
            break

        # Pide al usuario que introduzca las coordenadas de una ficha en el grupo que quiere eliminar
        # La función 'obtener_entrada_usuario' se encarga de obtener y validar la entrada del usuario
        # Esta función devuelve el grupo de fichas que el usuario quiere eliminar
        grupo = obtener_entrada_usuario(grupos)

        # Elimina el grupo de fichas seleccionado por el usuario del tablero llamando a la función 'eliminar_grupo'
        eliminar_grupo(tablero, grupo)

        # Comprime el tablero para llenar los espacios vacíos creados al eliminar el grupo de fichas
        # La función 'comprimir_tablero' se encarga de esto y devuelve el tablero comprimido
        tablero = comprimir_tablero(tablero)

    # Cuando el bucle termina, imprime un mensaje para indicar que el juego ha terminado
    print("¡Juego terminado!")

jugar()