git clone https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life MicB
cd MicB/
mkdir "temp"
mkdir "output"

# Clone the Synchronized-BatchNorm-PyTorch repository for
cd Face_Enhancement/models/networks/
git clone https://github.com/vacancy/Synchronized-BatchNorm-PyTorch
cp -rf Synchronized-BatchNorm-PyTorch/sync_batchnorm .
cd ../../../

cd Global/detection_models
git clone https://github.com/vacancy/Synchronized-BatchNorm-PyTorch
cp -rf Synchronized-BatchNorm-PyTorch/sync_batchnorm .
cd ../../

# Download the landmark detection pretrained model
cd Face_Detection/
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
cd ../

# Download the pretrained model from Azure Blob Storage, put the file Face_Enhancement/checkpoints.zip under ./Face_Enhancement, and put the file Global/checkpoints.zip under ./Global. Then unzip them respectively.
cd Face_Enhancement/
wget https://facevc.blob.core.windows.net/zhanbo/old_photo/pretrain/Face_Enhancement/checkpoints.zip
unzip checkpoints.zip
cd ../
cd Global/
wget https://facevc.blob.core.windows.net/zhanbo/old_photo/pretrain/Global/checkpoints.zip
unzip checkpoints.zip
cd ../

# Install dependencies
conda install -y cmake
pip install -r requirements.txt
