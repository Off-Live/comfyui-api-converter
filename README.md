## comfyui-api-converter
This project can convert the comfy's workflow to its api json format.

### Build
```shell
docker build -t comfyui-api-converter -f build.Dockerfile .
```

### Deploy
AWS Beanstalk with Docker environment

- Update the version of the docker image in Dockerrun.aws.json
- Deploy the json file to Beanstalk
