# [Tarea 1](https://github.com/)

## Contenido
* Desarrollo y ejecucion
* Pruebas
* Integrante

## Desarrollo y ejecucion
La tarea fue desarrollada en el lenguaje interpretado python, especificamente la version 3.5 de este.

La misma requiere que se tenga el interprete de python para poder funcionar.

Para ejecutarla ejecute el comando "python Tarea1.py", al ejecutarla se le presentara un menu de consola con el que podra
interactuar, coloque la opcion que desee para que es ejecute dicha accion.

Cabe destacar que el programa recibira siempre al principio una imagen llamada "entrada.bmp" y devolvera una imagen llamada "salida.bmp", este mismo no dejara de funcionar luego de la primera ejecucion, sino que, se le volvera a abrir el menu pero esta vez la accion se le aplicara a la imagen "salida.bmp", esto a fin de conservar la imagen original intacta.

Como dice el enunciado de la tarea el unico formato soportado es el ".bmp" permitiendo solamente imagenes de 1, 4, 8 y 24 bits.

## Pruebas
El programa fue probado en dos computadoras con las siguientes caracteristicas.:

1) Procesador Intel core i5 3210 con 4GB de RAM en Windows 7 de 64bits.

2) Procesador Intel core i5 4210 con 8GB de RAM en Windows 10 de 64bits.

Se menciona que en ambas las acciones se realizacion satisfactoriamente pero con un margen de tiempo bastante diferente en ambas, por ejemplo:

Pruebas de rotaciones de 180 en la pc 1 duraban 10-16 segundos (imagenes grandes), en cambio en la pc 2 duraban 1-2 segundos.

Pruebas de rotaciones de 90 y 270 en la pc 1 podian durar desde 20 segundos hasta casi 1 minuto (dependiendo de la cantidad de bits), mientras que en la pc 2 corrian en 3-4 segundos.

Como maximo tiempo para una accion la pc 1 se podia tomar entre 50 y 1 minuto mientras que la pc 2 entre 3-5 segundos.

Es por esto que al correr este programa y mas aun si se prueban imagenes grandes no se preocupe si ve que el programa
se encuentra "estancado" este todavia esta trabajando y realizando la accion que usted pidio. Esto se reitera en una impresion en el mismo menu del programa.

## Integrante

**Alejandro Moises Barone Cavalieri**
**CI 24206267**