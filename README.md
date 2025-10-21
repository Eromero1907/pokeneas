# Pokeneas (Flask + Docker + AWS S3)

Mini Pokedex paisa para el **Taller 02 – AWS**. Incluye:
- App Flask con 2 rutas (`/pokenea/json` y `/pokenea/view`)
- Contador/ID de contenedor (hostname) para verificar réplicas en Swarm
- Dockerfile listo para producción (Gunicorn)
- Workflow de GitHub Actions para construir y publicar a Docker Hub
- Estructura separada por módulos (no todo en un solo archivo)

---

## 🗂️ Estructura
```
app/
  __init__.py
  main.py
  routes.py
data/
  pokeneas.py
templates/
  view.html
.github/workflows/
  docker.yml
Dockerfile
requirements.txt
```

---

## ▶️ Ejecutar local
1. Crea y activa un entorno virtual (opcional).
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta:
   ```bash
   python -c "from app.main import create_app; app = create_app(); app.run(host='0.0.0.0', port=5000, debug=True)"
   ```
   - `http://127.0.0.1:5000/pokenea/json`
   - `http://127.0.0.1:5000/pokenea/view`

> **Nota:** Para obtener el `container_id` en local se usa el hostname del sistema; en contenedores será el ID del contenedor.

---

## 🐳 Docker
Construir y ejecutar:
```bash
docker build -t pokeneas:local .
docker run -p 5000:5000 pokeneas:local
```

---

## ☁️ AWS S3 (Imágenes públicas)
1. Crea un bucket S3 (misma región que las instancias EC2).
2. Desactiva el **bloqueo de acceso público** del bucket (ojo con costos y compliance).
3. Sube tus imágenes (PNG/JPG).
4. Copia las URLs públicas y reemplázalas en `data/pokeneas.py`.

> Este proyecto **no requiere** credenciales AWS si usas URLs públicas. Si quieres, puedes usar `boto3` para listar objetos S3 (ver comentarios en `data/pokeneas.py`).

---

## 🐙 GitHub + Docker Hub
1. Crea un repo en Docker Hub, por ejemplo: `USUARIO/pokeneas`.
2. En GitHub > Settings > Secrets and variables > Actions:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN` (Access Token de Docker Hub)
3. Cambia la etiqueta del workflow en `.github/workflows/docker.yml` para apuntar a tu imagen `USUARIO/pokeneas:latest`.
4. Empuja a `main` y verifica la publicación en Docker Hub.

---

## 🐝 Docker Swarm en AWS (4 instancias)
En la **líder**:
```bash
docker swarm init --advertise-addr <IP_PUBLICA_LIDER>
docker swarm join-token manager  # copia el comando
```

En las otras 3 instancias, pega el comando de `join`.

En la **líder**, despliega 10 réplicas:
```bash
docker service create --name pokeneas --replicas 10 -p 80:5000 USUARIO/pokeneas:latest
docker service ls
docker service ps pokeneas
```

Prueba:
- `http://IP_PUBLICA/pokenea/json`
- `http://IP_PUBLICA/pokenea/view`

---

## ✅ Entregables sugeridos
- Captura de `docker service ps pokeneas` con 10 tareas.
- Captura del bucket S3 con las imágenes.
- Dos capturas de `/pokenea/view` mostrando **dos container_id distintos**.
- IP pública y link al repo de GitHub.

¡Éxitos! 💪