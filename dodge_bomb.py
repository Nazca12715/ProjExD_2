import os
import sys
import pygame as pg
def check_bound(rect):
    inx = 0 <= rect.left and rect.right <= WIDTH
    iny = 0 <= rect.top  and rect.bottom <= HEIGHT
    return inx, iny

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に半透明の黒い画面上に「Game Over」と表
    示し，泣いているこうかとん画像を貼り付ける関数
    """

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
    """

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    import random
    bb_img = pg.Surface((20, 20))              
    bb_img.set_colorkey((0, 0, 0))             
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  
    bb_rct = bb_img.get_rect()  
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5     

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
        bb_rct.move_ip(vx, vy)
        inx, iny = check_bound(bb_rct)
        if not inx:
            vx *= -1
        if not iny:
            vy *= -1
        
        if kk_rct.colliderect(bb_rct):
            return

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
