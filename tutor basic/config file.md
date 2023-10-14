# Tutor `config.yml`

`config.yml` file chứa toàn bộ biến môi trường cho các file trong folder `env`, như Dockerfile, `lms.env.yml`, `cms.env.yml`.

Mỗi khi sửa file `config.yml`, cần chạy `tutor config save` để apply các thay đổi vào folder `env`.

Bạn có thể xóa folder `env` rồi chạy `tutor config save` để tạo lại.

Nếu bạn thay đổi các biến môi trường trong folder `env` thì cuối cùng nó cũng sẽ bị override bởi `config.yml` => do đó sửa `config.yml` > `tutor config save` chứ không sửa trực tiếp vào folder `env`.

Thay vì sửa bằng tay, bạn cũng có thể sửa bằng command:

```shell
tutor config save --set VARIABLE=<VALUE>
```

Một số environment variables không set trong `config.yml` được thì phải dùng Tutor plugins. 