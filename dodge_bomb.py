import os
import sys
import pygame as pg
import time
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect):
    inx = 0 <= rect.left and rect.right <= WIDTH
    iny = 0 <= rect.top  and rect.bottom <= HEIGHT
    return inx, iny

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に半透明の黒い画面上に「Game Over」と表
    示し，泣いているこうかとん画像を貼り付ける関数
    """
    overlay = pg.Surface(screen.get_size())
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    kk_cry = pg.transform.rotozoom(pg.image.load("fig/8.png"),0, 0.9)
    img_w, img_h = kk_cry.get_size()

    font = pg.font.Font(None, 100)
    txt = font.render("Game Over", True, (255,255,255))
    txt_w, txt_h = txt.get_size()

    spacing = 20
    total_w = img_w + spacing + txt_w + spacing + img_w
    x = (WIDTH - total_w) // 2
    y = HEIGHT // 2

    screen.blit(kk_cry, (x, (y - img_h //2)))
    screen.blit(txt, (x + img_w + spacing, y - txt_h //2))
    screen.blit(kk_cry, (x + img_w + spacing + txt_w + spacing, (y - img_h //2)))
    pg.display.update
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    移動量の合計値タプルに対応する向きの画像Surfaceを返す
    """

def calc_orientation(org: pg.Rect, dst: pg.Rect,
current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    orgから見て, dstがどこにあるかを計算し, 方向ベクトルをタプルで返す
    """

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))              
    bb_img.set_colorkey((0, 0, 0))             
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  
    bb_rct = bb_img.get_rect()  
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5     
    bb_imgs, bb_accs = init_bb_imgs()

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        DELTA = {
            pg.K_UP:    ( 0, -5),
            pg.K_DOWN:  ( 0,  5),
            pg.K_LEFT:  (-5,  0),
            pg.K_RIGHT: ( 5,  0),
        }
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, (dx, dy) in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += dx
                sum_mv[1] += dy
        prev_kk = kk_rct.copy()
        kk_rct.move_ip(sum_mv)

        inx, iny = check_bound(kk_rct)
        if not (inx and iny):
            kk_rct = prev_kk

        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]
        center = bb_rct.center
        bb_rct = bb_img.get_rect(center=center)
        bb_rct.move_ip(avx, avy)
        inx, iny = check_bound(bb_rct)
        if not inx:
            vx *= -1
        if not iny:
            vy *= -1
        
        if kk_rct.colliderect(bb_rct):
            gameover(screen)

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
