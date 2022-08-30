# E-paper-TaskList

RaspberryPiと Waveshare e-paper 7.5inchを使用して予定表を表示するプロジェクトです。

## Usage

- RaspberryPi zero WH (RaspberryPi OS lite)
- [7.5inch e-Paper HAT - Waveshare Wiki](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)


## Example

電子ペーパーへの表示をする前に表示用画像(480*800)を生成して確認することができます。
/imaoge.bmp を確認してください。
```sh
$ python3 create_image.py

```

バッチファイルを実行すると、電子ペーパーに反映されます。
```sh
$ bash run.sh
```




## License
Copyright (c) 2022 Tiger

This software is released under the MIT License, see LICENSE.
