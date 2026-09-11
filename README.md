# Base-de-Datos-Server
servidor con python, testeando verbos
Diferencias entre verbos:
GET: Se usa para leer o consultar información. No modifica nada en el servidor, solo pide datos.
Ejemplo: GET /users devuelve la lista de usuarios.

POST: Se usa para crear un recurso nuevo en el servidor. Envía datos en el cuerpo de la petición.
Ejemplo: POST /users con un JSON crea un usuario nuevo.
Importante: no es idempotente, porque cada vez que lo llamás puede generar un recurso distinto (si haces 3 POST iguales, se crean 3 usuarios).

PATCH: Se usa para actualizar parcialmente un recurso existente.
Ejemplo: PATCH /users/1 con un JSON que solo cambia el email del usuario 1.

DELETE: Se usa para eliminar un recurso.
Ejemplo: DELETE /users/1 borra el usuario con ID 1.

¿Por qué POST no es idempotente?
Idempotente significa que si repetís la misma operación varias veces, el resultado final es siempre el mismo.

GET, PATCH y DELETE pueden ser idempotentes (ejemplo: borrar el mismo usuario dos veces → el resultado es que ya no existe).

Pero POST no lo es, porque cada ejecución crea algo nuevo.

Si hacés POST /users tres veces con el mismo JSON, terminás con tres usuarios distintos en la base de datos.
