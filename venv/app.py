import time 
import os
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