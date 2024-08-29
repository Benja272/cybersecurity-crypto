## Repositorio con la resolucion de los desafios planteados en la seccion de criptografia de la diplomatura en ciberseguridad resueltos por Benjamin Martinez Picech.

## Aleatoriedad

### Clave generada a partir de la fecha y hora

Ver el archivo `fechayhorakey.py`, me base en la explicacion del ejercicio para generar todas las posibles fechas en microsegundos e intentar descifrar el mensaje pero no pude encontrar la solucion. Tomo la seccion del IV correspondiente mas la clave prospecto para desifrar, remover el padding y luego mostrar el mensaje en codificacion ascii.

## Cifrado de flujo

### Cambio de bits en el texto cifrado

Ver el archivo `cif_flujo/bit_flipping.py`, use el conocimiento sobre el texto claro mas la capacidad de elegir el texto claro del campo data para modificar el mensaje cifrado y lograr una escalada de privilegios luego de que el servidor descifre el mensaje. Al hacer un xor con el texto claro conocido logre "anular" el mensaje original y quedarme solo con la secuencia cifrante, haciendo nuevamente un xor con el texto claro deseado logre modificar el mensaje cifrado y lograr la escalada de privilegios.

## Cifrado de bloques

### Falsificación en modo ECB

Ver archivo ecv_ej.py
Considerando que si el usuario registró el correo usuario@example.com, el perfil tendrá la forma:

user=usuario@example.com&id=547&role=user

Entonces la idea fue jugar con los mails para construir construir bloques que nos permitan generar el mensaje que queremos, en particular uno de los mails que enviamos terminaba en .admin en lugar de .com, por lo que logre que uno de los bloques cifrados contenga [...&role=], como podemos agregar los pares key value que queramos podemos inventar una key sinsentido que nos permita ignorar la primera parte del bloque con el string [...&role=]. Luego jugando con los tamaños de los emails logramos que otro mensaje cifrado contenga el texto claro [admin&id=xxx&role=user + padding], ordenando adecuadamente los bloques logramos que el mensaje cifrado sea el deseado, gracias a que se utiliza la misma key en cada llamada al servidor.

Ejemplo de texto claro construido:

```
...user=...&role=admin&id=xxx&role=user
```

## Funciones de hash

### Colisiones en una función de hash

Ver archivo hash_collision.py
Dado el la poca cantidad de bits que reprecentan el hash teoricamente deberia costarnos 2^24 operaciones encontrar una colision utilizando la fuerza bruta. Genere un mensaje partiendo de mi email con todos las posibles extenciones de 5 bytes imprimibles y busque conincidencias entre los hashes generados.

## Autenticación

### CBC-MAC

Ver archivo cbc_mac.py
Para este desafio utilice el conocimiento sobre el CBC-MAC y como se puede explotar la propiedad de que el estado final de CBC se puede considerar un estado intermedio del algoritmo, ademas de que la key y el IV se mantienen iguales en cada llamado al servidor. De la misma forma como se explica en la consigna, tenemos que:

```
M = M1 || M2 || .. || Mn
T = CBC-MAC(M)
```

Podemos generar un mensaje M' tal que:

```
M' = M || (M1 XOR T) || M2 || .. || Mn || (M1 XOR T) || .. MN
con CBC-MAC(M') = T
```

Lo que imlica que podemos reptetir el mensaje original tanto como queramos para alcanzar las transferencias necesarias hacia nuestra cuenta. Tuve que considerar el relleno modo PKCS#7 para generar el mensaje nuevo porque el tamaño del mensaje original no era multiplo del tamaño de bloque.
