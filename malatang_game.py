import math
import os
import random
import sys
import time
import pygame as pg
from setting import *

pg.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# ---- クラス ------

class Player:
    """
    プレイヤーに関するクラス
    """
    def __init__(self):
        """
        select_list :プレイヤーが選択している商品
        """
        self.select_list = []
        self.bowl = Bowl()
        self.font = pg.font.Font(FONT_PATH,35)

        # 提供ボタンのテキスト
        self.save_txt = self.font.render("提供！(Enter)", True, GOLD)
        self.savetxt_rct = self.save_txt.get_rect()

        # 操作説明ボタンの画像
        self.hint_img = pg.image.load(f"fig/mark_question_yellow.png").convert_alpha()
        self.hint_img = pg.transform.scale(self.hint_img, (50,50))  # 画像のサイズ変更
        self.hint_rct = self.hint_img.get_rect()

        # 各ボタンの状態を示す変数
        self.savebtn_stutas = False
        self.hintbtn_stutas = False

        ## ボタンインスタンスの生成
        # 提供ボタン
        self.save_btn = BUTTON(
            x=self.savetxt_rct.left,
            y=self.savetxt_rct.top,
            width=270,
            height=50,
            color = SCARLET
            )
        # 操作説明ボタン
        self.hint_btn = BUTTON(
            x=self.hint_rct.left,
            y=self.hint_rct.top,
            width= (self.hint_rct.right-self.hint_rct.left),
            height= (self.hint_rct.bottom-self.hint_rct.top),
            color=BLACK
        )
        
        # 提供ボタンの座標の調整
        self.save_btn.move_center(centerx= WIDTH*5/6, centery=HEIGHT*24/35+5)
        self.savetxt_rct.center = self.save_btn.get_center()

        # 操作説明ボタンの座標の調整
        self.hint_btn.move_center(centerx=40, centery=HEIGHT/2)
        self.hint_rct.center = self.hint_btn.get_center()


    def add_select(self, goods: object):
        """
        商品を選択してselect_listに商品を追加する
        引数 goods: Goodsオブジェクト
        """
        self.select_list.append(goods.name)

    def get_count(self, name:str) -> int:
        """"
        指定された商品名の現在の個数を返す
        引数 name:商品名
        """
        return self.select_list.count(name)

    def get_select(self) -> list:
        """
        現在の選択内容を返す
        """
        return self.select_list.copy(), self.bowl.get_spicelevel()
    
    def reset(self):
        """
        商品の選択内容をすべて削除する
        """
        self.select_list.clear()
        self.bowl.reset()
        self.btn_stutas = False

    def savebtn_draw(self, screen:pg.Surface):
        """
        提供ボタンとテキストを描画する
        """
        self.savebtn_stutas = True

        # ボタンを描画する
        self.save_btn.draw(screen=screen, frame_color=GOLD)

        # ボタンの上にテキストを表示する
        screen.blit( self.save_txt, self.savetxt_rct)

    def hintbtn_draw(self, screen:pg.Surface):
        """
        ヒントボタンを描画する
        """
        # ボタンを描画する
        self.hint_btn.draw(screen=screen)

        # 画像を表示する
        screen.blit( self.hint_img, self.hint_rct )

class Bowl():
    """
    どんぶりに関するクラス
    """

    def __init__(self):
        self.spices_name = list(spices_dict.values())
        self.index = 0
        self.images = [ 
            pg.transform.scale(pg.image.load(path).convert_alpha(), (350,250)) 
            for path in spices_dict.keys()  
            ]
        self.img = self.images[self.index]
        self.rct = self.img.get_rect()
        self.rct.center = (WIDTH/2,HEIGHT*16/25)


    def draw(self,screen):
        """
        どんぶりを描画するメソッド
        """
        screen.blit(self.img,self.rct)

    def increase_spice(self):
        """
        辛さのレベルとどんぶりの画像を変えるメソッド
        激辛でストップする
        """
        # 末尾に達していない場合のみ変更する
        if self.index < len(self.images) - 1:
            self.index += 1
            self.img = self.images[self.index]

    def get_spicelevel(self) -> str:
        """
        現在の辛さのレベル名(中辛など)を返す
        """
        return self.spices_name[ self.index ]

    def reset(self):
        """
        辛さと画像を初期状態に戻す
        """
        self.index = 0
        self.img = self.images[self.index]

class BUTTON():
    """
    ボタンに関するクラス
    """

    def __init__(self, x, y, width, height, color ,raidius=10):
        self.rct = pg.Rect(x, y, width, height)
        self.color = color
        self.raidius = raidius
        # 各座標を保存
        self.left = self.rct.left
        self.right = self.rct.right
        self.top = self.rct.top
        self.bottom = self.rct.bottom
    
    def move_center(self, centerx, centery):
        """
        中心座標を変更し、更新する
        """
        self.rct.centerx = centerx
        self.rct.centery = centery

        # 座標保存変数の更新
        self.left = self.rct.left
        self.right = self.rct.right
        self.top = self.rct.top
        self.bottom = self.rct.bottom

    def get_center(self) -> tuple:
        """
        現在の中心座標を返す
        """
        return self.rct.centerx, self.rct.centery

    def draw(self, screen:pg.surface, frame_color=None):
        """
        ボタンを描画する
        引数1 screen: screeen
        引数2 frame_color: 枠線の色
        """
        # ボタン本体の描画
        pg.draw.rect(screen, self.color, self.rct, 0, self.raidius)

        # 枠線の色が指定されたときは枠線を表示する
        if frame_color is not None:
            # 枠線の描画
            pg.draw.rect(screen, frame_color, rect=(self.left-self.raidius , self.top+self.raidius, 10, (self.bottom-self.top)-self.raidius*2 ), width=0) #左
            pg.draw.rect(screen, frame_color, rect=(self.right , self.top+self.raidius, 10, (self.bottom-self.top)-self.raidius*2 ), width=0) #右
            pg.draw.rect(screen, frame_color, rect=(self.left+self.raidius , self.top-self.raidius, (self.right-self.left)-self.raidius*2 , 10), width=0) #上
            pg.draw.rect(screen, frame_color, rect=(self.left+self.raidius , self.bottom, (self.right-self.left)-self.raidius*2, 10), width=0) #下
            # 四隅
            pg.draw.rect(screen, frame_color, rect=(self.left , self.top, 10, 10), width=0) #左上
            pg.draw.rect(screen, frame_color, rect=(self.right-self.raidius , self.top, 10, 10), width=0) #右上
            pg.draw.rect(screen, frame_color, rect=(self.right-self.raidius , self.bottom-10, 10, 10), width=0) #右下
            pg.draw.rect(screen, frame_color, rect=(self.left , self.bottom-self.raidius, 10, 10), width=0) #左下

class Goods(pg.sprite.Sprite):
    """
    商品棚に表示する具材を管理するクラス
    """
    def __init__(self, name:str, xy:tuple):
        """
        商品画像を生成する
        引数1 name：商品名
        引数2 xy：商品の表示する位置
        """
        super().__init__()
        # 商品名保存
        self.name = name
        
        # 商品名に対応する画像を読み込む
        self.image = pg.image.load(goods_dic[name]).convert_alpha()
        # 商品画像のサイズを小さく
        self.image = pg.transform.scale(self.image,(200, 180))
        # 商品画像のRectを取得する
        self.rect = self.image.get_rect()
        # 商品の表示位置を設定
        self.rect.center = xy

    def draw_count(self, screen:pg.Surface, count:int, font:pg.font.Font):
        """
        選択個数を描画する
        引数1 screen:スクリーン
        引数2 count:選択個数
        引数3 font:個数表示用のフォント
        """
        # 商品の周囲に赤枠を表示
        pg.draw.rect(screen, BLACK, self.rect.inflate(-60,-60), 5)

        # 個数の表示
        count_txt = font.render(f"×{count}", True, (255,255,255))
        count_rect = count_txt.get_rect()

        # 選択枠の左上に表示
        count_rect = count_txt.get_rect(topright=(self.rect.right - 40, self.rect.top + 20))
        screen.blit(count_txt,count_rect)

class Life:
    """
    残機数を管理・表示するクラス
    """
    def __init__(self, num :int):
        self.num = num  # 残機数を保存
        
         # ハート
        img = pg.image.load("fig/life.png")
        self.image = pg.transform.scale(img, (40, 40))  # 40×40のSurfaceを生成
        self.image.set_colorkey((0, 0, 0))

    def update(self, screen: pg.Surface):
            """
            残基数に応じたハートを画面左上に表示する
            引数 screen：ゲーム画面のSurface
            戻り値：なし
            """
            for i in range(self.num):  # 残基数の分だけ繰り返す
                # ハートを画面の左上から50ピクセル間隔で描画
                screen.blit(self.image, (30+50*i, 150))

class Customer():
    """
    お客さんに関するクラス
    """
    def __init__(self, max:int):
        """
        お客さん画像Surfaceを生成する
        order : 注文内容を管理するインスタンス
        bowl :どんぶりを管理するインスタンス
        """
        self.img = pg.transform.scale(pg.image.load(f"fig/koukaton.png"),(500,500))
        self.activate = True

        self.order = Order(toppings_dict, spices_dict)
        self.order.set_order(max)

    def draw(self, screen:pg.surface):
        """
        お客さん、ふきだし、注文内容を表示するメソッドをまとめて呼び出す
        """
        self.draw_customer(screen)  # お客さんの描画
        self.draw_speech_bubble(screen)  # ふきだし＆注文内容の描画

    def draw_customer(self, screen:pg.surface):
        """
        お客さんを描画するメソッド
        """
        my_rct = self.img.get_rect()
        my_rct.center = (WIDTH/2,HEIGHT/2)

        screen.blit(self.img,my_rct)

    def draw_speech_bubble(self, screen:pg.surface):
        """
        ふきだしを描画するメソッド
        """
        #  ふきだし四角
        my_rect = pg.draw.rect(screen, color=(255,255,255), rect=(WIDTH*2/3,10,350,380), width=0, border_radius=10) #ふきだしぬりつぶし
        left = my_rect.left
        top = my_rect.top
        right = my_rect.right
        bottom = my_rect.bottom
        my_color = (0,0,0)
        try_positions = [
            (left,bottom*5/10),
            (left-40,bottom*6/10),
            (left,bottom*6/10)
            ]

        #  ふきだし枠線
        pg.draw.rect(screen, my_color, rect=(left-10 , top+10, 10, bottom-30), width=0) #左
        pg.draw.rect(screen, my_color, rect=(left+10 , top-10, right-(left+20), 10), width=0) #上
        pg.draw.rect(screen, my_color, rect=(right , top+10, 10, bottom-30), width=0) #右
        pg.draw.rect(screen, my_color, rect=(left+10 , bottom, right-(left+20), 10), width=0) #下
        #  枠線四隅
        pg.draw.rect(screen, my_color, rect=(left , top, 10, 10), width=0) #左上
        pg.draw.rect(screen, my_color, rect=(right-10, top, 10, 10), width=0) #右上
        pg.draw.rect(screen, my_color, rect=(right-10, bottom-10, 10, 10), width=0) #右下
        pg.draw.rect(screen, my_color, rect=(left, bottom-10, 10, 10), width=0) #左下

        #  ふきだししっぽ
        my_rect = pg.draw.polygon(screen, (255,255,255), points=try_positions, width=0)
        #  しっぽ枠線
        pg.draw.rect(screen, my_color, rect=(left-10, (bottom*5/10), 10, 10), width=0) #頂点1
        pg.draw.rect(screen, my_color, rect=(left-20, (bottom*5/10)+10, 10, 10), width=0) #辺1
        pg.draw.rect(screen, my_color, rect=(left-30, (bottom*5/10)+20, 10, 10), width=0) #辺1
        pg.draw.rect(screen, my_color, rect=(left-40, (bottom*6/10)-10, 10, 10), width=0) #頂点2
        pg.draw.rect(screen, my_color, rect=(left-50, (bottom*6/10), 50, 10), width=0) #辺3

        self.draw_text(screen, left, top)

    def draw_text(self, screen:pg.surface, left_x:int, top_y:int):
        """
        注文内容を表示するメソッド
        """
        # フォントの設定
        font = pg.font.Font(FONT_PATH,40)
        font_color = (139,0,0)
        # フォントの座標
        x = left_x+20
        y = top_y+10
        y_space = 50  # 行間

        order_text,order_img = self.order.get_text()  # オーダークラスから注文内容を取得
        text_lines = order_text.splitlines()  # "\n"でテキストを分ける

        for i,text in enumerate(text_lines):
            text_surface = font.render(text, True, font_color)
            text_rct = text_surface.get_rect()
            text_rct.topleft = (x,y)
            screen.blit(text_surface, text_rct)

            y += y_space

            # 具材アイコンの表示
            if i < len(order_img):
                img_surface = pg.image.load(order_img[i]).convert_alpha()
                img_surface = pg.transform.scale(img_surface, (75,75))  # 画像のサイズ変更
                img_rct = img_surface.get_rect()
                img_rct.left = text_rct.right
                img_rct.centery = text_rct.centery
                screen.blit(img_surface, img_rct)

class Order():
    """
    オーダーを管理するクラス

    my_spiceslevel : 注文する辛さ
    my_order :注文する具材内容
    my_orderimg :注文する具材の画像
    """
    def __init__(self, toppings_dict:dict, spices_dict:dict):
        self.my_spices = None
        self.my_order = []
        self.my_orderimg = []
        self.toppings_dict = {v:k for k,v in toppings_dict.items()} # topping_dictの値とキーを入れ替えた辞書
        self.toppings = list(toppings_dict.values())
        self.spicess = [ v for v in spices_dict.values()]

    def set_order(self, max:int):
        """
        オーダーを決める
        max :注文の最大選択個数
        """
        order_num = random.randint(1,max)

        #  具材リストからランダムに取得
        for i in range(0,order_num):
            topping = random.choice(self.toppings)
            self.my_order.append(topping)
            self.my_orderimg.append( self.toppings_dict[topping] )

        #  辛さをランダムに決定
        self.my_spices = random.choice(self.spicess)

    def get_order(self) -> list:
        """
        注文具材の一覧を取得
        """
        return self.my_order.copy()

    def get_spiceslevel(self) -> str:
        """
        注文の辛さを取得
        """
        return self.my_spices

    def get_text(self) -> tuple[str, list]:
        """
        注文表示用テキスト＆具材画像を返す
        """
        order_text = f""

        # テキストの生成
        for topping in self.my_order:
            order_text += topping + "\n"
        else:
            order_text += f"の{self.my_spices}\nをください"

        return order_text,self.my_orderimg
    
    def check_order(self, player:object) -> bool:
        """
        具材と辛さが両方一致しているか判定
        完全一致：True
        不一致：False
        引数 player:Playerオブジェクト
        """
        select_order, select_spice = player.get_select()

        # 具材の種類・個数を判定
        goods_result = (sorted(self.my_order)) == sorted(select_order)

        # 辛さを判定
        spice_result = (self.my_spices == select_spice)

        # 両方正解ならTrue
        return goods_result and spice_result

class Score:
    """
    提供した麻辣湯の数によってスコアがもらえるクラス
    正しく麻辣湯を提供できたら +1000点
    
    """
    def __init__(self):
        self.font = pg.font.Font(FONT_PATH, 40)  # フォントの指定
        self.color = (255, 255, 255)  # 文字の色の指定
        self.value = 0  # 初期スコア
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)  # スコア表示設定
        self.rect = self.image.get_rect()  # imageのrectを取得
        self.rect.left = 35  # 文字の左上のx座標
        self.rect.top = 205  # 文字の左上のy座標

    def update(self, screen: pg.Surface):
        """
        スコアを画面左上に表示する
        引数 screen：ゲーム画面のSurface
        戻り値：なし
        """
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)

def gameover(screen: pg.Surface, score: int) -> bool:
    """
    引数: Surface, スコア(int)
    戻り値: なし
    GameOver画面と最終スコアの表示
    """
    # BGMの再生
    pg.mixer.music.stop()  # 現在流れているBGMをストップ
    pg.mixer.music.load(BGM_GAMEOVER)  # ダウンロードした音源ファイルをロード
    pg.mixer.music.play(-1)  # ループ再生

    margin_x = 100
    margin_y = 50

    dialog_w = WIDTH - (margin_x * 2)
    dialog_h = HEIGHT - (margin_y * 2)

    gameover_screen = pg.Surface((dialog_w, dialog_h))
    pg.draw.rect(gameover_screen, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))  # 黒い矩形を作る
    gameover_screen.set_alpha(210)  # 透明度の調節

    fonto_go = pg.font.Font(FONT_PATH, 100)
    fonto_sc = pg.font.Font(FONT_PATH, 80)
    font_gu = pg.font.Font(FONT_PATH, 40)
    
    # "Game Over"の白文字を作る (少し上に配置)
    txt = fonto_go.render("Game Over", True, (255, 255, 255)) 
    txt_rect = txt.get_rect()
    txt_rect.center = dialog_w / 2, dialog_h / 2 - 100  # 中心から上に80ピクセルずらす
    gameover_screen.blit(txt, txt_rect)

    # スコアの白文字を作る (少し下に配置)
    score_txt = fonto_sc.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_txt.get_rect()
    score_rect.center = dialog_w / 2, dialog_h / 2  # 中心から下に50ピクセルずらす
    gameover_screen.blit(score_txt, score_rect)

    # 画面に操作案内を追加
    guide_txt = font_gu.render("Press ENTER to Restart / ESC to Exit", True, (200, 200, 200))
    guide_rect = guide_txt.get_rect()
    guide_rect.center = dialog_w / 2, dialog_h / 2 + 80
    gameover_screen.blit(guide_txt, guide_rect)

    screen.blit(gameover_screen, (margin_x, margin_y))  # Screenを表示
    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # ウィンドウの×ボタンが押されたとき
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Enterキーが押されたら True(リスタート)
                    return True
                elif event.key == pg.K_ESCAPE:  # Escキーが押されたら False(終了)
                    return False

class Time:
    """
    制限時間と日数を管理するクラス
    """

    def __init__(self,time:int):
        """
        時間管理に必要な属性を初期化する。
        引数：Time 秒数指定
        戻り値：なし
        """
        self.day = 1 # 現在の日数
        self.time_limit = time # 1日の制限時間(秒)
        self.nokori = self.time_limit # 残り時間
        self.owari = False # 時間切れかどうか
        self.font = pg.font.Font(FONT_PATH, 24) # 表示する文字の設定

    def update(self, dt: float) -> bool:
        """
        経過時間に応じて残り時間を減らすメソッド
        引数：dt (前のフレームからの経過時間、秒)
        戻り値：時間切れになった瞬間はTrue、それ以外はFalse
        """
        if self.owari:
            return False

        self.nokori -= dt

        if self.nokori <= 0:
            self.nokori = 0
            self.owari = True
            return True # 時間切れを知らせる
        
        return False

    def next_day(self):
        """
        日数を1日進め、制限時間をリセットするメソッド
        引数：なし
        戻り値：なし
        """
        self.day += 1
        self.nokori = self.time_limit
        self.owari = False

    def reset(self):
        """
        残り時間をリセットするメソッド
        引数：なし
        戻り値：なし
        """
        self.nokori = self.time_limit
        self.owari = False

    def get_customer_count(self) -> int:
        """
        日数に応じたお客さんの人数を取得するメソッド
        引数：なし
        戻り値：その日に来店するお客さんの人数（int）
        """
        return 3 + (self.day - 1) * 2

    def draw(self, screen):
        """
        現在の日数と残り時間を画面に表示するメソッド
        引数：screen（描画先のSurface）
        戻り値：なし
        """

        # 半透明の黒い背景を作成
        bg = pg.Surface((400, 250), pg.SRCALPHA)
        pg.draw.rect(bg, (0, 0, 0), (0, 0, 400, 250), border_radius=20)
        bg.set_alpha(150)
        screen.blit(bg, (20, 15))

        # 日数を表示
        day_img = self.font.render(
            f"{self.day}日目", True, (255, 255, 255)
        )

        # 残り時間の表示
        time_img = self.font.render(
            f"残り時間：{math.ceil(self.nokori)}秒",
            True, (255, 255, 255)
        )

        screen.blit(day_img, (35, 25))
        screen.blit(time_img, (35, 85))

class Help:
    """
    ゲームの操作方法を表示するクラス
    """

    def __init__(self):
        """
        引数：なし
        戻り値：なし
        """
        self.show = False  # 操作方法を表示するかどうか
        self.font = pg.font.Font(FONT_PATH, 30)  # 操作説明
        self.title_font = pg.font.Font(FONT_PATH, 45)  # 操作説明タイトル

    def toggle(self):
        """
        操作方法の表示・非表示を切り替えるメソッド
        引数：なし
        戻り値：なし
        """
        self.show = not self.show

    def draw(self, screen):
        """
        操作方法を表示させるメソッド
        引数：screen(描画先のSurface)
        戻り値：なし
        """
        if not self.show:
            return

        # 半透明の黒い背景画面
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))

        # タイトルを表示
        title = self.title_font.render(
            "操作方法", True, (255, 255, 255)
        )
        title_rect = title.get_rect(center=(WIDTH//2, 90))
        screen.blit(title, title_rect)

        # 操作説明
        texts = [
            "時間切れ・注文ミスでライフが－1",
            "数字キー：具材を選択する",
            "左クリック：具材を1つ追加する",
            "上キー：辛さを変更する",
            "Enterキー：商品を提供する",
            "Qキー：操作方法を開く・閉じる"
        ]

        for i, text in enumerate(texts):
            img = self.font.render(
                text, True, (255, 255, 255)
            )
            screen.blit(img, (280, 175 + i * 55))

# ----- クラスここまで ------

# ----- メイン ------

def main():
    pg.display.set_caption(TITLE)  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png").convert_alpha()  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更
    table_img = pg.image.load(f"fig/table.png").convert_alpha()
    table_img = pg.transform.scale(table_img, (WIDTH*1.1, HEIGHT))  # 画像のサイズ変更
    
    count_font = pg.font.Font(FONT_PATH,30)

    while True:
        # BGMの再生
        pg.mixer.music.stop()  # 現在流れているBGMをストップ
        pg.mixer.music.load(BGM)  # ダウンロードした音源ファイルをロード
        pg.mixer.music.play(-1)  # ループ再生

        # 商品の作成
        # 商品棚に商品を追加 引数(位置)を商品関数に渡す
        goods_list = []
        margin = 40
        width = WIDTH - margin*2
        num = len(goods_dic)
        for i,goods in enumerate(goods_dic.keys()):
                x = margin + width *(i+0.5)/num
                y = HEIGHT * 31/35
                goods_list.append( Goods(goods, (x,y)) )


        # インスタンス生成
        # 商品をまとめて管理するGroup
        life = Life(LIFE_NUM)   # 初期残機数を3に設定
        score = Score()
        clock = pg.time.Clock()
        timer = Time(TIME_NUM) # タイマーを作成
        help_screen = Help()  # 操作方法を作成
        goods = pg.sprite.Group(goods_list)

        player = Player()
        customer = Customer(max=5)

        # 数字キーと商品の対応
        key_dic = {pg.K_1: 1, pg.K_2: 2, pg.K_3: 3, pg.K_4: 4, pg.K_5: 5}

        is_restart = False  # リスタートするかどうかを記録する変数
        while True: 

            dt = clock.tick(50) / 1000 #経過時間を秒に変換

            for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
                if event.type == pg.QUIT:
                    return 0

                if event.type == pg.KEYDOWN:
                    # Qキーで操作方法の表示・非表示を切り替える
                    if event.key == pg.K_q:
                        help_screen.toggle()
                        continue
                                
                if event.type == pg.MOUSEBUTTONDOWN:
                    # ヒントボタンクリックで操作方法の表示・非表示を切り替える
                    if player.hint_btn.rct.collidepoint(event.pos):
                        help_screen.toggle()

                # 操作説明中と営業中はゲーム操作を受け付けない
                if help_screen.show or timer.owari:
                    continue
                
                 # 数字キーによる商品選択
                if event.type == pg.KEYDOWN:
                    # 1～5キーが押された場合、対応する商品番号を取得
                    if event.key in key_dic:
                        index = key_dic[event.key]-1
                        # 商品を選択
                        player.add_select( goods_list[index] )

                    # どんぶりの辛さ変更
                    if event.key == pg.K_UP:
                        player.bowl.increase_spice()

                    # ENTERキーで注文内容を判定
                    if event.key == pg.K_RETURN:
                                        
                        if customer.order.check_order(player=player):
                            # 正解で1000点
                            score.value += 1000
                        else:
                            life.num -= 1  # 注文を間違えたら残機を1減らす

                        # 商品選択をリセット
                        player.reset()

                        # 次のお客さんを作成    
                        customer = Customer(max=5)

                # GUI
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # マウスクリックによる商品選択
                    for good in goods:
                        good_rct = good.rect.inflate(-30,-30)
                        if good_rct.collidepoint(mouse_pos):
                            # 左クリック → 1個追加
                            if event.button == 1:
                                # good.select(player.get_select())
                                player.add_select(good)

                    # どんぶりクリックで辛さ変更
                    if player.bowl.rct.collidepoint(event.pos):
                        player.bowl.increase_spice()

                    # 提供ボタンクリックで注文内容を確定
                    if player.savebtn_stutas==True and player.save_btn.rct.collidepoint(event.pos):
                        if customer.order.check_order(player=player):
                            # 正解で1000点
                            score.value += 1000
                        else:
                            life.num -= 1  # 注文を間違えたら残機を1減らす

                        # 商品選択をリセット
                        player.reset()

                        # 次のお客さんを作成    
                        customer = Customer(max=5)

            # 操作方法が表示されていない時だけ時間を進める
            time_up = False
    
            if not help_screen.show:
                time_up = timer.update(dt)
    
            if time_up:
                print("時間切れ!")
                life.num -= 1  # 時間切れでライフを1減らす

                # 商品選択をリセット
                player.reset()
                timer.reset()

            screen.blit(bg_img, [0, 0]) # 画面表示
            customer.draw(screen)
            screen.blit(table_img,[-(WIDTH/20),HEIGHT/3])
            player.bowl.draw(screen)

            # 商品をまとめて表示
            goods.draw(screen)


            for good in goods:
                # 1個以上選択されている場合
                if player.get_count(good.name) > 0:

                    player.savebtn_draw(screen) # 提供ボタン
                    # 選択した商品が分かるように枠を表示
                    good.draw_count(
                        screen = screen,
                        count = player.get_count(good.name),
                        font = count_font
                        )

            player.hintbtn_draw(screen) # ヒントボタンを表示
            timer.draw(screen) # 残り時間と日数を表示
            life.update(screen)  #　残機数分のハートを表示
            score.update(screen) # Score表示
            
    
            # 操作説明を最後に表示
            help_screen.draw(screen)
            
            # ライフが0になったらゲームオーバー
            if life.num <= 0:
                is_restart = gameover(screen, score.value)
                break

            pg.display.update() # 画面更新

        if is_restart:
            pg.mixer.music.stop()  # 現在流れているBGMをストップ
            continue  # 外側のループの先頭に戻る（＝リスタート）
        else:
            pg.mixer.music.stop()  # 現在流れているBGMをストップ
            return 0  # main関数を終了する（＝Escが押されたか、×で閉じられた）

    
# 呪文
if __name__ == "__main__":
    main()
    pg.quit()
    sys.exit()
