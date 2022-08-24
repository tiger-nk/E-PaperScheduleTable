import create_image
from lib import epd7in5_V2

def main():
    image = create_image.create()
    epd = epd7in5_V2.EPD()
    epd.init()
    # 画面をクリアする
    epd.Clear()
    # 画像をディスプレイに描画
    epd.display(epd.getbuffer(image))
    # 電力供給OFF
    epd.sleep()

if __name__ == '__main__':
    main()