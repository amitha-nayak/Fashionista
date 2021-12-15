#!/bin/sh -eux
MODEL_GCS_DIR=$1
# e.g., gs://models/sn143-imat-v2
IMAGE_GCS_DIR=$2
# e.g., gs://iMaterialist/train
TF_RECORD_GCS_DIR=$3
# e.g., gs://iMaterialist/tfrecords
TPU_CONFIG_JSON="tpu_configs/tpu.json"
OUT_GCS_DIR=$4
# e.g., gs://predictions
PYTHONPATH="../tools/datasets/research"
msg() {
    set +x
    echo "============================================================================"
    echo "$1"
    echo "============================================================================"
    set -x
}

msg "download from $IMAGE_GCS_DIR"
IMAGE_DIR=/tmp/images
mkdir -p $IMAGE_DIR
gsutil -m rsync -r "$IMAGE_GCS_DIR" $IMAGE_DIR

msg "create TF Records"
PYTHONPATH="../tools/datasets/research" \
    python3 tools/datasets/create_coco_tf_record.py \
    --logtostderr \
    --num_shards=50 \
    --image_dir="$IMAGE_DIR" \
    --output_file_prefix="$TF_RECORD_GCS_DIR/predict"

msg "dump filename CSV"
FILENAME_CSV=/tmp/image_id_filename.csv
./scripts/dump_filenames_to_predict.sh "$IMAGE_DIR" \
    > "$FILENAME_CSV"

msg "predict"
PRED_DIR=/tmp/predictions

mkdir -p "$PRED_DIR"
./scripts/_predict.sh \
    "$MODEL_GCS_DIR" \
    "$TF_RECORD_GCS_DIR/predict-*" \
    "$PRED_DIR"

msg "join prediction with filename"
JOINED_PRED=/tmp/joined_predictions.json
python3 tools/join_prediction_with_filename.py \
    --prediction-json "$PRED_DIR"/predictions.json \
    --filename-csv "$FILENAME_CSV" \
    > $JOINED_PRED

sudo cp "$PRED_DIR"/predictions.json ./

msg "upload to $OUT_GCS_DIR/predictions.json"
gsutil -m cp $JOINED_PRED "$OUT_GCS_DIR"/predictions.json
