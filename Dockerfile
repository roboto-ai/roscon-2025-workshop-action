ARG PYTHON_MAJOR=3
ARG PYTHON_MINOR=12
ARG OS_VARIANT=slim-bookworm
FROM public.ecr.aws/docker/library/python:${PYTHON_MAJOR}.${PYTHON_MINOR}-${OS_VARIANT}

# -- INSTALL SYSTEM DEPENDENCIES --
# Uncomment the following RUN instruction and add the package name(s) to the apt-get install command.
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#       <PKG_NAME_1> \
#       <PKG_NAME_2> && \
#     rm -rf /var/lib/apt/lists/*

# -- INSTALL THIRD-PARTY PYTHON LIBRARIES --
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
COPY pyproject.toml ./
RUN uv pip install --system -r pyproject.toml && rm -rf /bin/uv

COPY src/detect_vibration/ ./detect_vibration

# Force the stdout and stderr streams to be unbuffered to decrease latency when viewing real-time action logs
# and to maximize context captured in logs if this action fails.
ENV PYTHONUNBUFFERED=0

ENTRYPOINT [ "python", "-m", "detect_vibration.bin.entrypoint" ]
