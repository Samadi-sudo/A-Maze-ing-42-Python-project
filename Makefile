PYTHON = python3
PIP    = pip3
MAIN   = a_maze_ing.py
CONFIG = config.txt
MLX_WHEEL_URL = https://cdn.intra.42.fr/document/document/43689/mlx-2.2-py3-ubuntu-any.whl
MLX_WHEEL = mlx-2.2-py3-none-any.whl

.PHONY: install run debug clean lint lint-strict

install:
	@wget -q -O $(MLX_WHEEL) $(MLX_WHEEL_URL) 2>/dev/null || true
	@$(PIP) install --user $(MLX_WHEEL) flake8 mypy

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	flake8 .
	mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict