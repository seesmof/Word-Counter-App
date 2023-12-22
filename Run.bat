if not exist "./data/requirements.txt" (
  echo Installing requirements...
  pip install -r requirements.txt
  echo Requirements installed successfully > "./data/requirements.txt"
)

python ./src/main.py
pause