# # # # # # # # # # # # # # # #	#
#         Tarea 1 - PDI         #
#  Alejandro Barone - 24206267  #
#                               #
#                               #
#        Imports y from'        # 
# # # # # # # # # # # # # # # # # 
import math

#Funcion 'main' carga una imagen con nombre 'entrada.bmp' y permite seleccionar opciones
def guardar_imagen(intento):
	print ("")
	# Cuando se hace input se trabaja con la imagen 'salida.bmp' (permitiendo seguir ejecutando acciones)
	if intento == 0:
		with open('entrada.bmp', 'rb') as f: #Abrir imagen
			data = bytearray(f.read())
			print("Se esta usando la imagen 'entrada.bmp'...")
	else:
		with open('salida.bmp', 'rb') as f: #Abrir imagen
			data = bytearray(f.read())
		print("Se esta usando la imagen 'salida.bmp'...")

	#Obtengo ancho y alto del arreglo de bytes
	ancho = int('{:08b}'.format(data[21])+'{:08b}'.format(data[20])+'{:08b}'.format(data[19])+'{:08b}'.format(data[18]),2)
	alto = int('{:08b}'.format(data[25])+'{:08b}'.format(data[24])+'{:08b}'.format(data[23])+'{:08b}'.format(data[22]),2)

	#Menu de interaccion
	print ("Imagen de %s bit(s)"%data[28])
	print ("Escoja una opcion:")
	print ("1: Negativo")
	print ("2: Invertir 270 grados derecha")
	print ("3: Invertir 270 grados izquierda")
	print ("4: Invertir 180 grados")
	print ("5: Invertir 90 grados izquierda")
	print ("6: Invertir 90 grados derecha")
	print ("7: Espejo vertical")
	print ("8: Espejo horizontal")
	print ("9: Salir")

	entrada = input()

	print ("")

	#Advertencia, el programa funciona aunque pueda trabarse un tiempo debido al peso o complejidad de una imagen
	print ("Si ves que se traba el programa no se preocupe, este esta trabajando!")

	#Llamadas a funciones pertinentes
	if entrada == '1':
		negativo(data)
	elif entrada == '3' or entrada == '5':
		invertir90(data,alto,ancho)
	elif entrada == '4':
		invertir180(data,alto,ancho)
	elif entrada == '2' or entrada == '6':
		invertir270(data,alto,ancho)
	elif entrada == '7':
		espejo_vertical(data,alto,ancho)
	elif entrada == '8':
		espejo_horizontal(data,alto,ancho)
	elif entrada == '9':
		print("Hasta luego")
	else:
		print("Entrada invalida")

# Funcion para obtener el negativo de una imagen
def negativo (data):
	#Condicional de que tipo es la imagen
	if(data[28] == 24):
		pos = 54 #Establezco posicion en 54 (inicio de datos de imagen para 24bits)
		#Por cada posicion resto 255 al valor actual
		for i in range(54,len(data)):
			data[i] = 255 - data[i]

	#Si la imagen es de 8 bits
	if(data[28] == 8):
		aux = 54 #A partir de este punto viene la "paleta" de colores
		for i in range(0,256):
			data[aux] = 255-data[aux]
			data[aux+1] = 255-data[aux+1]
			data[aux+2] = 255-data[aux+2]
			aux+=4

	#Si la imagen es de 4 bits
	if(data[28] == 4):
		# Como 2 pixeles estan hechos con 1 byte, para cambiar uno debo cambiar especificamente los 4 bits que quiero
		aux = 54
		paleta = [None]
		for i in range(54,70):
			data[aux] = 255-data[aux]
			data[aux+1] = 255-data[aux+1]
			data[aux+2] = 255-data[aux+2]
			aux+=4

	#Si la imagen es de 1 bits
	if(data[28] == 1):
		aux = 54
		#Cambio los RGB de la paleta, NO la paleta como tal
		for i in range(54,56):
			data[aux] = 255-data[aux]
			data[aux+1] = 255-data[aux+1]
			data[aux+2] = 255-data[aux+2]
			aux+=4

	# Creo la imagen con la data alterada
	with open('salida.bmp', 'wb') as f:
		f.write(data)

	guardar_imagen(1)

#Funcion para obtener la rotacion de 90 grados de una imagen
def invertir270(data,alto,ancho):
	#Swap de alto por ancho en la cabecera
	ancho1 = data[18]
	ancho2 = data[19]
	ancho3 = data[20]
	ancho4 = data[21]

	data[18] = data[22]
	data[19] = data[23]
	data[20] = data[24]
	data[21] = data[25]

	data[22] = ancho1
	data[23] = ancho2
	data[24] = ancho3
	data[25] = ancho4

	data_imagen2 = bytearray()
	data_2 = bytearray() 
	indice_alto = 1
	padding_referente = 0
	limite = 0
	if(data[28] == 24):
		data_imagen = data[54:len(data)] #Solo datos de imagen (para hacer los cambios)
		data_2[0:54] = data[0:54] 
		
		padding = sacar_padding24(ancho)
		padding_n = sacar_padding24(alto)

		indice_ancho = 3
		tam = len(data_imagen) + (ancho*padding_n) - (alto*padding)
		while (limite < tam):
			if (indice_alto == alto + 1):
				indice_alto = 1
				padding_referente = 0
				indice_ancho+=3
				for x in range(limite,padding_n+limite):
					data_imagen2.append(0)
				limite += padding_n
			else:
				temp = ((ancho * 3) * indice_alto) - indice_ancho + (padding * padding_referente)
				data_imagen2.append(data_imagen[temp])
				data_imagen2.append(data_imagen[temp + 1])
				data_imagen2.append(data_imagen[temp + 2])
				limite += 3
				padding_referente+=1
				indice_alto+=1

		data_2[54:len(data_imagen2)] = data_imagen2


	elif data[28] == 8:
		data_imagen = data[1078:len(data)] #Solo datos de imagen (para hacer los cambios)
		data_2[0:1078] = data[0:1078] 

		padding = sacar_padding8(ancho)
		padding_n = sacar_padding8(alto)

		indice_ancho = 1
		tam = len(data_imagen) + (ancho*padding_n) - (alto*padding)
		while (limite < tam):
			if (indice_alto == alto + 1):
				indice_alto = 1
				padding_referente = 0
				indice_ancho+=1
				for i in range(limite,limite+padding_n):
					data_imagen2.append(0)
				limite+= padding_n
			else:
				data_imagen2.append(data_imagen[(ancho * indice_alto) - indice_ancho + (padding * padding_referente)])
				limite+=1
				padding_referente+=1
				indice_alto+=1
		# data[1078:len(data)] = data_imagen2[0:len(data_imagen2)]

		data_2[1078:len(data_imagen2)] = data_imagen2

	elif data[28] == 4:
		#Parecido al de 90 solo que nunca toco el padding ya que nunca llego a ellos
		#Claramente empiezo en otra posicion el cambio de color
		data_imagen = data[118:len(data)] #Solo datos de imagen (para hacer los cambios)
		data_2[0:118] = data[0:118] 
		padding = sacar_padding4(ancho)
		padding_n = sacar_padding4(alto)

		pos = len(data_imagen)-padding-math.ceil((ancho/2))
		aux_arriba = pos
		primero = True
		guardado = 0
		limite = math.ceil(ancho/2)
		for i in range(0,(alto*ancho)):
			if(pos < limite):
				if(guardado == 0):
					if (primero):
						data_imagen2.append(data_imagen[pos]&240)
						primero = False
						guardado = 0
						pos = aux_arriba
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int((bits_auxiliar[4:8]+'0000'),2))
						primero = True
						aux_arriba = aux_arriba + 1
						guardado = 0
						pos = aux_arriba
				else:
					if(primero):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[0:4],2))
						primero = False
						guardado = 0
						pos = aux_arriba
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[4:8],2))
						primero = True
						aux_arriba = aux_arriba + 1
						guardado = 0
						pos = aux_arriba

				for j in range(0,padding_n):
					data_imagen2.append(0)

			else:
				if (guardado == 0):
					if (primero):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						bits = bits_auxiliar[0:4]
						pos = pos - padding - math.ceil(ancho/2)
						guardado = 1
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						bits = bits_auxiliar[4:8]
						pos = pos - padding - math.ceil(ancho/2)
						guardado = 1
				else:
					if (primero):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[0:4],2))
						pos = pos - padding - math.ceil(ancho/2)
						guardado = 0
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[4:8],2))
						pos = pos - padding - math.ceil(ancho/2)
						guardado = 0
			
		data_2[118:len(data_imagen2)] = data_imagen2
	
	else:
		#Parecido al de 90 solo que nunca toco el padding ya que nunca llego a ellos
		#Claramente empiezo en otra posicion el cambio de color
		data_imagen = data[62:len(data)] #Solo datos de imagen (para hacer los cambios)
		data_2[0:62] = data[0:62] 
		padding = sacar_padding1(ancho)
		padding_n = sacar_padding1(alto)
		pos = len(data_imagen)-padding-math.ceil((ancho/8))
		aux_arriba = pos
		guardado = 0
		limite = math.ceil(ancho/8)
		bits = ""
		primero = 0
		for i in range(0,(alto*ancho)):
			if(pos < limite):
				if(guardado <= 6):
					bits_auxiliar = '{:08b}'.format(data_imagen[pos])
					bits = bits+bits_auxiliar[primero]
					padding_auxiliar = ""
					for x in range(guardado+1,8):
						padding_auxiliar = padding_auxiliar + '0'

					data_imagen2.append(int((bits+padding_auxiliar),2))
					guardado = 0
					bits = ""
					primero +=1
				else:
					bits_auxiliar = '{:08b}'.format(data_imagen[pos])
					data_imagen2.append(int(bits+bits_auxiliar[primero],2))
					guardado = 0
					bits = ""
					primero +=1

				if (primero == 8):
					aux_arriba+=1
					primero = 0

				pos = aux_arriba
				for j in range(0,padding_n):
					data_imagen2.append(0)

			else:
				if (guardado <= 6):
					bits_auxiliar = '{:08b}'.format(data_imagen[pos])
					bits = bits+bits_auxiliar[primero]
					pos = pos - padding - math.ceil(ancho/8)
					guardado +=1
				else:
					bits_auxiliar = '{:08b}'.format(data_imagen[pos])
					data_imagen2.append(int(bits+bits_auxiliar[primero],2))
					pos = pos - padding - math.ceil(ancho/8)
					bits = ""
					guardado = 0
			
		data_2[62:len(data_imagen2)] = data_imagen2

	with open('salida.bmp', 'wb') as f:
		f.write(data_2)

	guardar_imagen(1)

#Funcion para obtener la rotacion de 180 grados de una imagen
def invertir180(data,alto,ancho):
	#Condicional que identifica el tipo de imagen
	if (data[28] == 24):
		#Saco el padding de la imagen
		padding = sacar_padding24(ancho)
		#Obtengo la mitad (para no cambiar mas pixeles)
		if (alto%2) == 0:
			limite = int(alto/2)
		else:
			limite = (int((alto/2))+1)
		pos = 54 #Pos inicial de datos
		aux = 54
		pos_arriba = len(data)-padding-1 #Pos final de datos (sin contar padding final)	
		if(alto%2 == 0):
			final = limite*(ancho)
		else:
			final = (limite*ancho) - int(ancho/2)

		#Bucle que cambiara primer y ultimo pixel (en bytes)
		for i in range(0,final):
			if(pos == aux+(ancho*3) and padding!=0): #Si hay padding los salto para no cambiarlos
				pos = pos + padding
				pos_arriba = pos_arriba - padding
				aux = pos
			#Cambio BGR pertinentes
			aux2_R = data[pos_arriba]
			aux2_G = data[pos_arriba-1]
			aux2_B = data[pos_arriba-2]
			data[pos_arriba] = data[pos+2]
			data[pos_arriba-1] = data[pos+1]
			data[pos_arriba-2] = data[pos]

			data[pos] = aux2_B
			data[pos+1] = aux2_G
			data[pos+2] = aux2_R

			pos = pos + 3
			pos_arriba = pos_arriba - 3

	elif (data[28] == 8):
		#Saco padding
		padding = sacar_padding8(ancho)
		#Saco el limite 
		if (alto%2) == 0:
			limite = int(alto/2)
			final = limite*(ancho)
		else:
			limite = int((alto/2)+1)
			final = limite*ancho - int(ancho/2)
		pos = 1078 #Posicion inicial de datos
		aux = 1078
		pos_arriba = len(data)-padding-1

		#Bucle que cambiara primer y ultimo pixel (en bytes)
		for i in range(0,final):
			if(pos == aux+ancho and padding!=0): #Si hay padding los salto
				pos = pos + padding
				pos_arriba = pos_arriba - padding
				aux = pos
			#Cambio pixeles pertinentes
			aux2 = data[pos_arriba]
			data[pos_arriba] = data[pos]
			data[pos] = aux2
			pos = pos + 1
			pos_arriba = pos_arriba - 1


	elif (data[28] == 4):
		#Saco padding y limite de ciclo

		if (ancho%2) == 0:
			ancho_nuevo = int(ancho/2)
			aux_padding = ((ancho_nuevo)/4)
			aux_padding = aux_padding - math.floor(aux_padding)
			if(aux_padding == 0.5):
				padding = 2
			elif (aux_padding == 0.25):
				padding = 3
			elif (aux_padding == 0.75):
				padding = 1
			else:
				padding = 0
			impar = False
		else:
			ancho_nuevo = int((ancho/2)+1) #Como en un byte hay dos pixeles debo cambiar cuentas
			aux_padding = (ancho_nuevo/4)
			aux_padding = aux_padding - math.floor(aux_padding)
			if(aux_padding == 0.5):
				padding = 2
			elif (aux_padding == 0.25):
				padding = 3
			elif (aux_padding == 0.75):
				padding = 1
			else:
				padding = 0
			impar = True

		pos = 118 #Posicion inicial de datos
		aux = 118
		pos_arriba = len(data)-1-padding 
		bits_auxiliar = ""

		#Si es impar siempre tendra un padding acompanando a un color final
		if(impar):
			while (pos < pos_arriba):
				if(pos == aux):
					#Primera posicion debo cambiar ese color que acompana al padding
					byte = '{:08b}'.format(data[pos]) 
					byte_final = '{:08b}'.format(data[pos_arriba])

					primer_cuarteto =  byte[0:4]
					segundo_cuarteto = byte_final[0:4]
					bits_auxiliar = byte[4:8]

					data[pos] = int(segundo_cuarteto+bits_auxiliar,2)
					data[pos_arriba] = int(primer_cuarteto+byte_final[4:8],2)

					pos+=1
					pos_arriba-=1

				elif(pos == aux+ancho_nuevo and padding!=0): #Llegue al final, me salto los paddings
					pos+=padding
					pos_arriba-=padding
					aux = pos

				else:
					#Cambio los 8 bits pertinentes
					byte = '{:08b}'.format(data[pos]) 
					byte_final = '{:08b}'.format(data[pos_arriba])
					byte_anterior = '{:08b}'.format(data[pos-1])
					primer_cuarteto_final = byte_final[0:4]
					segundo_cuarteto_final =  byte_final[4:8]

					primer_cuarteto = byte[0:4]
					segundo_cuarteto = byte[4:8]



					data[pos-1] = int((byte_anterior[0:4])+segundo_cuarteto_final,2)
					data[pos_arriba] = int(primer_cuarteto+bits_auxiliar,2)
					bits_auxiliar = byte[4:8]
					data[pos] = int(primer_cuarteto_final+bits_auxiliar,2)

					pos+=1
					pos_arriba-=1
		#Caso par
		else:
			while (pos < pos_arriba):
				if(pos == aux+ancho_nuevo and padding!=0): #Salto los paddings
					pos+=padding
					pos_arriba-=padding
					aux = pos

				else:
					#Cambio de bits pertinentes
					byte = '{:08b}'.format(data[pos]) 
					byte_final = '{:08b}'.format(data[pos_arriba])

					primer_cuarteto_final = byte_final[0:4]
					segundo_cuarteto_final =  byte_final[4:8]

					primer_cuarteto = byte[0:4]
					segundo_cuarteto = byte[4:8]

					data[pos_arriba] = int(segundo_cuarteto+primer_cuarteto,2)
					data[pos] = int(segundo_cuarteto_final+primer_cuarteto_final,2)

					pos+=1
					pos_arriba-=1


	# 1 Bit por pixel
	else:
		#Saco padding y limites
		if (ancho%8) == 0:
			ancho_nuevo = int(ancho/8)
			aux_padding = ((ancho_nuevo)/4)
			aux_padding = aux_padding - math.floor(aux_padding)
			if(aux_padding == 0.5):
				padding = 2
			elif (aux_padding == 0.25):
				padding = 3
			elif (aux_padding == 0.75):
				padding = 1
			else:
				padding = 0
			impar = False
		else:
			ancho_nuevo = int(ancho/8)+1 #Como en un byte hay 8 pixeles cambio mis datos
			aux_padding = (ancho_nuevo/4)
			aux_padding = aux_padding - math.floor(aux_padding)
			if(aux_padding == 0.5):
				padding = 2
			elif (aux_padding == 0.25):
				padding = 3
			elif (aux_padding == 0.75):
				padding = 1
			else:
				padding = 0
			impar = True
		pos = 62
		aux = 62
		pos_arriba = len(data)-1-padding
		ancho_aux = ancho
		while ancho_aux > 8: #Cantidad de pixeles(bits) que NO son padding en el byte final
			ancho_aux-=8 
		bits_auxiliar = ""
		#Si es impar siempre tendra un padding acompanando a un color final
		if(impar):
			while (pos<pos_arriba):
				if(pos == aux):
					#Primera posicion debo cambiar ese color que acompana al padding

					byte = '{:08b}'.format(data[pos]) 
					byte_final = '{:08b}'.format(data[pos_arriba])
					cambio = byte[0:ancho_aux]
					cambio_final = byte_final[0:ancho_aux]

					cambio = cambio[::-1]
					cambio_final = cambio_final[::-1]

					data[pos] = int(cambio_final+byte[ancho_aux:8],2)
					data[pos_arriba] = int(cambio+byte_final[ancho_aux:8],2)
					bits_auxiliar = byte[ancho_aux:8]

					pos+=1
					pos_arriba-=1

				elif(pos == aux+ancho_nuevo and padding!=0): #Salto paddings
					pos+=padding
					pos_arriba-=padding
					aux = pos

				else:
					# Cambio los bits pertinentes
					byte = '{:08b}'.format(data[pos]) 
					byte_final = '{:08b}'.format(data[pos_arriba])
					byte_anterior = '{:08b}'.format(data[pos-1])

					cambio = byte[0:ancho_aux]
					cambio_final =  byte_final[ancho_aux:8]

					cambio_final = cambio_final[::-1]
					cambio = cambio[::-1]
					bits_auxiliar = bits_auxiliar[::-1]

					data[pos-1] = int((byte_anterior[0:ancho_aux]+cambio_final),2)
					data[pos_arriba] = int((byte[0:ancho_aux])[::-1]+bits_auxiliar,2)
					bits_auxiliar = byte[ancho_aux:8]
					data[pos] = int((byte_final[0:ancho_aux])[::-1]+bits_auxiliar,2)

					pos+=1
					pos_arriba-=1		
		else:
			while(pos<pos_arriba):
				if(pos == aux+ancho_nuevo and padding!=0):
					pos+=padding
					pos_arriba-=padding
					aux = pos

				else:
					byte = '{:08b}'.format(data[pos]) 
					byte_final = '{:08b}'.format(data[pos_arriba])

					data[pos_arriba] = int((byte[0:ancho_aux])[::-1],2)
					data[pos] = int((byte_final[0:ancho_aux])[::-1],2)

					pos+=1
					pos_arriba-=1		

	# Creo la imagen
	with open('salida.bmp', 'wb') as f:
		f.write(data)

	guardar_imagen(1)

#Funcion para obtener la rotacion de 270 grados de una imagen
def invertir90(data,alto,ancho):
	#Swap de alto por ancho en la cabecera
	ancho1 = data[18]
	ancho2 = data[19]
	ancho3 = data[20]
	ancho4 = data[21]

	data[18] = data[22]
	data[19] = data[23]
	data[20] = data[24]
	data[21] = data[25]

	data[22] = ancho1
	data[23] = ancho2
	data[24] = ancho3
	data[25] = ancho4


	data_imagen2 = bytearray() #Bytearray vacio para crear la "nueva" imagen
	data_2 = bytearray() #Este byte array contendra toda la imagen
	indice_alto = alto
	padding_referente = 1
	limite = 0

	if(data[28] == 24):
		data_imagen = data[54:len(data)] #Solo datos de imagen (para hacer los cambios)
		data_2[0:54] = data[0:54]  #Voy guardando la cabecera en la nueva data
		
		#Saco paddings
		padding = sacar_padding24(ancho) 
		padding_n = sacar_padding24(alto)

		indice_ancho = ancho*3
		tam = len(data_imagen) + (padding_n*ancho) - (padding*alto)
		while (limite < tam):
			if (indice_alto == 0):
				indice_alto = alto
				padding_referente = 1
				indice_ancho-=3
				for x in range(limite,padding_n+limite):
					data_imagen2.append(0)
				limite += padding_n
			else:
				auxiliar = ((ancho * 3) * indice_alto) - indice_ancho + (padding * (alto - padding_referente))
				data_imagen2.append(data_imagen[auxiliar])
				data_imagen2.append(data_imagen[auxiliar + 1])
				data_imagen2.append(data_imagen[auxiliar + 2])
				limite += 3
				indice_alto-=1
				padding_referente+=1

		data_2[54:len(data_imagen2)] = data_imagen2

	elif data[28] == 8:
		data_imagen = data[1078:len(data)] #Solo datos de imagen (para hacer los cambios)
		data_2[0:1078] = data[0:1078] 

		padding = sacar_padding8(ancho)
		padding_n = sacar_padding8(alto)

		indice_ancho = ancho
		tam = len(data_imagen) + (ancho*padding_n) - (alto*padding)
		while (limite < tam):
			if (indice_alto == 0):
				indice_alto = alto
				padding_referente = 1
				indice_ancho-=1
				for i in range(limite,limite+padding_n):
					data_imagen2.append(0)
				limite+= padding_n
			else:
				data_imagen2.append(data_imagen[(ancho * indice_alto) - indice_ancho + (padding * (alto - padding_referente))])
				limite+=1
				padding_referente+=1
				indice_alto-=1
		
		data_2[1078:len(data_imagen2)] = data_imagen2

	elif data[28] == 4:
		data_imagen = data[118:len(data)] #Solo datos de imagen (para hacer los cambios)
		data_2[0:118] = data[0:118] 
		padding = sacar_padding4(ancho)
		padding_n = sacar_padding4(alto)

		pos = math.ceil(ancho/2) - 1 #Ultimo byte de la primera fila
		aux_arriba = pos
		primero = True #Si estoy parado en el primer cuarteto o en el segundo
		guardado = 0 #Cuantos bytes llevo guardado
		limite = len(data_imagen)-(math.ceil(ancho/2)+padding) #El maximo indice de la ultima fila (para no pasarme)
		if (ancho%2) != 0: #Si es impar el ancho tengo padding acompanando a un color, CP
			#Recorro todo el alto para "deshacerme" de esos bytes con padding
			for i in range(0,(alto)):
				#Llegue al ultimo byte en subida
				if(pos > limite):
					#Si no tengo algo guardado, guardo un "color"
					if(guardado == 0):
						data_imagen2.append(data_imagen[pos]&240)
						guardado = 0
						aux_arriba = aux_arriba - 1
						pos = aux_arriba
					#En caso de tener algo guardado, junto los colores en el nuevo byte
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[0:4],2))
						aux_arriba = aux_arriba - 1
						guardado = 0
						pos = aux_arriba

					#Agrego el padding correspondiente a la nueva imagen
					for j in range(0,padding_n):
						data_imagen2.append(0)
					break

				else:
					#Si no tengo algo guardado, guardo un "color"
					if (guardado == 0):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						bits = bits_auxiliar[0:4]
						pos = pos + padding + math.ceil(ancho/2)
						guardado = 1
					#En caso de tener algo guardado, junto los colores en el nuevo byte
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[0:4],2))
						pos = pos + padding + math.ceil(ancho/2)
						guardado = 0
			impar = alto #Variable que indica cuantas iteraciones se hicieron
		else:
			impar = 0
		#Guardo 4bits en 4bits (color por color ) segun corresponda para la imagen rotada
		for i in range(0,(alto*ancho)-impar): #Recorro la imagen quitandole ese pedazo que ya hice arriba
			#Igualmente, llegue al tope superior
			if(pos >= limite):
				
				if(guardado == 0):
				#Si estoy en el primer cuarteto no debo mover la posicion del byte, sino quedarme ahi y ir al otro cuarteto
					if (primero):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int((bits_auxiliar[4:8]+'0000'),2))
						primero = False
						guardado = 0
						pos = aux_arriba
				#No estoy en el primer cuarteto entonces me tengo que mover a la siguiente posicion del arreglo de bytes
					else:
						data_imagen2.append(data_imagen[pos]&240)
						primero = True
						aux_arriba = aux_arriba - 1
						guardado = 0
						pos = aux_arriba
				else:
				#Si estoy en el primer cuarteto no debo mover la posicion del byte, sino quedarme ahi y ir al otro cuarteto
					if(primero):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[4:8],2))
						primero = False
						guardado = 0
						pos = aux_arriba
				#No estoy en el primer cuarteto entonces me tengo que mover a la siguiente posicion del arreglo de bytes
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[0:4],2))
						primero = True
						aux_arriba = aux_arriba - 1
						guardado = 0
						pos = aux_arriba

				for j in range(0,padding_n):
					data_imagen2.append(0)
			#No he llegado al tope superior
			else:
				if (guardado == 0):
					if (primero):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						bits = bits_auxiliar[4:8]
						pos = pos + padding + math.ceil(ancho/2)
						guardado = 1
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						bits = bits_auxiliar[0:4]
						pos = pos + padding + math.ceil(ancho/2)
						guardado = 1
				else:
					if (primero):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[4:8],2))
						pos = pos + padding + math.ceil(ancho/2)
						guardado = 0
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[0:4],2))
						pos = pos + padding + math.ceil(ancho/2)
						guardado = 0
		
		data_2[118:len(data_imagen2)] = data_imagen2 #Guardo la data de imagen

	else:
		data_imagen = data[62:len(data)] #Solo datos de imagen (para hacer los cambios)
		data_2[0:62] = data[0:62] 
		padding = sacar_padding1(ancho)
		padding_n = sacar_padding1(alto)
		pos = math.ceil(ancho/8) - 1 #Me ubico en el ultimo byte de la primera fila
		aux_arriba = pos
		guardado = 0
		limite = len(data_imagen)-(math.ceil(ancho/8)+padding) #Maximo indice de la ultima fila
		bits = ""
		ancho_aux = ancho
		while ancho_aux > 8: #Cantidad de pixeles(bits) que NO son padding en el byte final
			ancho_aux-=8 
		primero = ancho_aux - 1 #Posicion donde empiezan los colores de ese byte con color-padding
		if (ancho%8) != 0: 
			for i in range(0,(alto*ancho_aux)):
				if(pos >= limite):
					#Si he guardado menos bits de lo necesario para tener un byte
					if(guardado <= 6):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						bits = bits+bits_auxiliar[primero]
						padding_auxiliar = ""
						#Agrego los padding referentes para completar ese byte
						for x in range(guardado+1,8):
							padding_auxiliar = padding_auxiliar + '0'

						data_imagen2.append(int((bits+padding_auxiliar),2))
						guardado = 0
						bits = ""
						primero-=1 #Decremento para estar agarrar los otros colores
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[primero],2))
						guardado = 0
						bits = ""
						primero-=1

					pos = aux_arriba
					for j in range(0,padding_n):
						data_imagen2.append(0)
				else:
					#Si he guardado menos bits de lo necesario para tener un byte
					if (guardado <= 6):
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						bits = bits+bits_auxiliar[primero]
						pos = pos + padding + math.ceil(ancho/8)
						guardado += 1
					else:
						bits_auxiliar = '{:08b}'.format(data_imagen[pos])
						data_imagen2.append(int(bits+bits_auxiliar[primero],2))
						pos = pos + padding + math.ceil(ancho/8)
						guardado = 0
						bits = ""

			impar = alto*ancho_aux #Valor que indica cuantas iteraciones hice
			aux_arriba-=1 #Como termine con este byte debo restarle uno a la posicion del arreglo 
			pos = aux_arriba
		else:
			impar = 0
		primero = 7 #A partir de aqui todos los bytes tendran 8 bits de color asi que primero es la posicion final
		#Guardo bit a bit (colo por color) en las posiciones que corresponden para tener la imagen volteada
		for i in range(0,(alto*ancho)-impar):
			if(pos >= limite):
				if(guardado <= 6):
					bits_auxiliar = '{:08b}'.format(data_imagen[pos])
					bits = bits+bits_auxiliar[primero]
					padding_auxiliar = ""
					for x in range(guardado+1,8):
						padding_auxiliar = padding_auxiliar + '0'

					data_imagen2.append(int((bits+padding_auxiliar),2))
					guardado = 0
					bits = ""
					primero -=1
				else:
					bits_auxiliar = '{:08b}'.format(data_imagen[pos])
					data_imagen2.append(int(bits+bits_auxiliar[primero],2))
					guardado = 0
					bits = ""
					primero -=1

				if (primero == -1):
					aux_arriba -= 1
					primero = 7

				pos = aux_arriba
				for j in range(0,padding_n):
					data_imagen2.append(0)

			else:
				if (guardado <= 6):
					bits_auxiliar = '{:08b}'.format(data_imagen[pos])
					bits = bits+bits_auxiliar[primero]
					pos = pos + padding + math.ceil(ancho/8)
					guardado +=1
				else:
					bits_auxiliar = '{:08b}'.format(data_imagen[pos])
					data_imagen2.append(int(bits+bits_auxiliar[primero],2))
					pos = pos + padding + math.ceil(ancho/8)
					bits = ""
					guardado = 0
			
		data_2[62:len(data_imagen2)] = data_imagen2


	with open('salida.bmp', 'wb') as f:
		f.write(data_2)

	guardar_imagen(1)

#Funcion para obtener el espejo vertical de una imagen
def espejo_vertical (data,alto,ancho):
	#Condicional que indica que tipo de imagen es
	if (data[28] == 24):
		#Saco el padding de la imagen
		padding = sacar_padding24(ancho)

		#Obtengo la mitad (para no cambiar mas pixeles)
		if (alto%2) == 0:
			limite = 0
		else:
			limite = 1
		pos = 54 #Pos inicial de datos
		aux_arriba = len(data)-padding-(ancho*3) #Pos inicial de la ultima fila
		#Ciclo que representa el cambio de toda una fila con otra (empezando en primero y ultimo)
		for i in range(0,int((alto/2))-limite):
			swap = data[pos:(pos+(ancho*3)-1)]
			data[pos:(pos+(ancho*3)-1)] = data[aux_arriba:(aux_arriba+(ancho*3)-1)]
			data[aux_arriba:(aux_arriba+(ancho*3)-1)] = swap

			pos = pos+(ancho*3)+padding
			aux_arriba = aux_arriba-(ancho*3)-padding


	elif (data[28] == 8):
		#Saco padding
		padding = sacar_padding8(ancho)
		#Saco el limite 
		pos = 1078 #Posicion inicial 
		aux_arriba = len(data)-padding-ancho #Posicion inicial de la ultima fila
		print(len(data))
		while (pos<aux_arriba):
			swap = data[pos:pos+(ancho)]
			data[pos:pos+(ancho)] = data[aux_arriba:aux_arriba+(ancho)]
			data[aux_arriba:aux_arriba+(ancho)] = swap

			pos = pos+(ancho)+padding
			aux_arriba = aux_arriba-(ancho)-padding

	# 4 bits por pixel		
	elif (data[28] == 4):
		#Saco padding y limites
		if (alto%2) == 0:
			limite = 0
		else:
			limite = 1

		if (ancho%2) == 0:
			impar = 0
		else:
			impar = 1

		padding = sacar_padding4(ancho)

		pos = 118 #Posicion inicial de datos
		pos_arriba = len(data)-padding-math.ceil((ancho/2)) #Posicion del ultimo primer byte final
		aux_arriba = pos_arriba
		#Si es impar siempre tendra un padding acompanando a un color final
		if(impar==1):
			#Ciclo que representa el cambio de toda una fila con otra (empezando en primero y ultimo)
			for i in range(0,int((alto/2))+limite):
				swap = data[pos:(pos+int(ancho/2))]
				data[pos:(pos+int(ancho/2))] = data[aux_arriba:(aux_arriba+int(ancho/2))]
				data[aux_arriba:(aux_arriba+int(ancho/2))] = swap

				pos = pos+int(ancho/2)+padding+1
				aux_arriba = aux_arriba-int(ancho/2)-padding-1
		else:
			#Ciclo que representa el cambio de toda una fila con otra (empezando en primero y ultimo)
			for i in range(0,int((alto/2))+limite):
				swap = data[pos:(pos+int(ancho/2))]
				data[pos:(pos+int(ancho/2))] = data[aux_arriba:(aux_arriba+int(ancho/2))]
				data[aux_arriba:(aux_arriba+int(ancho/2))] = swap

				pos = pos+int(ancho/2)+padding
				aux_arriba = aux_arriba-int(ancho/2)-padding

	# Caso de 1 bit por imagen
	else:
		#Saco padding y limites
		if (alto%2) == 0:
			limite = int(alto/2)
		else:
			limite = int((alto/2)+1)

		if (ancho%8) == 0:
			ancho_nuevo = int(ancho/8)
			aux_padding = ((ancho_nuevo)/4)
			aux_padding = aux_padding - math.floor(aux_padding)
			if(aux_padding == 0.5):
				padding = 2
			elif (aux_padding == 0.25):
				padding = 3
			elif (aux_padding == 0.75):
				padding = 1
			else:
				padding = 0
			impar = 1
		else:
			ancho_nuevo = int((ancho/8)+1)
			aux_padding = (ancho_nuevo/4)
			aux_padding = aux_padding - math.floor(aux_padding)
			if(aux_padding == 0.5):
				padding = 2
			elif (aux_padding == 0.25):
				padding = 3
			elif (aux_padding == 0.75):
				padding = 1
			else:
				padding = 0
			impar = 0
		pos = 62 #Posicion inicial
		aux = 62
		pos_arriba = len(data)-padding-(math.ceil(ancho/8)) #Posicion del ultimo primer byte
		aux_arriba = pos_arriba
		#Si es impar siempre tendra un padding acompanando a un color final
		for i in range(0,(limite*ancho_nuevo)):

			if(pos == aux+(math.floor(ancho/8)-impar)): #Si llego al ultimo dato lo cambio y salto el padding
				swap = data[pos]
				data[pos] = data[aux_arriba]
				data[aux_arriba] = swap

				pos = pos + padding + 1
				pos_arriba = pos_arriba-padding-(math.ceil(ancho/8))
				aux_arriba = pos_arriba
				aux = pos
			else:
				#Cambio data pertinente
				swap = data[pos]
				data[pos] = data[aux_arriba]
				data[aux_arriba] = swap

				pos+=1
				aux_arriba+=1		

	
	with open('salida.bmp', 'wb') as f:
		f.write(data)

	guardar_imagen(1)

#Funcion para obtener el espejo horizontal de una imagen
def espejo_horizontal(data,alto,ancho):
	#Condicional que indica el tipo de imagen
	if data[28] == 24:
		#Saco padding y limites
		padding = sacar_padding24(ancho)

		pos = 54 #Posicion inicial de datos
		aux = 54
		pos_derecha = 54+(ancho*3)-1 #Pos final de datos de la primera file
		for i in range(0,alto):
			for j in range(0,(math.floor(ancho/2))):
				#Cambio data de una misma fila
				B = data[pos]
				G = data[pos+1]
				R = data[pos+2]
				data[pos] = data[pos_derecha-2]
				data[pos+1] = data[pos_derecha-1]
				data[pos+2] = data[pos_derecha]
				data[pos_derecha] = R
				data[pos_derecha-1] = G
				data[pos_derecha-2] = B

				pos += 3
				pos_derecha-=3

			#Salto el padding
			pos = aux + (ancho*3) + padding
			pos_derecha = pos+(ancho*3)-1
			aux = pos
			
	elif data[28] == 8:
		#Saco padding y limites
		padding = sacar_padding8(ancho)

		pos = 1078 #Posicion inicial
		for i in range(0,alto):
			fila = data[pos:pos+ancho-1] #Obtengo fila sin padding
			fila = fila[::-1] #Giro la fila
			data[pos:pos+ancho-1] = fila
			pos = pos+ancho+padding

	elif data[28] == 4:		
		#Saco padding y limites
		if (ancho%2) == 0:
			impar = 1
		else:
			impar = 0

		padding = sacar_padding4(ancho)

		pos = 118 #Posicion inicial
		aux = 118
		pos_derecha = 118+math.ceil(ancho/2)-1 #Posicion final de la primera fila
		#Si es impar tendra padding acompanando al color
		if impar==0:
			for i in range(0,alto):
				for j in range(0,(math.ceil(ancho/4))):
					if(aux == pos):
						#Primera posicion cambio SOLO el color y omito el padding
						byte = '{:08b}'.format(data[pos])
						byte_final = '{:08b}'.format(data[pos_derecha]) 
						data[pos] = int(byte_final[0:4]+byte[4:8],2)
						data[pos_derecha] = int(byte[0:4]+byte_final[4:8],2)

						pos+=1
						pos_derecha-=1
					else:
						#Cambios pertinentes
						byte = '{:08b}'.format(data[pos])
						byte_final = '{:08b}'.format(data[pos_derecha])
						byte_anterior = '{:08b}'.format(data[pos-1]) 
						data[pos-1] = int(byte_anterior[0:4]+byte_final[4:8],2) #Cambio el color que me falta de la anterior posicion
						data[pos] = int(byte_final[0:4]+byte[4:8],2)
						data[pos_derecha] = int(byte[0:4]+byte_anterior[4:8],2)

						pos+=1
						pos_derecha-=1

				#Salto el padding
				pos += math.ceil(ancho/4)+padding
				pos_derecha = pos+math.ceil(ancho/2)-1
				aux=pos
		
		else: #Caso par
			for i in range(0,alto):
				for j in range(0,(math.floor(ancho/4))):
					#Cambios pertinentes
						byte = '{:08b}'.format(data[pos])
						byte_final = '{:08b}'.format(data[pos_derecha])
						data[pos] = int(byte_final[4:8]+byte_final[0:4],2)
						data[pos_derecha] = int(byte[4:8]+byte[0:4],2)

						pos+=1
						pos_derecha-=1
				pos += math.ceil(ancho/4)+padding
				pos_derecha = pos+math.ceil(ancho/2)-1

	else: #Caso 1 bit
		#Saco padding y limites		
		if (alto%2) == 0:
			limite = int(alto/2)
		else:
			limite = int((alto/2)+1)

		padding = sacar_padding1(ancho)

		if (ancho%2) == 0:
			impar = 0
		else:
			impar = 1
		pos = 62 #Posicion inicial de datos
		aux = 62
		ancho_aux = ancho
		bin_padding = ""
		while ancho_aux > 8: #Obtengo cuantos son los bits de color del ultimo byte de la fila
			ancho_aux-=8
		inicio_info = 8-ancho_aux #Obtengo cuantos son los bits de padding del ultimo byte de la fila
		while ancho_aux < 8:
			bin_padding = bin_padding + '0' #Creo un string con tantos '0' como bits de padding hay
			ancho_aux+=1
		bytes_aux = ""
		final = int(ancho/8)+impar
		for i in range(0,alto):
			#Ciclo que recorre todos los bytes de la fila
			for j in range (0,final):
				byte = '{:08b}'.format(data[pos]) #Guardo el byte en el que estoy parado
				byte = byte[::-1] #Lo giro
				
				bytes_aux = byte+bytes_aux #Le concateno los anteriores
				pos+=1
			bytes = bytes_aux[inicio_info:(len(bytes_aux))]+bin_padding #Omito los primeros bits (que seran padding) y le concateno el string de bits que representan estos bits omitidos
			auxiliar = 0
			for k in range (0,final):
				data[aux] = int(bytes[auxiliar:auxiliar+8],2) #Coloco cada 8 de mi string de byte en las posiciones de los bytes de data

				aux += 1
				auxiliar += 8
			bytes = ""
			byte = ""
			bytes_aux = ""
			aux+=padding #Salto el padding
			pos = aux


	with open('salida.bmp', 'wb') as f:
		f.write(data)

	guardar_imagen(1)

def sacar_padding24(ancho):
	#Saco el padding de la imagen
	aux_padding = ((ancho*3)/4)
	aux_padding = aux_padding - math.floor(aux_padding)
	if(aux_padding == 0.5):
		padding = 2
	elif (aux_padding == 0.25):
		padding = 3
	elif (aux_padding == 0.75):
		padding = 1
	else:
		padding = 0

	return padding

def sacar_padding8(ancho):
	aux_padding = (ancho/4)
	aux_padding = aux_padding - math.floor(aux_padding)
	if(aux_padding == 0.5):
		padding = 2
	elif (aux_padding == 0.25):
		padding = 3
	elif (aux_padding == 0.75):
		padding = 1
	else:
		padding = 0

	return padding

def sacar_padding4(ancho):
	if (ancho%2) == 0:
		ancho_nuevo = int(ancho/2)
		aux_padding = ((ancho_nuevo)/4)
		aux_padding = aux_padding - math.floor(aux_padding)
		if(aux_padding == 0.5):
			padding = 2
		elif (aux_padding == 0.25):
			padding = 3
		elif (aux_padding == 0.75):
			padding = 1
		else:
			padding = 0
	else:
		ancho_nuevo = int((ancho/2)+1) #Como en un byte hay dos pixeles debo cambiar cuentas
		aux_padding = (ancho_nuevo/4)
		aux_padding = aux_padding - math.floor(aux_padding)
		if(aux_padding == 0.5):
			padding = 2
		elif (aux_padding == 0.25):
			padding = 3
		elif (aux_padding == 0.75):
			padding = 1
		else:
			padding = 0

	return padding

def sacar_padding1(ancho):
	if (ancho%8) == 0:
		ancho_nuevo = int(ancho/8)
		aux_padding = ((ancho_nuevo)/4)
		aux_padding = aux_padding - math.floor(aux_padding)
		if(aux_padding == 0.5):
			padding = 2
		elif (aux_padding == 0.25):
			padding = 3
		elif (aux_padding == 0.75):
			padding = 1
		else:
			padding = 0
	else:
		ancho_nuevo = int((ancho/8)+1)
		aux_padding = (ancho_nuevo/4)
		aux_padding = aux_padding - math.floor(aux_padding)
		if(aux_padding == 0.5):
			padding = 2
		elif (aux_padding == 0.25):
			padding = 3
		elif (aux_padding == 0.75):
			padding = 1
		else:
			padding = 0

	return padding


#Ejecucion inicial
guardar_imagen(0)
