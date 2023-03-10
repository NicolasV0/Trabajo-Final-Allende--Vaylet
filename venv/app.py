import time 
import os
import math
import json
from http import HTTPStatus
from flask import Flask,jsonify, Response, request



with open("usuarios.json") as archivo:
    dic_usuarios = json.load(archivo)
    
with open("peliculas.json") as file:
    dic_peliculas = json.load(file)
    
    
app = Flask(__name__)
    
@app.route("/")
def hello_world():
    return "<p>Sesion Iniciada</p>"
######## ENDPOINTS######################################################################
@app.route("/main")
def main():
    imprimir_menu()
    while(True):
        in_menu = menu_usuarios()
        if in_menu == 1:
            usuario = iniciar_sesion()
            sesion_iniciada(usuario)
            return Response({'Sesion finalizada'}, HTTPStatus.OK)
        elif in_menu == 2:
            modo_libre()
            return Response({"peliculas modo libre"}, HTTPStatus.OK) 
           
@app.route("/directores")
def directores():
    list_direc =[]
    print("Directores disponibles en nuestra plataforma: ")
    for pelis in dic_peliculas["peliculas"]:
        list_direc.append(pelis['director']) 
    conjunto = set(list_direc)
    list_direc = list(conjunto)
    for directores in list_direc:            
        print(directores)
        print('------------------------------')
    return jsonify(list_direc)

@app.route("/directores/<director>")
def peli_director(director):
    cont = 0
    pelis_director =[]
    print(director)
    print("Peliculas disponibles para "+director+" en nuestra plataforma: ")
    for pelis in dic_peliculas["peliculas"]:
        if director == pelis['director']:        
            pelis_director.append(pelis['titulo'])
            pelis_director.append(pelis['imagen']) 
    if pelis_director == []:
        print('No encontramos a este director en nuestro catalogo')
        return Response('No encontramos a este director en nuestro catalogo', HTTPStatus.NOT_FOUND)
    for directores in pelis_director:
        cont = cont + 1            
        print(directores)
        if cont%2 == 0:
            print('------------------------------')
    return jsonify(pelis_director)

@app.route("/generos")
def generos():
    list_generos =[]
    print("Generos disponibles en nuestra plataforma: ")
    for pelis in dic_peliculas["peliculas"]:
        list_generos.append(pelis['genero']) 
    conjunto = set(list_generos)
    list_generos = list(conjunto)
    for genero in list_generos:            
        print(genero)
        print('------------------------------')
    return jsonify(list_generos)

@app.route("/peliculas/portada")
def portada():
    cont = 0
    peliculas_portada =[]
    print("Peliculas con portada disponibles en nuestra plataforma: ")
    for pelis in dic_peliculas["peliculas"]:
        if pelis['imagen'] != []:
            peliculas_portada.append(pelis['titulo']) 
            peliculas_portada.append(pelis['imagen'])
    if peliculas_portada ==[]:
        print('Ninguna pelicula cargada tiene imagen de portada')
        return Response({'Ninguna pelicula cargada tiene imagen de portada'}, HTTPStatus.NO_CONTENT) 
    for portada in peliculas_portada:            
        cont = cont +1
        print(portada)
        if cont%2 == 0:
            print('------------------------------')
    return jsonify(peliculas_portada)
###############################ABM PELICULAS###########################################

@app.route("/peliculas/agregar" , methods=["PUT"])
def agregar_pelicula():
    try:
        pelicula = request.get_json()
        for pelis in dic_peliculas["peliculas"]:
            if pelis["titulo"].lower() == pelicula["titulo"].lower():
                return Response({'Pelicula ya agregada'}, HTTPStatus.ALREADY_REPORTED)
        dic_peliculas["peliculas"].append({
            "titulo": pelicula["titulo"],
            "anio": pelicula["anio"],
            "director": pelicula["director"],
            "genero": pelicula["genero"],
            "sinopsis": pelicula["sinopsis"],
            "imagen": pelicula["imagen"],
            "comentarios": pelicula["comentarios"]
        })
        with open("peliculas.json", 'w') as file:
            json.dump(dic_peliculas, file, indent=4)
        return Response({"Pelicula cargada "}, HTTPStatus.OK)        
    except:
        return Response({"Error en datos ingresados"}, HTTPStatus.BAD_REQUEST)  

@app.route("/peliculas/modificar/<pelicula>" , methods=["PUT"])
def modificar_pelicula(pelicula):
    try:
        j_pelicula = request.get_json()
        for pelis in dic_peliculas["peliculas"]:
            if pelis["titulo"].lower() == pelicula.lower():
                pelis['titulo'] = j_pelicula['titulo']
                pelis['anio'] = j_pelicula['anio']
                pelis['director'] = j_pelicula['director']
                pelis['genero'] = j_pelicula['genero']
                pelis['sinopsis'] = j_pelicula['sinopsis']
                pelis['imagen'] = j_pelicula['imagen']
                with open("peliculas.json", 'w') as file:
                    json.dump(dic_peliculas, file, indent=4)
                return Response({"Pelicula modificada "}, HTTPStatus.OK)  
        return Response({'Pelicula no encontrada'}, HTTPStatus.NOT_FOUND)                
    except:
        return Response({"Error en datos ingresados"}, HTTPStatus.BAD_REQUEST) 

@app.route("/comentarios/borrar/<pelicula>" , methods=["DELETE"])
def borrar_comentarios(pelicula):
    comentario = request.get_json()
    for pelis in dic_peliculas["peliculas"]:
        if pelis["titulo"].lower() == pelicula.lower():
            for llaves in pelis['comentarios']:
                print(llaves)
                if llaves == comentario['comentarios']:
                    print(llaves)
                    pelis['comentarios'].pop(llaves)
                    with open("peliculas.json", 'w') as file:
                        json.dump(dic_peliculas, file, indent=4)
                    return Response({"Comentario borrado"}, HTTPStatus.ACCEPTED)
                
            return Response({'Comentario no encontrado'}, HTTPStatus.NOT_FOUND)
    return Response({'Pelicula no encontrada'}, HTTPStatus.NOT_FOUND)

@app.route("/peliculas/borrar" , methods=["DELETE"])
def borrar_pelicula():
    cont = 0
    try:
        pelicula = request.get_json()
        for pelis in dic_peliculas["peliculas"]:
            cont = cont + 1
            if pelis["titulo"].lower() == pelicula["titulo"].lower():
                dic_peliculas['peliculas'].pop(cont -1)
                with open("peliculas.json", 'w') as file:
                    json.dump(dic_peliculas, file, indent=4)
                print('Pelicula borrada...')
                return Response({'Pelicula eliminada correctamente'}, HTTPStatus.ACCEPTED) 
        return Response({'Pelicula no encontrada'}, HTTPStatus.NOT_FOUND)                
    except:
        return Response({"Error en datos ingresados"}, HTTPStatus.BAD_REQUEST) 

@app.route("/peliculas/puntuacion/<pelicula>", methods=["GET"])
def puntuar_pelicula(pelicula):
    print (pelicula)
    cont = 0
    suma = 0
    for pelis in dic_peliculas["peliculas"]:
        if pelis["titulo"].lower() == pelicula.lower():
            for llave, valor in pelis['puntuacion'].items():
                cont = cont + 1
                suma = suma + valor
                print(f"{llave}: {valor}")    
            print(f'* {suma/cont: .2f}')
            return Response({"Puntuaciones"}, HTTPStatus.ACCEPTED)
    
    return Response({"No encontrada"}, HTTPStatus.NOT_FOUND)

#################################################################################
#################### MENU INICIO SESION #####################################    
def menu_usuarios():
    while(True):
        print('+--------------------------+')
        print('|                          |')
        print('|1)   Inicie sesion        |')
        print('|2)   Modo libre           |')
        print('|                          |')
        print('+--------------------------+')
        try:
            in_menu = int(input())
            if (in_menu != 1) and (in_menu !=2):
                print('Error... Ingrese 1 o 2')
                time.sleep(1)
                os.system('cls')
            elif (in_menu == 1 or in_menu == 2):
                return in_menu
        except:
            print('Error... Ingrese 1 o 2')
            time.sleep(1)
            os.system('cls')
            menu_usuarios()
                    
#################### MENU PRINCIPAL #####################################    
def imprimir_menu():
    print('\033[0;31m' +'+--------------------------------------------------------------+'+'\033[0;m')
    print('\033[0;31m' +'|                                                              |'+'\033[0;m')
    print('\033[0;31m' +'|       N    N  NNNNN  NNNNN  NNNNN  N      NNNNN  N   N       |'+'\033[0;m')
    print('\033[0;31m' +'|       NN   N  N        N    N      N      N   N   N N        |'+'\033[0;m')
    print('\033[0;31m' +'|       N N  N  NNN      N    NNN    N      N   N    N         |'+'\033[0;m')
    print('\033[0;31m' +'|       N  N N  N        N    N      N      N   N   N N        |'+'\033[0;m')
    print('\033[0;31m' +'|       N   NN  NNNNN    N    N      NNNNN  NNNNN  N   N       |'+'\033[0;m')
    print('\033[0;31m' +'|                                                              |'+'\033[0;m')
    print('\033[0;31m' +'+--------------------------------------------------------------+'+'\033[0;m')
    time.sleep(2 )
    os.system('cls')      
    return

#########################INICIAR SESION##################################
def iniciar_sesion():
    while (True):
        flag = False
        usuario = input('Ingrese Nombre y Apellido: ')
        try:
            contrase??a = int(input('Ingrese Contrase??a: '))
        except:
            print('Error de dato, vuelva a intentarlo')
            flag = True
            continue    
        for us in dic_usuarios['usuarios']:    
            if us['Nombre y Apellido'].lower() == usuario.lower():
                if us['contrasenia'] == contrase??a:
                    print('Has iniciado sesion')
                    return us['Nombre y Apellido']
                else:
                    print('Contrasenia incorrecta')
                    flag = True
                    continue
        if flag == False:            
            print('Usuario inxistente')
        print('1) Para Menu de inicio')
        print('2) Para modo libre')
        print('3) Para volver a intentar')
        print('4) Para cerrar')
        opcion = int(input('Como desea continuar: '))
        if opcion == 1:
            os.system('cls')      
            return
        if opcion == 2:
            modo_libre()
            print('modo libre')
            exit(1)
        if opcion == 3:
            os.system('cls')
            continue
        if opcion == 4:
            break


def sesion_iniciada(usuario):
    opcion= 0
    continuar=""
    print('Bienvenido ' ,usuario)
    time.sleep(1)
    while(opcion!= 8):
        os.system('cls')
        print('+-------------------------------------+')
        print('|                                     |')
        print('|1)Peliculas disponibles              |')    
        print('|2)Buscar Titulo                      |')
        print('|3)Buscar Titulos por primera letra   |')    
        print('|4)Buscar Director                    |')    
        print('|5)Buscar Genero                      |')
        print('|6)Comentarios                        |')
        print('|7)Ver comentarios                    |')                
        print('|8)Borrar pelicula                    |')
        print('|9)Editar pelicula                    |')
        print('|10)Puntuar pelicula                  |')
        print('|11)Cerrar sesion                     |')             
        print('|                                     |')
        print('+-------------------------------------+')    
        opcion = int(input('??Que desea realizar? '))
        if opcion >=12 or opcion <=0:
            print('Error seleccion invalida...')
            time.sleep(1)
            continue
        elif opcion == 1:
            cont = 0
            pag_actual = 1
            cant_pelic = len(dic_peliculas['peliculas'])
            paginas_totales = math.trunc(cant_pelic/5)
            if cant_pelic % 5 > 0:
                paginas_totales = paginas_totales + 1
            print (paginas_totales)    
            for pelis in dic_peliculas['peliculas']:
                cont = cont + 1
                print ('Pelicula:',pelis['titulo'])
                print('Link imagen:',pelis['imagen'])
                if cont == 5:
                    print ('Pagina ('+ str(pag_actual) +'/'+ str(paginas_totales)+')')
                    pag_actual = pag_actual + 1
                    continuar = input('Presione una tecla para continuar...')
                    cont = 0
                    os.system('cls')    
            
                    
            while(True):
                continuar= input('Presione Enter para continuar...')
                if continuar != "":    
                    print('Error, presione enter')
                else:
                    break
                
        elif opcion ==2:
            flag = False
            buscar_peli = input('??Que pelicula desea buscar?: ')
            for pelis in dic_peliculas['peliculas']:
                if buscar_peli.lower() in pelis['titulo'].lower() :
                    flag = True
                    print('Hemos encontrado esto para ti: \n')
                    print("Pelicula:",pelis['titulo'])
                    print('anio:',pelis['anio'])
                    print('Link imagen:',pelis['imagen'])
                    print('Director:',pelis['director'])
                    print('Genero:',pelis['genero'])
                    print('Sinopsis:',pelis['sinopsis'])
                    while(True):
                        continuar= input('Presione Enter para continuar...')
                        if continuar != "":    
                            print('Error, presione enter')
                        else:
                            break
            if flag == False:
                print('Lo sentimos no hemos encontrado esa pelicula, prueba en Netflix...')
                time.sleep(2)
        
        elif opcion ==3:
            flag = False
            buscar_peli = input('??Que peliculas desea buscar que comience con la letra?: ')
            for pelis in dic_peliculas['peliculas']:
                if pelis['titulo'][0].lower() == buscar_peli.lower():
                    flag = True
                    print('Pelicula:',pelis['titulo'])
                    time.sleep(1)
            if flag == False:
                print('Lo sentimos no hemos encontrado peliculas que empiecen con '+buscar_peli+', prueba en Netflix...')
                time.sleep(1)
            while(True):
                        continuar= input('Presione Enter para continuar...')
                        if continuar != "":    
                            print('Error, presione enter')
                        else:
                            break
        
        elif opcion == 4:
            cont = 0
            flag = False
            buscar_director = input('??Que director desea buscar? ')
            for pelis in dic_peliculas['peliculas']:
                if buscar_director.lower() in pelis['director'].lower():
                    if cont == 0:
                        print('Para '+pelis['director']+' hemos encontrado los siguientes titulos: ')
                    else:
                         print('-----------------------------------')
                    print("Pelicula:",pelis['titulo'])
                    print('anio:',pelis['anio'])
                    print('Genero:',pelis['genero'])
                    print('Sinopsis:',pelis['sinopsis'])
                    cont = cont + 1
                    flag = True
            if flag == False:
                print('Lo sentimos no hemos encontrado a ese director en nuestro catalogo, mejor prueba en Netflix...')
                time.sleep(1)
            while(True):
                        continuar= input('Presione Enter para continuar...')
                        if continuar != "":    
                            print('Error, presione enter')
                        else:
                            break
        
        elif opcion == 5:
            flag = False
            cont = 0
            buscar_genero = input('??Que genero de peliculas desea buscar? ')
            for pelis in dic_peliculas['peliculas']:
                if buscar_genero.lower() in pelis['genero'].lower():
                    if cont == 0:
                        print('Peliculas de genero '+ pelis['genero'])
                    else:
                        print('-----------------------------------')
                    print("Pelicula:",pelis['titulo'])
                    print('anio:',pelis['anio'])
                    print('Director:',pelis['director'])
                    print('Sinopsis:',pelis['sinopsis'])
                    cont = cont + 1
                    flag = True
            if flag == False:
                print('Lo sentimos no hemos encontrado a ese genero en nuestro catalogo, mejor prueba en Netflix...')
                time.sleep(1)
            while(True):
                        continuar= input('Presione Enter para continuar...')
                        if continuar != "":    
                            print('Error, presione enter')
                        else:
                            break
                        
        elif opcion == 6:
            while(True):
                print("1)Realizar un comentario sobre alguna pelicula")
                print("2)Volver al menu anterior")
                opcion = int(input())
                if opcion >= 3 or opcion <=0:
                    print('Seleccion invalida')
                    continue
                if opcion == 2:
                    break
                else:
                    flag = False
                    flag_comentario = False
                    buscar_peli = input('??Sobre que pelicula desea hacer un comentario?: ')
                    for pelis in dic_peliculas['peliculas']:
                        if buscar_peli.lower() == pelis['titulo'].lower() :
                            for llaves in pelis['comentarios']:
                                if llaves == usuario:
                                    print('Ya hiciste un comentario sobre esa pelicula')
                                    modificar = input('??Desea modificarlo? (S/N)')
                                    if modificar == 's' or modificar=='S':
                                        break
                                    else:
                                        flag_comentario = True
                                        continue
                            if flag_comentario == True:
                                break
                            flag = True
                            print('Hemos encontrado esto para ti: \n')
                            print("Pelicula:",pelis['titulo'])
                            print('anio:',pelis['anio'])
                            print('Link imagen:',pelis['imagen'])
                            print('Director:',pelis['director'])
                            print('Genero:',pelis['genero'])
                            comentario = input('Comente aqui sobre la pelicula: ')
                            pelis['comentarios'].update({usuario:comentario})
                            with open("peliculas.json", 'w') as file:
                                json.dump(dic_peliculas, file, indent=4)
                            #    file.seek(0)                         
                            while(True):
                                continuar= input('Presione Enter para continuar...')
                                if continuar != "":    
                                    print('Error, presione enter')
                                else:
                                    break
                                if flag == False:
                                    print('Lo sentimos no hemos encontrado esa pelicula, prueba en Netflix...')
        
        elif opcion == 7:
            flag = False
            buscar_peli = input('??Que pelicula desea buscar?: ')
            for pelis in dic_peliculas['peliculas']:
                if buscar_peli.lower() in pelis['titulo'].lower() :
                    if pelis['comentarios'] == {}:
                        print("Pelicula:",pelis['titulo'])
                        print('Esta pelicula aun no tiene comentarios...')
                        time.sleep(2)
                        flag = True
                        break
                    flag = True
                    print('Hemos encontrado esto para ti: \n')
                    print("Pelicula:",pelis['titulo'])
                    print('anio:',pelis['anio'])
                    print('Link imagen:',pelis['imagen'])
                    print('Director:',pelis['director'])
                    print('Genero:',pelis['genero'])
                    print('Sinopsis:',pelis['sinopsis'])
                    print('Comentarios: ')
                    for llave, valor in pelis['comentarios'].items():
                        print(f"{llave}: {valor}")
                    while(True):
                        continuar= input('Presione Enter para continuar...')
                        if continuar != "":    
                            print('Error, presione enter')
                        else:
                            break
            if flag == False:
                print('Lo sentimos no hemos encontrado esa pelicula, prueba en Netflix...')
                time.sleep(2)
        
        elif opcion == 8:
            while(True):
                print('1)Eliminar una pelicula')    
                print('2)Volver')
                opcion = int(input())
                if opcion == 1:
                    cont = 0
                    peli_borrar = input('??Que pelicula desea borrar?: ')
                    for pelis in dic_peliculas['peliculas']:
                        cont = cont + 1
                        if peli_borrar.lower() == pelis['titulo'].lower(): 
                            if pelis['comentarios'] == {}:
                                dic_peliculas['peliculas'].pop(cont -1)
                                with open("peliculas.json", 'w') as file:
                                    json.dump(dic_peliculas, file, indent=4)
                                print('Pelicula borrada...')
                                cont = 0
                                time.sleep(2)
                                break
                    if cont == 0:
                        break
                    else:        
                        print('Esa pelicula tiene comentarios, no se puede borrar...')
                        time.sleep(2)
                    break
                elif opcion == 2:
                    break
                elif opcion<=0 or opcion >=3:
                    print('Vuelva a intentarlo...')    
        
        elif opcion == 9:
            while(True):
                flag = False
                print('1) Para editar una pelicula')
                print('2) Volver')
                opcion = int(input())
                if opcion == 1:
                    editar = input('Que pelicula desea editar: ')
                    for pelis in dic_peliculas['peliculas']:
                        if editar.lower() == pelis['titulo'].lower():
                            flag = True
                            print("1)Editar titulo:")
                            print("2)Editar anio:")
                            print("3)Editar director:")
                            print("4)Editar genero:")
                            print("5)Editar sinopsis:")
                            print("6)Editar imagen:")
                            op = int(input(''))
                            if op == 1:
                                cambiar = input('Ingrese nuevo titulo: ')
                                pelis['titulo'] = cambiar
                                with open("peliculas.json", 'w') as file:
                                    json.dump(dic_peliculas, file, indent=4)
                                print('Titulo cambiado exitosamente')
                                time.sleep(2)
                                break
                            elif op == 2:
                                cambiar = input('Ingrese nuevo anio: ')
                                pelis['anio'] = cambiar
                                with open("peliculas.json", 'w') as file:
                                    json.dump(dic_peliculas, file, indent=4)
                                print('Anio cambiado exitosamente')
                                time.sleep(2)
                                break
                            elif op == 3:
                                cambiar = input('Ingrese nuevo director: ')
                                pelis['director'] = cambiar
                                with open("peliculas.json", 'w') as file:
                                    json.dump(dic_peliculas, file, indent=4)
                                print('Director cambiado exitosamente')
                                time.sleep(2)
                                break
                            elif op == 4:
                                cambiar = input('Ingrese nuevo genero: ')
                                pelis['genero'] = cambiar
                                with open("peliculas.json", 'w') as file:
                                    json.dump(dic_peliculas, file, indent=4)
                                print('Genero cambiado exitosamente')
                                time.sleep(2)
                                break
                            elif op == 5:
                                cambiar = input('Ingrese nuevo sinopsis: ')
                                pelis['sinopsis'] = cambiar
                                with open("peliculas.json", 'w') as file:
                                    json.dump(dic_peliculas, file, indent=4)
                                print('Sinopsis cambiado exitosamente')
                                time.sleep(2)
                                break
                            elif op == 6:
                                cambiar = input('Ingrese nuevo imagen: ')
                                pelis['imagen'] = cambiar
                                with open("peliculas.json", 'w') as file:
                                    json.dump(dic_peliculas, file, indent=4)
                                print('Imagen cambiado exitosamente')
                                time.sleep(2)
                                break
                            elif op >= 7 or op <= 0:
                                print("Seleccion invalida")
                                continue             
                    if flag == False:
                        print('Pelicula no encontrada')
                        continue        
                                
                elif opcion ==2:
                    break
                elif opcion <= 0 or opcion >= 3:
                    print('Seleccione 1 o 2 ')
                    continue     
       
        elif opcion == 10:
            while (True):
                print ('1) Que pelicula desea puntuar? ')
                print ('2) Desea ver la puntuacion de una pelicula? ')
                print ('3) Salir.')
                opcion = int(input('Que tarea desea realizar? '))
                if opcion <= 0 or opcion >= 4:
                    print('Seleccion invalida')
                    continue
                elif opcion == 1:
                    flag = False
                    flag_puntuacion = False
                    buscar_peli = input('??Que pelicula desea puntuar?: ')
                    for pelis in dic_peliculas['peliculas']:
                        if buscar_peli.lower() in pelis['titulo'].lower() :
                            for llaves in pelis['puntuacion']:
                                if llaves == usuario:
                                    print('Ya hiciste una puntuacion sobre esa pelicula')
                                    modificar = input('??Desea modificarlo? (S/N)')
                                    if modificar == 's' or modificar=='S':
                                        break
                                    else:
                                        flag_puntuacion = True
                                        continue
                            if flag_puntuacion == True:
                                break
                            flag = True
                            print('Hemos encontrado esto para ti: \n')
                            print("Pelicula:",pelis['titulo'])
                            print('anio:',pelis['anio'])
                            print('Link imagen:',pelis['imagen'])
                            print('Director:',pelis['director'])
                            print('Genero:',pelis['genero'])
                            while(True):
                                puntuacion = int(input('Ingrese del 0-10 para puntuar la pelicula: '))
                                if puntuacion < 0 or puntuacion > 10:
                                    print('seleccion invalida')
                                break    
                            pelis['puntuacion'].update({usuario:puntuacion})
                            with open("peliculas.json", 'w') as file:
                                json.dump(dic_peliculas, file, indent=4)
                            #    file.seek(0)                         
                            while(True):
                                continuar= input('Presione Enter para continuar...')
                                if continuar != "":    
                                    print('Error, presione enter')
                                else:
                                    break
                                if flag == False:
                                    print('Lo sentimos no hemos encontrado esa pelicula, prueba en Netflix...')
                
                elif opcion == 2:
                    flag = False
                    buscar_peli = input('??Que pelicula desea buscar?: ')
                    for pelis in dic_peliculas['peliculas']:
                        if buscar_peli.lower() in pelis['titulo'].lower() :
                            if pelis['puntuacion'] == {}:
                                print("Pelicula:",pelis['titulo'])
                                print('Esta pelicula aun no tiene una puntuacion...')
                                time.sleep(2)
                                flag = True
                                break
                            flag = True
                            print('Hemos encontrado esto para ti: \n')
                            print("Pelicula:",pelis['titulo'])
                            print('anio:',pelis['anio'])
                            print('Link imagen:',pelis['imagen'])
                            print('Director:',pelis['director'])
                            print('Genero:',pelis['genero'])
                            print('Sinopsis:',pelis['sinopsis'])
                            print('Puntuacion: ')
                            for llave, valor in pelis['puntuacion'].items():
                                print(f"{llave}: {valor}")
                                while(True):
                                    continuar= input('Presione Enter para continuar...')
                                    if continuar != "":    
                                        print('Error, presione enter')
                                    else:
                                        break
                    if flag == False:
                        print('Lo sentimos no hemos encontrado esa pelicula, prueba en Netflix...')
                        time.sleep(2)
                    
                elif opcion == 3:
                    break   
        elif opcion == 11:
            while(True):
                cambiar_usuario = input('??Desea cerrar sesion? (S/N)')                    
                if cambiar_usuario == "s" or cambiar_usuario == "S":
                    print('Gracias! Recuerde que nuestro catalogo es mejor que el de la copia...')
                    time.sleep(2)
                    return
                elif cambiar_usuario == "n" or cambiar_usuario == "N":
                    break
                else:
                    print('Error ingrese S o N')
        
  
    
def modo_libre(): 
    empieza = len(dic_peliculas["peliculas"]) - 9
    cont = 0
    print('Hemos encontrado esto para ti: \n')
    for pelis in dic_peliculas["peliculas"]:
        cont += 1
        if cont >= empieza:
            print("Pelicula:",pelis['titulo'])
            print('anio:',pelis['anio'])
            print('Link imagen:',pelis['imagen'])
            print('Director:',pelis['director'])
            print('Genero:',pelis['genero'])
            print('Sinopsis:',pelis['sinopsis'])
            print("-------------------------") 
    return    