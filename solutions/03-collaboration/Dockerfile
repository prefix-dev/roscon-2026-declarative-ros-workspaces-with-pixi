# A runtime image built from the same lockfile the team develops against.
#
#     docker build -t turtle-dancer:latest .
#     docker run --rm turtle-dancer:latest
#
# The build stage has Pixi; the final stage does not. It only carries the
# resolved environment, so nothing in the image can drift from pixi.lock.

FROM ghcr.io/prefix-dev/pixi:0.77.0-noble AS build

WORKDIR /app
COPY . .

# --locked refuses to solve: if pixi.lock does not match pixi.toml, the build
# fails instead of quietly installing something else.
RUN pixi install --locked --environment robot

# Bake the activation into a script, so the runtime stage needs no Pixi.
RUN pixi shell-hook --environment robot -s bash > /shell-hook.sh \
    && echo 'exec "$@"' >> /shell-hook.sh

FROM ubuntu:26.04 AS runtime

COPY --from=build /app/.pixi/envs/robot /app/.pixi/envs/robot
COPY --from=build /shell-hook.sh /shell-hook.sh
COPY --from=build /app/src /app/src

WORKDIR /app
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
CMD ["dance"]
