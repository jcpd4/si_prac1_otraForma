from a_estrella import *
def seleccionar_heuristica():
    print("Selecciona la heurística:")
    print("1. Trivial")
    print("2. Manhattan")
    print("3. Euclidiana")
    print("4. Chebyshev")
    
    #opcion = input("Introduce el número de la heurística que deseas usar: ")
    opcion = "2"
    
    if opcion == "1":
        return trivial_heuristica  # Asegúrate de que esta función esté implementada
    elif opcion == "2":
        return manhattan_heuristica
    elif opcion == "3":
        return euclidea_heuristica
    elif opcion == "4":
        return chebyshev_heuristica
    else:
        print("Opción no válida, usando heurística trivial por defecto.")
        return trivial_heuristica
