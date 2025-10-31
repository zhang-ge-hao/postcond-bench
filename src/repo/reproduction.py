import os
from openai import OpenAI
from dataclasses import dataclass
import subprocess
import logging
from src.runner import testsuite_run
from src.runner.python import (
    _ensure_poetry_virtualenv_in_project,
    _get_env
)

from src.util import change_dir

@dataclass
class Result:
    success: bool
    log: str
    timeout: bool = False
    flag: str = None


class ChatSession:
    def __init__(self, repo_dir, init_prompt_path, follow_prompt_path, config_file_name):
        self.repo_dir = repo_dir
        self.client = OpenAI()
        self.config_path = os.path.join(repo_dir, config_file_name)
        with open(init_prompt_path) as file:
            self.init_fmt = "".join(file.readlines())
        with open(follow_prompt_path) as file:
            self.follow_fmt = "".join(file.readlines())

    def _new_message(self, messages: list, prompt) -> Result:
        messages.append({"role": "user", "content": prompt})
        logging.info(f"\n{'=' * 30}\n prompt\n{'=' * 30}\n" + \
                     f"{prompt}\n{'=' * 30}")
        try:
            completion = self.client.chat.completions.create(
                model="o4-mini", 
                # model="gpt-4o-mini", 
                messages=messages)
            response = completion.choices[0].message.content
            logging.info(f"\n{'=' * 30}\n response\n{'=' * 30}\n" + \
                         f"{response}\n{'=' * 30}")
            messages.append({"role": "assistant", "content": response})
            return Result(True, response)
        except:
            return Result(False, "")

    def start_session(self, messages) -> Result:
        assert isinstance(messages, list) and len(messages) == 0
        with open(self.config_path) as file:
            original_config = "".join(file.readlines())
        prompt = self.init_fmt.format(original_config=original_config)
        return self._new_message(messages, prompt)

    def further_question(self, messages, error_message, flag) -> Result:
        assert isinstance(messages, list) and len(messages) > 0
        assert flag is not None and isinstance(flag, str)
        prompt = self.follow_fmt.format(error_message=error_message, flag=flag)
        return self._new_message(messages, prompt)


class Reproduction:

    def postprocess_response(self, response: str) -> Result:
        block_mark_count = 0
        for line in response.split("\n"):
            if line.strip().startswith("```"):
                block_mark_count += 1
        if block_mark_count == 0:
            return Result(True, response)
        elif block_mark_count == 2:
            commands = ""
            block_opened = False
            for line in response.split("\n"):
                if line.strip().startswith("```"):
                    block_opened = (not block_opened)
                elif block_opened:
                    commands += line + "\n"
            return Result(True, commands)
        else:
            logging.error(response)
            return Result(False, "Postprocess failed.")

    def script_run(self, script: str) -> Result:
        raise NotImplementedError()

    def check_prerequisites(self) -> bool:
        raise NotImplementedError()

    def response_run(self, response: Result) -> Result:
        if not response.success:
            return response
        postprocess_result = \
            self.postprocess_response(response.log)
        if not postprocess_result.success:
            return postprocess_result
        script = postprocess_result.log
        return self.script_run(script)

    def run(self) -> Result:
        with change_dir(self.repo_dir):
            if not self.check_prerequisites():
                return Result(False, "Prerequisites failed.")
            if self.config_file_name == "pyproject.toml":
                _ensure_poetry_virtualenv_in_project()
            messages = []
            cli_result: Result = None
            for idx in range(self.chat_rounds):
                logging.info(f"Round {idx} started.")
                previous_length = len(messages)
                logging.info(f"previous_length: {previous_length}.")
                if previous_length == 0:
                    response = self.chat_session.start_session(messages)
                else:
                    response = self.chat_session.further_question(
                        messages, cli_result.log, cli_result.flag)
                if response.success:
                    logging.info(f"Chat idx {idx} successed.")
                    cli_result = self.response_run(response)
                    if cli_result.timeout:
                        logging.error("cmd timeout. reproduction failed.")
                        return cli_result
                    if cli_result.success:
                        logging.info(cli_result.log)
                        logging.info("reproduction success.")
                        return Result(True, "")
                    elif cli_result.log == "Postprocess failed.":
                        logging.error("Postprocess failed.")
                        return cli_result
                else:
                    logging.info(f"Chat idx {idx} failed.")
                    logging.error(response.log)
                    messages = messages[: previous_length]
            return cli_result


class PoetryReproduction(Reproduction):
    def __init__(self, repo_dir, init_prompt_path, follow_prompt_path):
        self.repo_dir = repo_dir
        self.config_file_name = "pyproject.toml"
        self.chat_session = ChatSession(
            repo_dir, init_prompt_path, follow_prompt_path,
            self.config_file_name)
        self.chat_rounds = 10
        self.config_path = os.path.join(
            repo_dir, self.config_file_name)

    def check_prerequisites(self) -> bool:
        if not os.path.exists(self.config_path):
            return False
        if not (os.path.isdir("test") or os.path.isdir("tests")):
            return False
        with open(self.config_path) as file:
            for line in file:
                if line.strip() == "[project]":
                    return True
        return False

    def script_run(self, cmd: str) -> Result:
        # Run the command, capturing both stdout and stderr
        try:
            env = _get_env()
            result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=200,
                text=True,
                env=env)
        except subprocess.TimeoutExpired:
            return Result(False, "Timeout.", timeout=True)
        # Determine success based on return code
        test_result = testsuite_run(lang="python", timeout=200)
        success = test_result.to_flag() in ["passed", "local_crash", "failed"]
        logging.info(f"\n{'=' * 30}\n flag\n{'=' * 30}\n{test_result.to_flag()}")
        # TODO use result.stdout here for now
        with open(self.config_path) as file:
            config_content = file.read()
        feedback = f"""
Current config file:
```
{config_content}
```
STDOUT from your commands:
```
{result.stdout}
```
STDOUT from `poetry install` and `pytest` commands:
```
{test_result.stdout}
```
"""
        return Result(success, feedback, flag=test_result.to_flag())


class MavenReproduction(Reproduction):
    def __init__(self, repo_dir, init_prompt_path, follow_prompt_path):
        self.repo_dir = repo_dir
        self.config_file_name = "pom.xml"
        self.chat_session = ChatSession(
            repo_dir, init_prompt_path, follow_prompt_path,
            self.config_file_name)
        self.chat_rounds = 10
        self.config_path = os.path.join(repo_dir, self.config_file_name)
        self.src_path = os.path.join(repo_dir, "src")
        self.script_name = os.path.join(repo_dir, "edit.py")

    def check_prerequisites(self) -> bool:
        if not os.path.exists(self.src_path) \
                or not os.path.exists(self.config_path):
            return False
        return True

    def script_run(self, script: str) -> Result:
        try:
            # Run the script to edit the pom.xml
            with open(self.script_name, "w") as file:
                file.write(script)
            result = subprocess.run(
                f"python {self.script_name}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=200,
                text=True)
        except subprocess.TimeoutExpired:
            return Result(False, "Timeout.", timeout=True, flag="Your script timeout!")
        # Determine success based on return code
        if result.returncode != 0:
            return Result(False, result.stdout, flag="Your script failed!")
        test_result = testsuite_run(lang="java", fatjar_mode=False, timeout=200)
        success = test_result.to_flag() in ["passed", "local_crash", "failed"]
        logging.info(f"\n{'=' * 30}\n flag\n{'=' * 30}\n{test_result.to_flag()}")
        feedback = f"```\n{test_result.test_summary}\n```"
        # NOTE use summary here
        return Result(success, feedback, flag=test_result.to_flag())
    