# Flask-API-Model-Deployment-Tutorial
Tutorial for Model Deployment using Flask on Google Cloud

## Instalation Guide
1. Download or clone this repository
2. Unzip/extract all file
3. Build Docker image using
    ```
    docker buildx build -f Dockerfile -t <your-docker-image-name> .
    ```
4. Run it
    ```
    docker run <your-docker-image-name>
    ```
 
## Testing on Postman
### 1. Normal Version
#### Method: POST
>```
>http://127.0.0.1:5321/predict
>```
#### Body form data

|Param|value|Type|
|---|---|---|
|image|/D:/Skripsi/Bismillah/Analisis/Dataset/Test/Positive/16001.jpg|file|
|model_name|concrate|text|
|offset|7|text|
|user_id|112448|text|

#### Response
```json
{
    "User_ID": "112448",
    "condition": "Positive",
    "confidence": 1.0,
    "time": "2024-04-17 17:22:19 UTC"
}
```




## 2. Without user_id
### Method: POST
>```
>http://127.0.0.1:5321/predict
>```
### Body form data

|Param|value|Type|
|---|---|---|
|image|/D:/Skripsi/Bismillah/Analisis/Dataset/Test/Positive/16010.jpg|file|
|model_name|concrate|text|
|offset|7|text|
|user_id||text|

### Response
```json
{
    "error": "No user id provided"
}
```




## 3. Without offset
### Method: POST
>```
>http://127.0.0.1:5321/predict
>```
### Body form data

|Param|value|Type|
|---|---|---|
|image|/D:/Skripsi/Bismillah/Analisis/Dataset/Test/Positive/16009.jpg|file|
|model_name|concrate|text|
|offset||text|
|user_id|112448|text|

### Response
```json
{
    "error": "No offset provided"
}
```




## 4. Without model_name
### Method: POST
>```
>http://127.0.0.1:5321/predict
>```
### Body form data

|Param|value|Type|
|---|---|---|
|image|/D:/Skripsi/Bismillah/Analisis/Dataset/Test/Positive/16009.jpg|file|
|model_name||text|
|offset|7|text|
|user_id|112448|text|

### Response
```json
{
    "error": "No offset provided"
}
```



## 5. Without image
### Method: POST
>```
>http://127.0.0.1:5321/predict
>```
### Body form data

|Param|value|Type|
|---|---|---|
|image||file|
|model_name|concrate|text|
|offset|7|text|
|user_id|112448|text|

{
    "error": "No image provided"
}


_________________________________________________
Powered By: [postman-to-markdown](https://github.com/bautistaj/postman-to-markdown/)
