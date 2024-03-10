# face validator

## Setup

### Requirements

- Python 3.11
- Docker 

1. clone the project

    ```bash
    git clone https://github.com/PascaII/face-validator.git
    ```

2. start the project with docker (can take a lot of time on the first build)

    ```bash
    docker compose up --build
    ```

3. open the [docs](http://localhost:8007/docs)


## Endpoints

The python FastAPI offers two endpoints:

| Request-Type | Path           | Body      | Description                    |
|--------------|----------------|-----------|--------------------------------|
| **GET**      | /heartbeat     | -         | Returns status of the service  |
| **POST**     | /image/process | .png file | Processes image and returns it |

### Parameters for "image/process"

| Parameter    | Default | Type    | Description                                                                                                              |
|--------------| ---- |---------|--------------------------------------------------------------------------------------------------------------------------|
| bounds       | False | boolean | allows visible images edges                                                                                              |
| side_spacing | 0.72 | number  | distance of eyes to the edge <br> 0 = eyes on the edge <br> 0.9998 = eyes centered                                       |
| top_spacing  | 0.4 | number  | vertical position of the eyes <br> 0 = eyes on the upper edge <br> 0.9998 = eyes on the lower edge                       |
| width        | 512 | integer | width of the final image                                                                                              |
| height       | 640 | integer | height of the final image                                                                                                 |
| mask_method  | multiclass | string  | method used for background removal <br>multiclass = more accurate, slower <br> selfie = faster, less accurate |


## System components / Frameworks


![Static Badge](https://img.shields.io/badge/Mediapipe-0.10.8-lightblue?logo=google)

![Static Badge](https://img.shields.io/badge/dlib-19.24.2-green?logo=dlib)

![Static Badge](https://img.shields.io/badge/FastAPI-0.105.0-darkgreen?logo=fastapi)
