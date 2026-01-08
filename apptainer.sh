IMAGE="${1:-$HOME/image/apptainer/sbpy.sif}"

export PATH_STR=/root/.cargo/bin
export PATH_STR=$PATH_STR:/opt/maven/bin
export PATH_STR=$PATH_STR:/root/.local/bin
export PATH_STR=$PATH_STR:/root/.pyenv/bin
export PATH_STR=$PATH_STR:/root/.pyenv/shims
export PATH_STR=$PATH_STR:/usr/local/sbin
export PATH_STR=$PATH_STR:/usr/local/bin
export PATH_STR=$PATH_STR:/usr/sbin
export PATH_STR=$PATH_STR:/usr/bin
export PATH_STR=$PATH_STR:/sbin
export PATH_STR=$PATH_STR:/bin

apptainer shell --cleanenv \
  --env JAVA_HOME=/usr \
  --env SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
  --env PYTHONPATH=. \
  --env LC_ALL=C.UTF-8 \
  --env LANG=C.UTF-8 \
  --env PATH="$PATH_STR" \
  --env PI_WORKDIR="$PI_WORKDIR" \
  --env OPENAI_API_KEY="$OPENAI_API_KEY" \
  --env ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  --env DASHSCOPE_API_KEY="$DASHSCOPE_API_KEY" \
  --env AWS_BEARER_TOKEN_BEDROCK="$AWS_BEARER_TOKEN_BEDROCK" \
  --env GITHUB_TOKEN="$GITHUB_TOKEN" \
  --env HF_HOME="$HF_HOME" \
  --env HF_TOKEN="$HF_TOKEN" \
  "$IMAGE"
