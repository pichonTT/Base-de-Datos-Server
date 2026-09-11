import json
from wsgiref.simple_server import make_server

tasks = {}
next_id = 1

def app(environ, start_response):
    global tasks, next_id

    method = environ["REQUEST_METHOD"] #de la clave "REQUEST_METHOD" se obtiene el valor (un verbo)
    path = environ["PATH_INFO"] #de la calve "PATH_INFO" se obtiene el valor (una ruta)
    
    # --- GET /tasks ---  | Devuelve todas las tareas. `200 OK` |
    if method == "GET" and path == "/tasks":
        response_body = json.dumps(tasks)
        status = "200 OK"
        headers = [("Content-Type", "application/json")]

    # --- GET /tasks/{id} --- | Devuelve una tarea por id. `200 OK` o `404 Not Found` si no existe |
    elif method == "GET" and path.startswith("/tasks/"):
        task_id = path.split("/")[-1]
        if task_id.isdigit() and int(task_id) in tasks:
            response_body = json.dumps(tasks[int(task_id)])
            status = "200 OK"
        else:
            response_body = json.dumps({"error": "Not Found"})
            status = "404 Not Found"
        headers = [("Content-Type", "application/json")]

    # --- POST /tasks --- | Crea una nueva tarea con el cuerpo JSON recibido y le asigna un id. `201 Created` |
    elif method == "POST" and path == "/tasks":
        try:
            length = int(environ.get("CONTENT_LENGTH", 0))
            body = environ["wsgi.input"].read(length)
            data = json.loads(body.decode("utf-8"))

            tasks[next_id] = data
            data["id"] = next_id
            next_id += 1

            response_body = json.dumps(data)
            status = "201 Created"
        except Exception as e:
            response_body = json.dumps({"error": str(e)})
            status = "400 Bad Request"
        headers = [("Content-Type", "application/json")]

    # --- PATCH /tasks/{id} --- | Modifica **solo los campos** enviados en el cuerpo JSON. `200 OK` o `404 Not Found` |
    elif method == "PATCH" and path.startswith("/tasks/"):
        task_id = path.split("/")[-1]
        if task_id.isdigit() and int(task_id) in tasks:
            length = int(environ.get("CONTENT_LENGTH", 0))
            body = environ["wsgi.input"].read(length)
            data = json.loads(body.decode("utf-8"))

            # Actualiza solo los campos enviados
            tasks[int(task_id)].update(data)

            response_body = json.dumps(tasks[int(task_id)])
            status = "200 OK"
        else:
            response_body = json.dumps({"error": "Not Found"})
            status = "404 Not Found"
        headers = [("Content-Type", "application/json")]

    # --- DELETE /tasks/{id} --- | Elimina la tarea con ese id. `200 OK` / `204 No Content` o `404 Not Found` |
    elif method == "DELETE" and path.startswith("/tasks/"):
        task_id = path.split("/")[-1]
        if task_id.isdigit() and int(task_id) in tasks:
            del tasks[int(task_id)]
            response_body = json.dumps({"message": "Deleted"})
            status = "200 OK"
        else:
            response_body = json.dumps({"error": "Not Found"})
            status = "404 Not Found"
        headers = [("Content-Type", "application/json")]

    # --- Ruta no encontrada --- | Cualquier otra combinaciÃ³n | `404 Not Found` (o `405 Method Not Allowed` si la ruta existe pero el verbo no) |
    else:
        response_body = json.dumps({"error": "Not Found"})
        status = "404 Not Found"
        headers = [("Content-Type", "application/json")]

    start_response(status, headers)
    return [response_body.encode("utf-8")]

if __name__ == "__main__":
    with make_server("", 9292, app) as server:
        print("Servidor escuchando en http://localhost:9292")
        server.serve_forever()