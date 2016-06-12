## A http client to create and push gce image

### create and push image 

#### url
/image/BuildPush

#### http method
post

#### para
| paraname | example | desc |
| -------- | :-----: | ----:|
| app_type | jdk1.7_resin | N/A |
| app_name | tethys  |  N/A |
| owner    | zhangxing | N/A |

#### example

    curl -d "owner=zhangxing&app_type=jdk1.7_resin&app_name=tethys"   http://127.0.0.1:9999/image/build





