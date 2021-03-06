#!/bin/sh
# Get the registration token from:
# http://host.docker.internal:8080/root/${project}/settings/ci_cd

registration_token=XXXXXXXXXXXXXXXXX

docker exec -it gitlab-runner1 \
  gitlab-runner register \
    --non-interactive \
    --registration-token ${registration_token} \
    --locked=false \
    --description docker-stable \
    --url http://host.docker.internal\
    --executor docker \
    --docker-image docker:stable \
    --docker-volumes "/var/run/docker.sock:/var/run/docker.sock" \
    --docker-network-mode gitlab-network
