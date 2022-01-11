# docker-superset
Superset Docker image that works on a Swarm stack deployment.

## Objectives 

I want:
* to build a standard Docker image using only the apache/superset repo files.
* to publish the standard image on Docker Hub named computablefacts/superset-for-swarm
* to have a Swarm stack YAML file that use this image and works out of the box.
* to build my own custom Docker image to add database drivers or other specific stuff
* to publish the custom image on Docker Hub named computablefacts/superset-for-swarm-custom

## Usage

Copy the `swarm-stack.yaml` on your Docker Swarm manager and launch:

```bash
$ docker stack deploy --compose-file swarm-stack.yaml my-superset-stack
```

You can choose the superset image by changing:
```yaml
x-superset-image: &superset-image computablefacts/superset-for-swarm:1.3.0
```
with another version
```yaml
x-superset-image: &superset-image computablefacts/superset-for-swarm:1.3.2
```
or with your custom image
```yaml
x-superset-image: &superset-image my-user/my-custom-image:latest
```

You can test the Swarm stack locally. Clone this repo first and change the `ports` setting 
in the `swarm-stack.yaml` file like this (uncomment the `mode` key):
```yaml
    ports:
      - target: 8088
        published: 8088
        protocol: tcp
# Uncomment below to test locally on http://localhost:8088/
        mode: host
```
Start the stack with:
```shell
# Turn your local Docker on a Swarm
$ docker swarm init
# Launch the stack
$ docker stack deploy --compose-file swarm-stack.yaml my-local-superset-stack
```

Superset should be accessible on http://localhost:8088/

## More details

### How the Docker Swarm stack is built

TODO: based on xxx-nodev.yaml but without any external dependencies (no external files needed).
No superset_home volume shared among containers
Celery workers should work


### How the standard image is built

TODO

### How to update the Docker images from a new superset version

#### Update the superset files

Checkout the [apache/superset repo](https://github.com/apache/superset) on the new version.

```shell
$ git clone git@github.com:apache/superset.git
$ git checkout 1.3.0
```

Copy the bash scripts from superset/docker into this repo /docker (6 bash scripts).

Copy the config file from superset/docker/pythonpath_dev/superset_config.py into this 
repo /docker/pythonpath/superset_config.py.

Modify the superset_config.py to use Redis as the results backend.

```shell
##### Change from original file
#RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")
# Put results on Redis not on a file that is not shared among containers on the Swarm stack
from cachelib.redis import RedisCache
RESULTS_BACKEND = RedisCache(host=REDIS_HOST, port=REDIS_PORT, key_prefix='superset_results')
##### End of change
```
#### Change version tag

On Dockerfile
On custom.dockerfile
On Swarm stack

#### Commit, tag and push

TODO

