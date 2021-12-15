import pandas as pd
import numpy as np
import json
import os

def predict():
    os.environ['TPU_CONFIG_JSON'] ="tpu_configs/example.json"
    os.system('sudo ./scripts/predict.sh  \
        gs://capstone-data1/model \
        /home/jigyas15/t4/fash/media/images \
        gs://capstone-data1/production/tfrecords/sample \
        gs://capstone-data1/production/predictions')


    df = pd.read_json('predictions.json')
    f=open("../dataset-iMaterialist/raw/label_descriptions.json")
    file = json.load(f)

    class_ids=[]
    website_major= []
    website_attr=[]
    threshold_df = df[df['score'].between(.45, 1.)]

    for index, row in threshold_df.iterrows():
    #     rle = row["segmentation"]
    #     mask = coco_rle_to_mask(rle).astype(np.uint8)
    #     masks.append(np.array(mask))
        max_prob_attr=max(row["attribute_probabilities"][:294])
        attribute_index = row["attribute_probabilities"][:294].index(max_prob_attr)
        item=file["attributes"][attribute_index]["name"]

        class_id=row["category_id"]
    #     image = mask
    #     binary = image > 0
    #     plt.imshow(binary)
        item=item+" "+file["categories"][class_id]["name"]
        if class_id<26:
            website_major.append(item)
        else :
            website_attr.append(item)
    #     plt.show()

    website_attr=np.unique(website_attr).tolist()
    print(website_major)
    print(website_attr)
    os.system('sudo rm -r /home/jigyas15/t4/fash/media/images/*')
    val={'major':website_major,'minor':website_attr}
    return val
    #     website I/O
