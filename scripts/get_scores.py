import requests
from tqdm import tqdm

URL = "http://0.0.0.0:9090/estimate_quality"
batch_size = 100

src_lang = "en"
tar_lang = "hi"

src_file = "/14td1/varun-18869/model/create_finetune/finetune/sources.txt"
tar_file = "/14td1/varun-18869/model/create_finetune/finetune/translations.txt"

with open(src_file, "r") as f1, open(tar_file, "r") as f2:
    lines_src = f1.readlines()
    lines_tar = f2.readlines()

lines_src = [line.strip() for line in lines_src]
lines_tar = [line.strip() for line in lines_tar]

data = []
[data.append({"source" : lines_src[index], "translate": lines_tar[index]}) for index, _ in enumerate(lines_src)]

with open("comet_scores.txt", "w") as f:
    for lines in tqdm(range(0, len(lines_src), batch_size), desc = "Querying Your Request"):
        json_data = {
                "source_language" : src_lang,
                "target_language" : tar_lang,
                "translation" : data[lines: lines+batch_size]
        }
        response =  requests.post(f"{URL}", json=json_data)
        temp_output = (response.json())
        f.writelines(str(temp_output)+'\n')
