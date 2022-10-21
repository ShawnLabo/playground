# Spring Boot - Cloud Run and Spanner

## 作るもの

![image](https://user-images.githubusercontent.com/1286807/195768261-41f59dca-f1ad-46fa-bc2b-a31dcb2d1d08.png)

## 環境

* OpenJDK 17.0.2
* Gradle 7.5.1

## Spring Boot 初期設定

### Spring Boot 初期化

https://github.com/ShawnLabo/playground/pull/1/commits/81c5f4a7256e7ceeb2b38766151974006bff71a5

* https://start.spring.io/ にアクセスする
* 設定してzipをダウンロード
  * ![image](https://user-images.githubusercontent.com/1286807/195762882-c949ea3e-85f5-4adc-a86b-55534628cf78.png)
* 適当なディレクトリに展開する

### 動作確認

https://github.com/ShawnLabo/playground/pull/1/commits/4643bc460e40a47ed44f5f286a65bfcb3ac599f8

ファイルを追加: `src/main/java/tube/shawn/java/demo/HelloMessage.java`

```java
package tube.shawn.java.demo;

import lombok.Getter;

public class HelloMessage {
    @Getter private final String message;

    public HelloMessage(String message) {
        this.message = message;
    }
}
```

ファイルを追加: `src/main/java/tube/shawn/java/demo/HelloController.java`

```java
package tube.shawn.java.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
    private static final String template = "Hello, %s!";

    @GetMapping("/hello")
    public HelloMessage hello(@RequestParam(value = "name", defaultValue = "World") String name) {
        return new HelloMessage(String.format(template, name));
    }
}
```

Spring Boot を起動

```sh
./gradlew bootRun
```

http://localhost:8080/hello


## Google Cloud 設定

gcloud コマンドにプロジェクトを設定

```sh
gcloud config set project YOUR-PROJECT-ID
```

各種サービスの有効化

```sh
gcloud services enable spanner.googleapis.com run.googleapis.com artifactregistry.googleapis.com
```

Cloud Run サービス用の Service Account を作成

```sh
gcloud iam service-accounts create spring-demo
```

Spanner インスタンス作成

```sh
gcloud spanner instances create spring-demo \
  --config regional-asia-northeast1 \
  --description "Spring Boot demo" \
  --processing-units 100
```

Spanner データベース作成

```sh
gcloud spanner databases create spring-demo \
  --instance spring-demo
```

Service Account にデータベースのユーザー権限を付与

```sh
gcloud spanner databases add-iam-policy-binding spring-demo \
  --instance spring-demo \
  --member serviceAccount:spring-demo@$(gcloud config get-value project).iam.gserviceaccount.com \
  --role roles/spanner.databaseUser
```

## Spring Data Spanner の利用

`build.gradle` に依存ライブラリを追加

```groovy
dependencies {
    // ...
    implementation 'com.google.cloud:spring-cloud-gcp-data-spanner:3.3.0'
    // ...
}
```

参考:

* [Maven Repository: com.google.cloud » spring-cloud-gcp-data-spanner » 3.3.0](https://mvnrepository.com/artifact/com.google.cloud/spring-cloud-gcp-data-spanner/3.3.0)