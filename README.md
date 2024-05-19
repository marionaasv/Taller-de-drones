# Taller-de-Drones

#### _Nombre del taller: Taller de Drones_

## **1. Presentación**

En este taller vas a aprender a desarrollar programas en Python para **controlar la operación de
un dron**. Aprenderás a crear un programa con una **interfaz gráfica** que use botones para
ordenar al dron que despegue o vuele en una dirección determinada, que presentará al
usuario un **mapa** en el que mostrará la posición del dron en todo momento y que permitirá
**guiar el dron con las poses de tu cuerpo**, utilizando técnicas de reconocimiento de imagen.

En este repositorio encontrarás:
1. Los **códigos** de referencia para la realización del taller.
2. Material **escrito**.
3. **Vídeos** que te guiarán durante el proceso.
   
Aprenderás instalando esos códigos, analizándolos, modificándolos y ampliándolos.

El taller admite diferentes grados de implicación. Puedes limitarte a instalar los códigos, 
comprobar que funcionan correctamente y examinarlos. Eso no te llevará más de 1 hora.
Puedes también enfrentarte a unos cuantos retos concretos que te iremos proponiendo, y que
requerirán que añadas código de tu propia cosecha. **En el repositorio encontrarás los códigos
que resuelven esos retos**, para el caso en que necesites ayuda. Esta modalidad te llevará unas
2 horas. Finalmente, puedes abordar tus propios retos, porque seguro que te vas a imaginar
cosas. Ya no podemos indicarte cuántas horas te llevará eso, porque podrías consagrar tu vida
entera a añadir funcionalidades interesantes.

Los códigos que vas a desarrollar interactúan en realidad con un **simulador del dron**, de
manera que solo necesitas tu portátil, las instalaciones que te indicaremos y los códigos de
referencia.

No obstante, existe un segundo taller en el que tus códigos harán volar un **dron real** (para lo
cual tendrás que modificar solo un par de líneas de tu código). Naturalmente, ese segundo
taller se realiza de forma presencial en las instalaciones **del campus del Baix Llobregat de la
UPC, en Castelldefels**.


  <a href="https://www.youtube.com/watch?v=P_NCKA_3-PQ">, <a href="https://www.youtube.com/watch?v=UPyklN9namM">
    <img src="https://img.youtube.com/vi/P_NCKA_3-PQ/0.jpg" width="250" alt="Vista previa del video">, <img src="https://img.youtube.com/vi/UPyklN9namM/0.jpg" width="250" alt="Vista previa del video">
  </a>


## 2. Etapas del taller

El taller está organizado en 4 etapas, que se describen a continuación:

**- Etapa 1**: Se desarrolla un programa en **Python** con una **interfaz gráfica** basada en botones con
los que controlar la operación del dron (operaciones básicas como **armar, despegar, volar en
diferentes direcciones** o **aterrizar**). En esta etapa se plantean un par de **retos**, cuya solución
también puede encontrarse en el repositorio.

**- Etapa 2.A:** Se añade al resultado de la Etapa 1 un **mapa** que permite mostrar al usuario la
posición del dron en cada momento. También se plantean un par de **retos** que permiten al
usuario interactuar con el dron a través del mapa.

**- Etapa 2.B:** Se añade al resultado de la Etapa 1 el código necesario para guiar el dron mediante
las **poses del cuerpo**, detectadas a través de la cámara del portátil. De nuevo se plantearán dos
**retos** para ampliar las funcionalidades de esta versión.

**- Etapa 3:** Consiste en integrar en una única aplicación los desarrollos de las etapas anteriores,
puesto que las etapas **2.A** y **2.B** se desarrollarán **de manera independiente y en cualquier
orden.**

Como ya se ha indicado, en cualquiera de esas etapas es posible plantearse retos mucho más
ambiciosos que los que se propondrán. Eso ya dependerá de tu nivel de motivación y del
tiempo que quieras dedicar a este taller.

## 3. Herramientas

Para realizar el taller necesitarás instalar en tu ordenador las herramientas siguientes:

**- Git:** Es una herramienta muy popular para la gestión de versiones. Con esta herramienta
podrás instalar en tu ordenador (clonar) este repositorio y acceder a los códigos de las
diferentes etapas:<br />
https://git-scm.com/downloads

**- Mission Planner:** Es una aplicación de escritorio que **permite interactuar con el dron**. Por
ejemplo, permite configurar muchos parámetros del dron y darle ordenes típicas (armar,
despegar, volar a un punto dado, etc.). Mission Planner permite también poner en marcha un
**simulador del dron**, que llamaremos **SITL** (Software In The Loop). Tanto Mission Planner como
las aplicaciones que se desarrollan en este taller **interactúan con el simulador, exactamente
igual que como lo harían con el dron real**. Esto es ideal para desarrollar y verificar el correcto
funcionamiento de los códigos antes de usarlos para controlar el dron real (cosa que podrás
hacer si realizas el segundo taller al que hemos hecho referencia en la presentación):<br />
https://ardupilot.org/planner/docs/mission-planner-installation.html

<p>
  <img src="mp.png" width="70%"/>
</p>

**- PyCharm:** Se trata de la aplicación más popular para el desarrollo de código en Python.
Asegurate de instalar la versión denominada Community Edition, que es gratuita y más que
suficiente.<br />
https://www.jetbrains.com/pycharm/

**- Python:** Necesitarás un intérprete de Python. Puedes utilizar las versiones más actuales.<br />
https://www.python.org/downloads/

Además, durante el taller tendrás que instalar en el entorno de desarrollo creado por Pycharm
diferentes librerías. Por ejemplo:

```bash
import mediapipe as mp
import cv2
```
Dónde: 

**- Mediapipe:** permite detectar puntos clave del cuerpo que aparece en la imagen

  
**- OpenCV:** permite una gran variedad de operaciones de tratamiento de imagen


