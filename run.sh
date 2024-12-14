echo "Trying to activate virtual environment..."
python -m venv .venv
source .venv/bin/activate
echo "Upgrading pip..."
pip install --upgrade pip
echo -e "\n\nInstalling transformers..."
pip install --upgrade transformers
echo -e "\n\nInstalling pytorch..."
pip3 install torch torchvision torchaudio scipy
