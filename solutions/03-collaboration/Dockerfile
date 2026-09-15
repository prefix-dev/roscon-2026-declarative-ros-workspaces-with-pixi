# A runtime image built from the same lockfile the team develops against.
#
#     docker build -t ros-demo-team:latest .
#     docker run --rm ros-demo-team:latest
#
# The build stage has Pixi; the final stage does not. It only carries the
# resolved environment, so nothing in the image can drift from pixi.lock.

FROM ghcr.io/prefix-dev/pixi:0.80.0-noble AS build

WORKDIR /app
COPY pixi.toml pixi.lock ./

RUN pixi install --locked

# Bake the activation into a script, so the runtime stage needs no Pixi.
RUN pixi shell-hook -s bash > /shell-hook.sh \
    && echo 'exec "$@"' >> /shell-hook.sh

FROM ubuntu:26.04 AS runtime

COPY --from=build /app/.pixi/envs/default /app/.pixi/envs/default
COPY --from=build /shell-hook.sh /shell-hook.sh

WORKDIR /app
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
CMD ["ros2", "run", "demo_nodes_cpp", "talker"]
