# Installation

sudo apt update
sudo apt -y install libgl1-mesa-glx
sudo apt -y install libqt5x11extras5
sudo apt -y install libvulkan-dev

conda install -y -c anaconda protobuf  ## photobuf
conda install -y -c anaconda scikit-learn ## scikit-learn
conda install -y -c anaconda scikit-image  ## scikit-image
conda install -y -c menpo opencv   ## opencv
conda install -y pyqt  ## qt5
conda install -y -c pytorch pytorch torchvision torchaudio cpuonly  ## PyTorch CPU
conda install -y qdarkstyle
conda install -y qtpy
conda install -y wget

conda update --all -y
conda clean --all -y

# Preparation for PyTorch model

wget http://colorization.eecs.berkeley.edu/siggraph/models/caffemodel.pth -O ./models/pytorch/caffemodel.pth

# Environment for preprocess

echo "Preprocess is recommended for better performance."
echo -e "\033[31mRun 'bash install/one-click-pre.sh' to build preprocess environment. \033[0m"
echo -e "\033[31mA new conda environment is recommended for preprocess. \033[0m"
