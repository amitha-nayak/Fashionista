import pandas as pd
import numpy as np
import json
import os

def pre(imgdir='0'):
    if(imgdir!='0'):
      clean_up="sudo mkdir -p ../media/images && sudo cp ../main/static/images/{0}.jpg ./media/images/".format(imgdi)
      os.system(clean_up) 
    os.environ['TPU_CONFIG_JSON'] ="tpu_configs/tpu.json"
    os.system('sudo ./scripts/predict.sh  \
        gs://<MODEL DIR> \
        ../media/images \
        gs://<TF RECORDS> \
        gs://<PREDICTIONS>)


    df = pd.read_json('predictions.json')
    f=open("../../label_descriptions.json")
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
    website_major=np.unique(website_major).tolist()
    website_attr=np.unique(website_attr).tolist()
    print(website_major)
    print(website_attr)
    val={'major':website_major,'minor':website_attr}
    return val
    #     website I/O
