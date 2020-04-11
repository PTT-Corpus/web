from pymongo import MongoClient
from pathlib import Path
import time

uri = "mongodb://root:example@mongo/ptt?authSource=admin"
client = MongoClient(uri)

ptt_db = client.ptt
lexical_item_collection = ptt_db.lexical_item

# 計時開始
t_start = time.time()

vrt_path = Path("/app/cwb/vrt")
for vrt in vrt_path.iterdir():
    vrt_file_path = str(vrt)
    board_name = vrt.stem
    with open(vrt_file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line.startswith("<") and not line == "":
                _word_pos = line.split("\t")
                try:
                    word = _word_pos[0]
                    pos = _word_pos[1]
                except:
                    print("出錯的地方")
                    print(line)
                    print(_word_pos)

                lexical_item_collection.update_one(
                    {
                        "word": word,
                        "pos": pos,
                    },
                    {
                        "$inc": {
                            f"boards.{board_name}": 1,
                            "total": 1
                        }
                    },
                    upsert=True
                )


# 計時結束
t_end = time.time()
print(f"花掉的時間: {t_end - t_start}")
