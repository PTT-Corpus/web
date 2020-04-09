import subprocess
from pathlib import Path
import sys

REGISTRY_PATH = Path("/app/cwb/registry")
DATA_PATH = Path("/app/cwb/data")
VRT_PATH = Path("/app/cwb/vrt")

if __name__ == '__main__':
    vrt_file = VRT_PATH / sys.argv[1]

    if not vrt_file.is_file():
        raise Exception(f"{vrt_file}不存在!")

    corpus_name = vrt_file.stem.lower()
    corpus_data_path = DATA_PATH / corpus_name

    # 建立data資料夾
    if not corpus_data_path.is_dir():
        corpus_data_path.mkdir()

    # 執行 cwb-encode
    subprocess.run(['cwb-encode', 
        '-d', str(DATA_PATH / corpus_name), 
        '-f', str(vrt_file),
        '-R', str(REGISTRY_PATH / corpus_name),
        '-xsBv9',
        '-P', 'pos',
        '-S', 'post:0+id+year+month+day+neg+pos+neu',
        '-S', 'titlet:0+id+year+month+day+neg+pos+neu',
        '-S', 'text:0+id+type+author+c_type',
        '-c', 'utf8'
    ])

    # 執行 cwb-makeall
    subprocess.run(['cwb-makeall',
        '-r', str(REGISTRY_PATH),
        '-V', corpus_name
    ])