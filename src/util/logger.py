import os
import logging
import sys

def set_logging(log_dir: bool=None):
    if log_dir is None:
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(message)s')
    else:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = os.path.join(log_dir, f'{timestamp}.log')
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_path, encoding='utf-8')
            ]
        )


def setup_child_io_logging(log_path: str, level: int = logging.INFO):
    """
    将子进程的 logging、stdout、stderr 全部重定向到 log_path。
    保证逐条 flush，便于实时查看。
    """
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # 清理并设置 root logger
    for h in list(logging.root.handlers):
        logging.root.removeHandler(h)
    logging.root.setLevel(level)

    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8", delay=False)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(processName)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logging.root.addHandler(file_handler)

    # stdout/stderr 重定向
    log_fp = open(log_path, "a", buffering=1, encoding="utf-8")
    sys.stdout = log_fp
    sys.stderr = log_fp

    # 每条记录后 flush
    class _FlushingFileHandler(logging.FileHandler):
        def emit(self, record):
            super().emit(record)
            try:
                self.flush()
            except Exception:
                pass

    logging.root.removeHandler(file_handler)
    flushing_handler = _FlushingFileHandler(log_path, mode="a", encoding="utf-8", delay=False)
    flushing_handler.setLevel(level)
    flushing_handler.setFormatter(file_handler.formatter)
    logging.root.addHandler(flushing_handler)