#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import traceback
import logging
from datetime import datetime
from multiprocessing import current_process, get_context
from multiprocessing.managers import SyncManager
from typing import Callable, List, Any, Dict, Tuple
from threading import Thread, Event

from src.util import setup_child_io_logging

# -------------------------------
# Helpers
# -------------------------------

def ensure_parent_dirs(path: str):
    d = os.path.dirname(os.path.abspath(path))
    if d:
        os.makedirs(d, exist_ok=True)

def fmt_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def fmt_duration(seconds: float) -> str:
    seconds = int(max(0, seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h{m:02d}m{s:02d}s"
    elif m:
        return f"{m}m{s:02d}s"
    return f"{s}s"

# -------------------------------
# Worker
# -------------------------------

def _worker(index: int, func: Callable, task_name: str, params: Any, log_path: str,
            running_proxy, completed_proxy) -> Tuple[int, str, int, Any]:
    """
    Execute a task inside a process. Update running/completed stores and write logs.
    Return (index, task_name, return_code, return_value).
    """
    pid = os.getpid()
    start_ts = time.time()
    start_dt = fmt_ts(start_ts)

    setup_child_io_logging(log_path)

    # mark running
    running_proxy[pid] = {
        "task": task_name,
        "start_ts": start_ts,
        "start_dt": start_dt,
        "log_path": os.path.abspath(log_path)
    }

    ret_val: Any = None
    try:
        logging.info(f"Start task[{index}]: {task_name} (PID={pid}) params={params!r}")
        if isinstance(params, (list, tuple)):
            ret_val = func(*params)
        else:
            ret_val = func(params)
        rc = ret_val if isinstance(ret_val, int) else 0
        if rc == 0:
            logging.info(f"Task succeeded: {task_name} rc={rc}")
        else:
            logging.error(f"Task failed: {task_name} rc={rc}")
    except Exception:
        rc = -1
        logging.error(f"Task raised exception: {task_name}\n{traceback.format_exc()}")
        ret_val = None
    finally:
        end_ts = time.time()
        end_dt = fmt_ts(end_ts)
        elapsed = fmt_duration(end_ts - start_ts)
        try:
            running_proxy.pop(pid, None)
        except Exception:
            pass
        completed_proxy.append({
            "task": task_name,
            "return_code": rc,
            "pid": pid,
            "start_dt": start_dt,
            "end_dt": end_dt,
            "elapsed": elapsed,
            "log_path": os.path.abspath(log_path),
        })

    return index, task_name, rc, ret_val

# -------------------------------
# Summary writer (Markdown)
# -------------------------------

def _render_summary_md(running: Dict[int, dict], completed: List[dict]) -> str:
    now = time.time()
    now_dt = fmt_ts(now)
    lines = []
    lines.append(f"# Multiprocessing Pool Monitor")
    lines.append(f"_Last update: **{now_dt}**_")
    lines.append("")
    # Running
    lines.append("## Running")
    if running:
        lines.append("| Process | Task | Start Time | Elapsed | Log Path |")
        lines.append("|---:|---|---|---:|---|")
        for pid, info in running.items():
            elapsed = fmt_duration(now - info.get("start_ts", now))
            lines.append(f"| PID {pid} | {info.get('task','')} | {info.get('start_dt','')} | {elapsed} | `{info.get('log_path','')}` |")
    else:
        lines.append("_(none)_")
    lines.append("")

    # Completed
    lines.append("## Completed")
    if completed:
        lines.append("| # | Task | Return Code | Process | Start | End | Duration | Log Path |")
        lines.append("|---:|---|---:|---:|---|---|---:|---|")
        for i, it in enumerate(list(completed), start=1):
            rc = it.get("return_code", 1)
            lines.append(
                f"| {i} | {it.get('task','')} | {rc} | PID {it.get('pid','')} | "
                f"{it.get('start_dt','')} | {it.get('end_dt','')} | {it.get('elapsed','')} | `{it.get('log_path','')}` |"
            )
    else:
        lines.append("_(none)_")
    lines.append("")
    lines.append("> Note: return code 0 = success; non-zero = failure; -1 = exception.")
    return "\n".join(lines)

def _summary_writer_loop(status_store, summary_path: str, refresh_interval: float, stop_event: Event):
    ensure_parent_dirs(summary_path)
    while not stop_event.is_set():
        try:
            running = dict(status_store["running"])
            completed = list(status_store["completed"])
            content = _render_summary_md(running, completed)
            tmp_path = summary_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, summary_path)  # atomic
        except Exception as e:
            print(f"[WARN] summary writer error: {e}")
        finally:
            stop_event.wait(refresh_interval)

    # Final write on stop
    try:
        running = dict(status_store["running"])
        completed = list(status_store["completed"])
        content = _render_summary_md(running, completed)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"[WARN] final summary write error: {e}")

# -------------------------------
# Orchestrator (no web server)
# -------------------------------

def run_with_pool_file_monitor(
    func: Callable,
    task_names: List[str],
    log_paths: List[str],
    params_list: List[Any],
    processes: int = None,
    summary_path: str = "./monitor_summary.md",
    refresh_interval: float = 1.0,
) -> Tuple[Dict[str, int], List[Any]]:
    """
    Run tasks in a process pool and continuously write a Markdown summary to `summary_path`.

    Returns:
        (return_codes_by_task, return_values_in_order)
        - return_codes_by_task: Dict[str, int]
        - return_values_in_order: List[Any], aligned with task_names/params_list order.
    """
    assert len(task_names) == len(log_paths) == len(params_list), "Lengths of task_names, log_paths, params_list must match"

    mp_ctx = get_context("spawn")
    manager: SyncManager = mp_ctx.Manager()

    status_store = manager.dict()
    status_store["running"] = manager.dict()
    status_store["completed"] = manager.list()

    # Start summary writer thread
    stop_event = Event()
    writer_thread = Thread(
        target=_summary_writer_loop,
        args=(status_store, summary_path, refresh_interval, stop_event),
        daemon=True,
    )
    writer_thread.start()
    print(f"[INFO] Writing live summary to: {os.path.abspath(summary_path)} (every {refresh_interval:.1f}s)")

    # Build args with index to preserve ordering
    args_iter = [
        (idx, func, tname, params, lpath, status_store["running"], status_store["completed"])
        for idx, (tname, lpath, params) in enumerate(zip(task_names, log_paths, params_list))
    ]

    return_codes_by_task: Dict[str, int] = {}
    return_values_in_order: List[Any] = [None] * len(task_names)

    try:
        # Use mp_ctx.Pool (do NOT pass context= to top-level Pool)
        with mp_ctx.Pool(processes=processes) as pool:
            async_results = [pool.apply_async(_worker, args=a) for a in args_iter]

            # Collect results as workers finish; place by index to keep order
            for ar in async_results:
                idx, tname, rc, ret_val = ar.get()
                return_codes_by_task[tname] = rc
                return_values_in_order[idx] = ret_val
    finally:
        # Stop writer thread and finalize one last write
        stop_event.set()
        writer_thread.join(timeout=5)

    print("[INFO] All tasks finished. Return codes:")
    for tname in task_names:
        print(f" - {tname}: {return_codes_by_task.get(tname)}")

    return return_codes_by_task, return_values_in_order

# -------------------------------
# Example task
# -------------------------------

def example_task(x: int, y: int, delay: float = 0.5) -> int:
    logging.info(f"Computing {x} + {y}")
    time.sleep(delay)
    s = x + y
    logging.info(f"Sum = {s}")
    # Succeed on even results, fail on odd
    return 0 if (s % 2 == 0) else 1

# -------------------------------
# Demo
# -------------------------------

if __name__ == "__main__":
    func = example_task

    task_names = [f"task_{i}" for i in range(1, 7)]
    log_paths = [f"./data/__tmp/{name}.log" for name in task_names]
    params_list = [
        (1, 1, 0.8),
        (2, 2, 1.2),
        (3, 3, 0.5),
        (4, 5, 0.9),
        (10, 1, 0.4),
        (6, 7, 15),
    ]

    rc_map, ordered_vals = run_with_pool_file_monitor(
        func=func,
        task_names=task_names,
        log_paths=log_paths,
        params_list=params_list,
        processes=None,  # default: CPU count
        summary_path="./data/__tmp/monitor_summary.md",
        refresh_interval=1.0,
    )

    print("[INFO] Ordered return values:", ordered_vals)
