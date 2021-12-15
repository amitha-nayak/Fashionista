import pandas as pd
import numpy as np
import json
import os

os.environ['TPU_CONFIG_JSON'] ="tpu_configs/tpu.json"
os.system('sudo ./scripts/predict.sh  \
gs://<MODEL DIR> \
<IMAGE DIR> \
gs://<TF RECORDS> \
gs://<PRED DIR>')

