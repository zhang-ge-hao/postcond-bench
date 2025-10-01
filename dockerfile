# 使用 ubuntu:22.04 作为基础镜像
FROM ubuntu:22.04

# 避免交互式安装时卡住
ENV DEBIAN_FRONTEND=noninteractive

# 安装构建 Python 所需依赖及常用工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential curl wget git ca-certificates bash \
      libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
      libncurses5-dev libgdbm-dev libnss3-dev libffi-dev liblzma-dev \
      zip unzip && \
    rm -rf /var/lib/apt/lists/*

# 安装 pyenv 用于管理和编译多版本 Python
ENV PYENV_ROOT="/root/.pyenv" \
    PATH="/root/.pyenv/bin:/root/.pyenv/shims:$PATH"
RUN git clone https://github.com/pyenv/pyenv.git ${PYENV_ROOT} && \
    # 安装 python-build 插件（可选）
    mkdir -p ${PYENV_ROOT}/plugins && \
    git clone https://github.com/pyenv/pyenv-virtualenv.git ${PYENV_ROOT}/plugins/pyenv-virtualenv

# 构建 Python 3.6–3.11
RUN for ver in 3.6.15 3.7.13 3.8.13 3.9.13 3.10.11 3.11.5; do \
      pyenv install ${ver}; \
    done && \
    # 设置全局默认 Python 版本
    pyenv global 3.11.5

# 安装 Poetry
RUN curl -sSL https://install.python-poetry.org | python3 && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.in-project true

# 安装 Eclipse Temurin JDK 21
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-21-jdk && \
    rm -rf /var/lib/apt/lists/*

# 安装 Maven 3.9.x
ENV MAVEN_VERSION=3.9.5
RUN wget -q https://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz && \
    tar -xzf apache-maven-${MAVEN_VERSION}-bin.tar.gz -C /opt && \
    ln -s /opt/apache-maven-${MAVEN_VERSION} /opt/maven && \
    rm apache-maven-${MAVEN_VERSION}-bin.tar.gz && \
    { echo 'export MAVEN_HOME=/opt/maven'; echo 'export PATH=${MAVEN_HOME}/bin:${PATH}'; } \
      >> /etc/profile.d/maven.sh

# 安装 Gradle（这里使用 8.3，可改为你需要的最新稳定版本）
ENV GRADLE_VERSION=8.3
RUN wget -q https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip && \
    unzip gradle-${GRADLE_VERSION}-bin.zip -d /opt && \
    ln -s /opt/gradle-${GRADLE_VERSION} /opt/gradle && \
    rm gradle-${GRADLE_VERSION}-bin.zip && \
    { echo 'export GRADLE_HOME=/opt/gradle'; echo 'export PATH=${GRADLE_HOME}/bin:${PATH}'; } \
      >> /etc/profile.d/gradle.sh

# For pygit2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgit2-dev pkg-config build-essential && \
    rm -rf /var/lib/apt/lists/*

# 使用 Bash 登录 shell，以便加载 pyenv、Maven 环境变量
SHELL ["/bin/bash", "-lc"]

# 工作目录
WORKDIR /workspace

# 进入容器时开启登录 shell
CMD ["bash", "-l"]