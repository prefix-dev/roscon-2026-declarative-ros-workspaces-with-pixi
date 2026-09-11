# A runtime image built from the same lockfile the team develops against.
#
#     docker build -t turtle-dancer:latest .
#     docker run --rm turtle-dancer:latest
#
# The build stage has Pixi; the final stage does not. It only carries the
# resolved environment, so nothing in the image can drift from pixi.lock.

FROM ghcr.io/prefix-dev/pixi:0.80.0-noble AS build

WORKDIR /app
COPY . .

# Install the dependencies for the robot environment, make sure it's locked
RUN pixi FIXME

# Bake the activation shell-hook into a script, so the runtime stage needs no Pixi.
RUN pixi FIXME

FROM ubuntu:26.04 AS runtime

COPY --from=build FIXME
COPY --from=build /shell-hook.sh /shell-hook.sh
COPY --from=build /app/src /app/src

WORKDIR /app
ENTRYPOINT ["/bin/bash", "/shell-hook.sh"]
CMD ["ros2", "run", "turtle_dancer", "dance"]