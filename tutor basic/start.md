# Dùng Tutor để build Open edX

---

## 1. Cài tutor

```shell
pip install "tutor[full]==15.3.6"
```

---

## 2. Tạo file config

```shell
tutor config save # tạo file config
```

Câu lệnh trên tạo folder `~/.local/share/tutor`, trong đây có:

- `config.yml`: file config chính, chứa environment variables Tutor tự tạo cho bạn như tên app, pass mysql,...
- folder `env` chứa nhiều thứ, trong đó có:
  - `env/build/openedx/Dockerfile`: file docker dùng để build image `openedx`.
  - `env/plugins/mfe/build/mfe/Dockerfile`: file docker dùng để build image `mfe`. (Mình không biết nó được tạo luôn hay đến bước sau mới được tạo)

---

## 3. Sửa file `config.yml`

```yml
MYSQL_ROOT_PASSWORD: root # optional, do tutor tạo random password, mình không thích nên sửa lại cho dễ nhìn
OPENEDX_MYSQL_PASSWORD: edx # optional, do tutor tạo random password, mình không thích nên sửa lại cho dễ nhìn

# edx-platform
# đây là repo dùng để build image openedx
# thay vì dùng của tutor, ta dùng repo của ta
EDX_PLATFORM_REPOSITORY: https://github.com/uuuuv/edx-platform.git # git repo
EDX_PLATFORM_VERSION: main # branch

# tương tự
# frontend-app-learning
MFE_LEARNING_MFE_APP:
  name: learning
  port: 2000
  repository: https://github.com/FUNiX-Tech/frontend-app-learning # git repo
  version: open-release/olive.master # branch
```

Lưu lại config:

```shell
tutor config save
```

Chạy câu lệnh trên thì tutor sẽ thay các config mình đã khai báo trong `config.yml` vào 2 Dockerfile để build image `openedx` và `mfe`.

---

## 4. Build image `openedx` và `mfe`

```shell
tutor images build openedx # Dùng env/build/openedx/Dockerfile để build => image overhangio/openedx
tutor images build mfe # Dùng env/plugins/mfe/build/mfe/Dockerfile để build => image overhangio/openedx-mfe
```

## 5. Launch edx

```shell
tutor local launch
```

Tạo superusser:

```shell
tutor local do createuser --staff --superuser admin admin@openedx.com
```

