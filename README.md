# Fashionista

<p align="center">
<img src="https://github.com/amitha-nayak/Fashionista/blob/main/model%20architecture.png" width=100%/>
</p>

## Model architecture:

Mask R-CNN model

SpineNet-143 + FPN backbone

## Training:

Pre-trained on the COCO dataset

Image resolution: 1280x1280

Focal loss for the attributes head

Augmentations: random scaling (0.5x - 2.0x), v3 policy from the AutoAugment (modified to support masks)

## Setup
- Set up `gcloud` command.

   - https://cloud.google.com/sdk/docs/install?hl=ja
   - https://cloud.google.com/sdk/docs/initializing
   - https://medium.com/google-cloud-jp/gcp-%E3%81%A8-oauth2-91476f2b3d7f

- Install `ctpu` command.

https://github.com/tensorflow/tpu/tree/master/tools/ctpu#download

- Copy and modify a TPU config file

`cp tpu_configs/example.json tpu_configs/YOUR_TPU.json`

- Create a VM instance and TPU

```
export TPU_CONFIG_JSON=tpu_configs/YOUR_TPU.json
./scripts/tpu.sh create
```

You will automatically log in the VM via SSH.

- Grant roles/storage.admin the TPU service account (e.g., service-1123456789@cloud-tpu.iam.gserviceaccount.com).

- Install Python dependencies to the VM instance.
```
cd $HOME
git clone https://github.com/amitha-nayak/Fashionista.git
cd $HOME/kaggle-imaterialist2020-model
./scripts/setup_bashrc.sh
source ~/.bashrc
./scripts/install_requirements.sh

```

- Setup is done. Log out from the terminal, and stop the VM and TPU.

```
./scripts/tpu.sh stop

# or
./scripts/tpu.sh stop --vm
./scripts/tpu.sh stop --tpu
```

## Train

- Log in to the VM instance via SSH.

```
./scripts/tpu.sh start
./scripts/tpu.sh ssh
```
- Set up iMaterialist dataset.
- Create TF Records from iMaterialist COCO format annotations

```
poetry shell

./scripts/create_tf_records.sh \
    train \
    $IMAGE_DIR \
    $COCO_JSON_FILE \
    $OUTPUT_FILE_PREFIX

# e.g.,
./scripts/create_tf_records.sh \
    train \
    ~/iMaterialist/raw/train \
    ~/iMaterialist/raw/instances_attributes_train2020.json \
    gs://yourbucket/tfrecords/train
    
```
    
TF Records will be created like `gs://yourbucket/tfrecords/train-00001-of-00050.tfrecord`.

- Train a model.

```
./scripts/train.sh $INPUT_GCS_PATTERN $OUT_GCS_DIR

# e.g.,
./scripts/train.sh \
    gs://yourbucket/tfrecords/train-* \
    gs://yourbucket/model
  
 ```
Training artifacts (checkpoints, hyperparmeters, and logs etc) will be dumped into `gs://yourbucket/model/`.

- Don't forget to stop your TPU if the training finishes.

```
./scripts/tpu.sh stop --tpu
```
- Note: If the training fails, delete the training artifacts from GCS. Otherwise, the configurations of the failed training will be loaded and it will fail again. For example, tensor's shape mismatch.

## Predict
- Log in to the VM instance via SSH.

```
./scripts/tpu.sh start --vm
./scripts/tpu.sh ssh
```

- Predict for your images

```
poetry shell

./scripts/predict.sh \
    $MODEL_GCS_DIR \
    $IMAGE_GCS_DIR \
    $TF_RECORD_GCS_DIR \
    $OUT_GCS_DIR

# e.g.,
./scripts/predict.sh \
    gs://yourbucket/model \
    gs://yourbucket/yourdataset/images \
    gs://yourbucket/yourdataset/tfrecords \
    gs://yourbucket/yourdataset/predictions
   ```
   
- The TPU should be automatically shut down by scripts/predict.sh.

## Django UI

- Log in to the VM instance via SSH.

```
./scripts/tpu.sh start --vm
./scripts/tpu.sh ssh
```

- Run django
```
cd kaggle-imaterialist2020-model
python3 ../manage.py runserver
```
- Don't forget to stop your TPU.

```
./scripts/tpu.sh stop --tpu
```

- Note: to change or add sample images on the website, 

use the path `./fash/media/images`

<hr />

All the changes were made on top of the [TPU Object Detection and Segmentation Framework](https://github.com/tensorflow/tpu/tree/master/models/official/detection).

