# Iris Full-Stack Classifier

- **Description:** Extend the FastAPI Iris classifier with a web UI and PostgreSQL inference logging, all runnable with Docker Compose.
- **Inputs:** Sepal length, sepal width, petal length, and petal width in centimetres.
- **Classes:** Setosa, versicolor, and virginica.

## Assignment

- Create a `ui/` directory with a Streamlit app for entering the four measurements.
- Send the measurements from the UI to the API's `POST /predict` endpoint and display the predicted species.
- Add a `ui/Dockerfile` to build and run the Streamlit app.
- Add a root-level `compose.yaml` with services for the API, UI, and PostgreSQL.
- Use the lightweight official PostgreSQL image `postgres:16-alpine` and configure a persistent data volume.
- Create `api/.env` with a `DATABASE_URL` for the Compose PostgreSQL service, for example:
  `DATABASE_URL=postgresql://postgres:postgres@db:5432/iris`
- Keep the database name, user, and password consistent between `api/.env` and the Compose PostgreSQL settings.
- Configure the UI to call the API at `http://api:8000` from inside Compose; use the Compose service name, not `localhost`.
- Start the full stack from the project root with `docker compose up --build`.
- Verify the UI prediction, API docs at `http://localhost:8000/docs`, and inference records in PostgreSQL.

## Run the full stack

Use Docker with Docker Compose 2.24 or newer. For a local configuration file,
copy `api/.env.example` to `api/.env` from the project root.

```powershell
Copy-Item api/.env.example api/.env
docker compose up --build
```

On Linux or macOS, use `cp api/.env.example api/.env` for the copy step.
Compose uses the committed example for the local demo if `api/.env` is absent.
If you change the demo database credentials, update the `db` settings in
`compose.yaml` and `DATABASE_URL` in `api/.env` together.

## Verify a prediction

1. Open the [Streamlit UI](http://localhost:8501). Click **Predict species**
   with the default measurements (5.1, 3.5, 1.4, 0.2 cm). The result is **Setosa**.
2. Open the [FastAPI docs](http://localhost:8000/docs) and check that
   `POST /predict` is listed. You can send another prediction using **Try it out**.
3. In a second terminal, check the stored inputs, class ID, and timestamp.

```sh
docker compose exec db psql -U postgres -d iris -c "SELECT id, features, prediction, created_at FROM inferences ORDER BY id DESC LIMIT 10;"
```

Class IDs are `0` for setosa, `1` for versicolor, and `2` for virginica.
Stop the stack with `docker compose down`. The `postgres_data` volume
keeps inference records across restarts.
