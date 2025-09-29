# utils/file_reader.py
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)


def read_video_info(txt_path: str):
    txt_file = Path(txt_path)
    if not txt_file.exists():
        logger.error(f"文件不存在：{txt_path}")
        return None, None

    title = ""
    description = ""
    try:
        with txt_file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("title:"):
                    title = line.replace("title:", "", 1).strip()
                elif line.startswith("description:"):
                    description = line.replace("description:", "", 1).strip()
        return title, description
    except Exception as e:
        logger.error(f"读取 TXT 文件失败: {e}")
        return None, None
