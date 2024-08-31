## Repositorio con la resolucion de los desafios planteados en la seccion de criptografia de la diplomatura en ciberseguridad resueltos por Benjamin Martinez Picech.

## Aleatoriedad

### Clave generada a partir de la fecha y hora

#### Descripción del desafío

El desafío consiste en descifrar un mensaje encriptado utilizando una clave generada a partir de la fecha y hora.

#### Análisis del problema

El problema surge debido a la previsibilidad de la clave generada. Al utilizar la fecha y hora como semilla para la generación de la clave, se limita significativamente el espacio de búsqueda para un atacante.

#### Descripción de la solución

Ver el archivo `fechayhorakey.py`. Me basé en la explicación del ejercicio para generar todas las posibles fechas en microsegundos e intentar descifrar el mensaje, pero no pude encontrar la solución. Tomé la sección del IV correspondiente más la clave prospecto para descifrar, remover el padding y luego mostrar el mensaje en codificación ASCII.

#### Forma de evitar el problema

Para evitar este problema, se recomienda utilizar fuentes de entropía más robustas y aleatorias para la generación de claves, como generadores de números aleatorios criptográficamente seguros (CSPRNG).

## Cifrado de flujo

### Cambio de bits en el texto cifrado

#### Descripción del desafío

El desafío implica modificar un mensaje cifrado para lograr una escalada de privilegios después de que el servidor lo descifre.

#### Análisis del problema

El problema se produce debido a la maleabilidad del cifrado de flujo, donde los cambios en el texto cifrado se reflejan directamente en el texto claro descifrado.

#### Descripción de la solución

Ver el archivo `cif_flujo/bit_flipping.py`. Usé el conocimiento sobre el texto claro más la capacidad de elegir el texto claro del campo data para modificar el mensaje cifrado y lograr una escalada de privilegios luego de que el servidor descifre el mensaje. Al hacer un XOR con el texto claro conocido logré "anular" el mensaje original y quedarme solo con la secuencia cifrante, haciendo nuevamente un XOR con el texto claro deseado logré modificar el mensaje cifrado y lograr la escalada de privilegios.

#### Forma de evitar el problema

Para evitar este tipo de ataque, se recomienda implementar mecanismos de integridad como MAC (Message Authentication Code) junto con el cifrado, o utilizar modos de operación que proporcionen autenticación e integridad, como GCM (Galois/Counter Mode).

## Cifrado de bloques

### Falsificación en modo ECB

#### Descripción del desafío

El desafío consiste en manipular un perfil de usuario cifrado en modo ECB para obtener privilegios de administrador.

#### Análisis del problema

El problema surge debido a la naturaleza determinista del modo ECB, donde bloques idénticos de texto plano producen bloques idénticos de texto cifrado, permitiendo la manipulación de bloques individuales.

#### Descripción de la solución

Ver archivo ecv_ej.py. Considerando que si el usuario registró el correo usuario@example.com, el perfil tendrá la forma:

user=usuario@example.com&id=547&role=user

La idea fue jugar con los correos electrónicos para construir bloques que nos permitan generar el mensaje que queremos. En particular, uno de los correos que enviamos terminaba en .admin en lugar de .com, logrando que uno de los bloques cifrados contenga [...&role=]. Como podemos agregar los pares key-value que queramos, podemos inventar una key sin sentido que nos permita ignorar la primera parte del bloque con el string [...&role=]. Luego, jugando con los tamaños de los correos, logramos que otro mensaje cifrado contenga el texto claro [admin&id=xxx&role=user + padding]. Ordenando adecuadamente los bloques, logramos que el mensaje cifrado sea el deseado, gracias a que se utiliza la misma key en cada llamada al servidor.

Ejemplo de texto claro construido:

```
...user=...&role=admin&id=xxx&role=user
```

#### Forma de evitar el problema

Para evitar este problema, se recomienda utilizar modos de cifrado más seguros como CBC con un vector de inicialización aleatorio, o preferiblemente modos autenticados como GCM. Además, se debe implementar una validación robusta del lado del servidor para los datos descifrados.

## Funciones de hash

### Colisiones en una función de hash

#### Descripción del desafío

El desafío consiste en encontrar una colisión en una función de hash con una salida de 24 bits.

#### Análisis del problema

El problema surge debido a la limitada cantidad de bits en la salida del hash, lo que hace factible encontrar colisiones mediante fuerza bruta debido al principio del cumpleaños.

#### Descripción de la solución

Ver archivo hash_collision.py. Dado el la poca cantidad de bits que representan el hash, teóricamente debería costarnos 2^24 operaciones encontrar una colisión utilizando la fuerza bruta. Generé un mensaje partiendo de mi email con todas las posibles extensiones de 5 bytes imprimibles y busqué coincidencias entre los hashes generados.

#### Forma de evitar el problema

Para evitar este problema, se deben utilizar funciones de hash criptográficas con una salida suficientemente grande (por ejemplo, SHA-256 con 256 bits) para hacer computacionalmente inviable la búsqueda de colisiones.

## Autenticación

### CBC-MAC

#### Descripción del desafío

El desafío implica explotar una vulnerabilidad en la implementación de CBC-MAC para generar un mensaje falsificado con el mismo MAC que un mensaje válido.

#### Análisis del problema

El problema se produce debido al uso incorrecto de CBC-MAC, donde se permite al atacante conocer el estado intermedio del algoritmo y manipular el mensaje para generar colisiones.

#### Descripción de la solución

Ver archivo cbc_mac.py. Para este desafío utilicé el conocimiento sobre el CBC-MAC y cómo se puede explotar la propiedad de que el estado final de CBC se puede considerar un estado intermedio del algoritmo, además de que la key y el IV se mantienen iguales en cada llamado al servidor. De la misma forma como se explica en la consigna, tenemos que:

```
M = M1 || M2 || .. || Mn
T = CBC-MAC(M)
```

Podemos generar un mensaje M' tal que:

```
M' = M || (M1 XOR T) || M2 || .. || Mn || (M1 XOR T) || .. MN
con CBC-MAC(M') = T
```

Lo que implica que podemos repetir el mensaje original tanto como queramos para alcanzar las transferencias necesarias hacia nuestra cuenta. Tuve que considerar el relleno modo PKCS#7 para generar el mensaje nuevo porque el tamaño del mensaje original no era múltiplo del tamaño de bloque.

#### Forma de evitar el problema

Para evitar este problema, se recomienda utilizar algoritmos de MAC más seguros como HMAC.

## Clave Publica

### RSA con clave pequeña

#### Descripción del desafío

El desafío consiste en descifrar un mensaje encriptado con RSA utilizando una clave pública con un módulo pequeño.

#### Análisis del problema

El problema surge debido al uso de un módulo RSA (n) demasiado pequeño, lo que hace factible su factorización en un tiempo razonable.

#### Descripción de la solución

Ver el archivo RSA_small_key.py. Siguiendo la consigna, conseguí factorizar n utilizando la herramienta msieve, luego pude calcular la clave privada y con esta descifrar el mensaje.

#### Forma de evitar el problema

Para evitar este problema, se deben utilizar tamaños de clave RSA suficientemente grandes (al menos 2048 bits en la actualidad) para que la factorización del módulo sea computacionalmente inviable con los recursos actuales.
