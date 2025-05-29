# 🔴 Side-Stacker 🔵
## Instructions

```sh
docker compose up
```

Once the server is up, visit <http://localhost:5000> to start playing.

To test remote multiplayer locally open the game link in different browser or a private tab.

## Development
Run the following commands in a virtual env.

```sh
pip install -e src -r requirements.txt	# deps
ssg_init_db				# init/reset DB
QUART_APP=ssg:app quart run		# dev server
pytest tests/				# tests
```

### Machine Learning

```sh
ssg_train_ml
```

This runs the training script found in `src/ssg/ai/training/train.py` which can be adjusted for retraining, self-play, etc.

This repository includes a pre-trained model.

Model weights are stored in `artifacts/`

## Features

- [x] Real-time UI updates
- [x] Local play (self vs self)
- [x] Remote play (human vs human)
- [x] AI play (human vs AI)
    - [x] 🌱 Random
    - [x] 🌶️ Heuristic/algorithmic
    - [x] ✨ Machine learning
- [x] AI vs AI
- [x] Game spectating
- [x] Game storage/retrieval

## Stack

- [Quart](https://quart.palletsprojects.com/en/latest/index.html): asyncio Python microframework
- [htmx](https://htmx.org/): HTML-first frontend library
- PyTorch
- SQLite
