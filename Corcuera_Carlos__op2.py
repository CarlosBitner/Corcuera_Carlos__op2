# -*- coding: utf-8 -*-
import time
import os
from pynput import keyboard as kb
import random
from playsound import playsound as pls

class Esclavo:
    def __init__(self,pos_x,pos_y,option):
        self.pos_x=pos_x
        self.pos_y=pos_y
        opciones={1:10,2:5,3:1}
        self.vida=opciones[option]
        self.gemas=0

    def limpiar_pos_actual(self,other):
        other.lista_matriz[self.pos_y][self.pos_x]="  "
        
    def posicionar(self,other):
        other.lista_matriz[self.pos_y][self.pos_x]="⛏ "
    
    def muerte(self,other):
        other.lista_matriz[self.pos_y][self.pos_x]="💥"

    def movimiento(self,other,a,b):
        global mostrar_bombas
        if other.lista_matriz[self.pos_y+a][self.pos_x+b] not in ["██","▓▓","▒▒","░░","║║","══"]:
            if other.lista_matriz[self.pos_y+a][self.pos_x+b] == "💣":
                self.vida-=1
            elif other.lista_matriz[self.pos_y+a][self.pos_x+b]=="🔹":
                self.gemas+=1
            elif other.lista_matriz[self.pos_y+a][self.pos_x+b]=="❤ ":
                self.vida+=1
            elif other.lista_matriz[self.pos_y+a][self.pos_x+b]=="🔦":
                mostrar_bombas=True
            self.limpiar_pos_actual(other)
            self.pos_x+=b
            self.pos_y+=a
            self.posicionar(other)
        else:
            pass
    
    def mover_derecha(self,other):
        self.movimiento(other,0,1)
    def mover_izquierda(self,other):
        self.movimiento(other,0,-1)
    def mover_arriba(self,other):
        self.movimiento(other,-1,0)
    def mover_abajo(self,other):
        self.movimiento(other,1,0)

    def picar(self,other,a,b):
        if other.lista_matriz[self.pos_y+a][self.pos_x+b] == "██":

            other.lista_matriz[self.pos_y+a][self.pos_x+b] = "▓▓"

        elif other.lista_matriz[self.pos_y+a][self.pos_x+b] == "▓▓":

            other.lista_matriz[self.pos_y+a][self.pos_x+b] = "▒▒"

        elif other.lista_matriz[self.pos_y+a][self.pos_x+b] == "▒▒":

            other.lista_matriz[self.pos_y+a][self.pos_x+b] = "░░"

        elif other.lista_matriz[self.pos_y+a][self.pos_x+b] == "░░":
            buff=random.randint(0,20)
            if buff==10:
                other.lista_matriz[self.pos_y+a][self.pos_x+b] = "🔦"
            elif buff == 5 or buff ==15:
                other.lista_matriz[self.pos_y+a][self.pos_x+b] = "❤ "
            else:
                other.lista_matriz[self.pos_y+a][self.pos_x+b] = "  "
        else:
            pass

    def picar_derecha(self,other):
        self.picar(other,0,1)
    def picar_izquierda(self,other):
        self.picar(other,0,-1)
    def picar_arriba(self,other):
        self.picar(other,-1,0)
    def picar_abajo(self,other):
        self.picar(other,1,0)

class Entorno:
    def __init__(self,numero_de_filas,numero_de_columnas):
        self.lista_matriz = []
        self.numero_de_filas=numero_de_filas
        self.numero_de_columnas=numero_de_columnas
        for i in range(numero_de_filas):
            self.lista_matriz.append([])
            for j in range(numero_de_columnas):
                self.lista_matriz[i].append(self.bloque())	
    def bloque(self):
        bloque = random.randint(1,20)
        if bloque==1:
            value ="🔹"
        elif bloque==7:
            value ="💣"
        elif bloque==5 or bloque==10 or bloque==15:
            value="██"
        else:
            value ="  "
        return value
        
    def enmarcar(self):
        for i in self.lista_matriz:
            i[0],i[self.numero_de_columnas-1] = "║║","║║"
        for j in range(self.numero_de_columnas):
            self.lista_matriz[0][j] = "══"
            self.lista_matriz[self.numero_de_filas-1][j] = "══"
        self.lista_matriz[0][0] = "╔╦"
        self.lista_matriz[0][self.numero_de_columnas-1] = "╦╗"
        self.lista_matriz[self.numero_de_filas-1][0] = "╚╩"
        self.lista_matriz[self.numero_de_filas-1][self.numero_de_columnas-1] = "╩╝"
        
    def graficar(self,flag):
        self.enmarcar()
        if flag:
            for i in self.lista_matriz:
                for k in i:
                    print(k,end = "")
                print("")
        else:
            for i in self.lista_matriz:
                for k in i:
                    if k=="💣":
                        print("  ",end = "")
                    else:
                        print(k,end = "")
                print("")
                
    def contar_diamantes(self):
        num_de_diamantes=0
        for i in self.lista_matriz:
            num_de_diamantes+=i.count("🔹")
        return num_de_diamantes

class Titulo:
	A=0
	def __init__(self,texto,espaciado,altura):
		self.texto = texto
		self.espaciado = espaciado
		self.altura = altura
		self.A = len(self.texto)+self.espaciado*2
	def __str__(self):
		str1 = ("╔"+"═"*self.A+"╗").center(70) + "\n"
		str2 = ("║"+" "*self.espaciado+self.texto+" "*self.espaciado + "║").center(70) + "\n"
		str3 = ("║"+" "*self.A+"║").center(70) + "\n"
		str4 = ("╚"+"═"*self.A+"╝").center(70) + "\n"
		return str1 + str3*(self.altura//2) + str2+str3*(self.altura//2)+ str4

title_menu = Titulo("BLIND MINER",3,3)
opcion_menu = Titulo("Presione Enter para iniciar", 0, 1)
Filas_de_prueba=21
Columnas_de_prueba=31
posx_inicial_esclavo=1
posy_inicial_esclavo=1
picar=0
niv_dificultad=1
estado=True
valor=True
prueba = Entorno(Filas_de_prueba,Columnas_de_prueba)
player=Esclavo(posx_inicial_esclavo,posy_inicial_esclavo,niv_dificultad)

def iniciar_juego():
	os.system("cls")
	input()

def pulsa(tecla):
    global estado,valor,picar
    if str(tecla) =="Key.enter":
        estado = False
    elif str(tecla) == "Key.esc":
        valor = False
    elif str(tecla) == "Key.space":
        picar=1
    elif str(tecla) == "Key.right":
        if picar ==0:
            player.mover_derecha(prueba)
        elif picar ==1:
            player.picar_derecha(prueba)
            picar=0
    elif str(tecla) == "Key.left":
        if picar ==0:
            player.mover_izquierda(prueba)
        elif picar==1:
            picar=0
            player.picar_izquierda(prueba)
            pass
    elif str(tecla) == "Key.up":
        if picar==0:
            player.mover_arriba(prueba)
        elif picar==1:
            player.picar_arriba(prueba)
            picar=0
            pass
    elif str(tecla) == "Key.down":
        if picar==0:
            player.mover_abajo(prueba)
        elif picar==1:
            player.picar_abajo(prueba)
            picar=0
            pass

def sonido_victoria():
    pls('C:/Users/Asus/Desktop/Ganar.mp3')

def sonido_derrota():
    pls('C:/Users/Asus/Desktop/Perder.mp3')

def Espaciado(entry):
    num_de_espacios=20
    espacio=" "
    texto=espacio*num_de_espacios
    a=num_de_espacios-len(entry)
    texto=entry+espacio*a
    return texto

def main():
    global prueba, player, mostrar_bombas,valor
    escuchador = kb.Listener(pulsa)
    escuchador.start()
    while(estado):
        print(title_menu)
        print(opcion_menu)
        time.sleep(0.9)
        os.system("cls")
        print(title_menu)
        print("\n\n\n")
        time.sleep(0.5)
        os.system("cls")
    iniciar_juego()
    
    game_over=True
    while game_over:
        niv_dificultad=0
        while niv_dificultad not in [1,2,3]:
	        niv_dificultad=int(input("Decida el nivel de dificultad del juego, eliga el número correspondiente:\n"+Espaciado("(1)Fácil")+"❤ x10"+"\n"+Espaciado("(2)Intermedio")+"❤ x5"+"\n"+Espaciado("(3)Difícil")+"❤ x1"+"\n"))
	        os.system("cls")
        prueba = Entorno(Filas_de_prueba,Columnas_de_prueba)
        prueba.graficar(True)
        print("Tiene 10 segundos para memorizar las posiciones de las bombas")
        print("No presione ninguna tecla")
        time.sleep(10)
        player=Esclavo(posx_inicial_esclavo,posy_inicial_esclavo,niv_dificultad)
        player.posicionar(prueba)
        print("Use las teclas para mover a su personaje")
        print("Para picar un bloque posicionese al lado de este,\nluego presione la tecla espacio y finalmente\nla dirección en la que se encuentra el bloque")
        print("Si quiere dejar de jugar presione la tecla escape")
        prueba.graficar(False)
        print("HP:","❤ "*(player.vida),end="        ")
        print("🔹x",str(player.gemas))
        valor=True
        mostrar_bombas=False
        while valor==True and prueba.contar_diamantes()>0 and player.vida>0:
            os.system("cls")
            print("Use las teclas para mover a su personaje")
            print("Si quiere dejar de jugar presione la tecla escape")
            print("Para picar un bloque posicionese al lado de este,\nluego presione la tecla espacio y finalmente\nla dirección en la que se encuentra el bloque")
            prueba.graficar(mostrar_bombas)
            print("HP:","❤ "*(player.vida),end="        ")
            print("🔹x",str(player.gemas))
            time.sleep(0.2)
    
        if prueba.contar_diamantes()==0:
            os.system("cls")
            title_victory=Titulo("Ganaste, has conseguido reunir todos los diamantes",1,1)
            print(title_victory,"\n\n\n")
            prueba.graficar(True)
            sonido_victoria()
        elif player.vida==0:
            os.system("cls")
            player.muerte(prueba)
            title_muerte=Titulo("☠  Has muerto ☠ ",1,1)
            print(title_muerte,"\n\n\n")
            prueba.graficar(True)
            sonido_derrota()
        decision=0
        while decision not in [1,2]:
            decision=int(input("¿Quiere empezar un nuevo juego?\nSí(1)\nNo(2)\n"))
            if decision==1:
                game_over=True
            else:
                game_over=False



if __name__ == "__main__":
    main()