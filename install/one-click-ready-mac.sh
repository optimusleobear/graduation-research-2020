# Installation

conda install -y -c anaconda protobuf  ## photobuf
conda install -y -c anaconda scikit-learn ## scikit-learn
conda install -y -c anaconda scikit-image  ## scikit-image
conda install -y -c menpo opencv   ## opencv
conda install -y pyqt  ## qt5
conda install -y -c pytorch pytorch torchvision torchaudio  ## PyTorch CPU
conda install -y qdarkstyle
conda install -y qtpy
conda install -y wget

conda update --all -y
conda clean --all -y

# Preparation for PyTorch model

wget http://colorization.eecs.berkeley.edu/siggraph/models/caffemodel.pth -O ./models/pytorch/caffemodel.pth
