import pygame as pg
import sys
import os
from board import Board
from button import HoverButton, PseudoButton
from grid import Grid

pg.init()
RESOLUTION = WIDTH, HEIGHT = 1024, 800
WHITE = (255, 255, 255)
SCREEN = pg.display.set_mode(RESOLUTION)
pg.display.set_caption("Tic-Tac-Toe")

########################################################
SP_IMG_HOVER = pg.image.load(os.path.join
                             ('img', "buttons", "SinglePlayerHover.png"))
SP_IMG_NORMAL = pg.image.load(os.path.join
                              ('img', "buttons", "SinglePlayerNormal.png"))
MG_IMG_HOVER = pg.image.load(os.path.join
                             ('img', "buttons", "MultiPlayerHover.png"))
MP_IMG_NORMAL = pg.image.load(os.path.join
                              ('img', "buttons", "MultiPlayerNormal.png"))
QUIT_IMG_HOVER = pg.image.load(os.path.join('img', "buttons", "QuitHover.png"))
QUIT_IMG_NORMAL = pg.image.load(os.path.join('img', "buttons", "QuitNormal.png"))
NORMAL_3x3 = pg.image.load(os.path.join('img', "buttons", "3x3gridNorm.png"))
HOVER_3x3 = pg.image.load(os.path.join('img', "buttons", "3x3gridHover.png"))
NORMAL_4x4 = pg.image.load(os.path.join('img', "buttons", "4x4gridNorm.png"))
HOVER_4x4 = pg.image.load(os.path.join('img', "buttons", "4x4gridHover.png"))
BACK_IMG_NORM = pg.image.load(os.path.join('img', "buttons", "back_norm.png"))
BACK_IMG_HOVER = pg.image.load(os.path.join('img', "buttons", "back_hover.png"))
TITLE_IMG = pg.image.load(os.path.join('img', "titleImg.png"))
BACK_ARROW_HOVER = pg.image.load(os.path.join('img', "buttons", "end_hover.png"))
BACK_ARROW_NORMAL = pg.image.load(os.path.join('img', "buttons", "end_default.png"))
TURNX_NORMAL = pg.image.load(os.path.join('img', "default_x.png"))
TURNX_ACTIVE = pg.image.load(os.path.join('img', "active_x.png"))
TURNO_NORMAL = pg.image.load(os.path.join('img', "default_o.png"))
TURNO_ACTIVE = pg.image.load(os.path.join('img', "active_o.png"))
BACKGROUND = pg.image.load(os.path.join('img', "background-ttt.png"))
GRID_3x3 = pg.image.load(os.path.join('img', "3x3.png"))
GRID_4x4 = pg.image.load(os.path.join('img', "4x4.png"))
REFRESH_NORMAL = pg.image.load(os.path.join('img', "buttons", "refresh_norm.png"))
REFRESH_ACTIVE = pg.image.load(os.path.join('img', "buttons", "refresh_active.png"))


######################################################


def get_text(text, size):
    font = pg.font.SysFont("Courier", size, bold=True)
    label = font.render(text, True, (0, 0, 0), )
    return label


def update_sprite(sprites):
    for sprite in sprites:
        sprite.update()
        sprite.draw(SCREEN)


def main_menu():
    singleplayer_btn = HoverButton(
        SP_IMG_NORMAL,
        SP_IMG_HOVER,
        (512, 360)
    )

    multiplayer_btn = HoverButton(
        MP_IMG_NORMAL,
        MG_IMG_HOVER,
        (512, 490)
    )

    quit_btn = HoverButton(
        QUIT_IMG_NORMAL,
        QUIT_IMG_HOVER,
        (512, 680)
    )

    buttons = [singleplayer_btn, multiplayer_btn, quit_btn]

    while True:
        click = False

        SCREEN.blit(BACKGROUND, (0, 0))
        SCREEN.blit(TITLE_IMG, (WIDTH // 6, HEIGHT // 8))
        update_sprite(buttons)

        pg.display.update()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.display.quit()
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                click = True

        if click:
            if singleplayer_btn.hover_state:
                choose_grid(True)
            elif multiplayer_btn.hover_state:  # to do
                choose_grid(False)
            elif quit_btn.hover_state:
                pg.display.quit()
                pg.quit()
                sys.exit()


def prewiev_grid(grid):
    grid_image = pg.transform.scale(grid, (WIDTH // 3, HEIGHT // 3))
    SCREEN.blit(grid_image, (WIDTH // 3, HEIGHT // 2))


def choose_grid(ai):
    btn_3x3 = HoverButton(
        NORMAL_3x3,
        HOVER_3x3,
        (WIDTH // 2.92, HEIGHT // 2.9)
    )

    btn_4x4 = HoverButton(
        NORMAL_4x4,
        HOVER_4x4,
        (WIDTH // 1.52, HEIGHT // 2.9)
    )

    back_btn = HoverButton(
        BACK_IMG_NORM,
        BACK_IMG_HOVER,
        (WIDTH // 5.50, HEIGHT // 1.08),
    )

    grid_label = get_text("Choose Grid:", 85)

    buttons = [btn_3x3, btn_4x4, back_btn]
    running = True

    while running:
        click = False

        SCREEN.blit(BACKGROUND, (0, 0))
        update_sprite(buttons)
        SCREEN.blit(grid_label, (WIDTH // 4.6, HEIGHT * 0.10))

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                click = True

        if btn_3x3.hover_state:
            prewiev_grid(GRID_3x3)
            if click:
                game_instance(3, ai, GRID_3x3)

        if btn_4x4.hover_state:
            prewiev_grid(GRID_4x4)
            if click:
                game_instance(4, ai, GRID_4x4)

        if back_btn.hover_state and click:
            break

        pg.display.update()


def prepare_grid(grid):
    SCREEN.fill(WHITE)
    grid.draw_grid()
    SCREEN.blit(grid.grid_surface, (grid.offsetx, grid.offsety))
    pg.display.update()


def make_play(mouse_pos, board, grid, ai_play, ai_on):
    if ai_play:
        cell_pos = board.play_optimal_move(board.opponent, board.player)
    else:
        bounds_pos = mouse_pos[0] - grid.offsetx, mouse_pos[1] - grid.offsety
        cell_pos = int(bounds_pos[1] // grid.cell_proportions), \
                   int(bounds_pos[0] // grid.cell_proportions)

    change_to_board = board.set_cell_value(*cell_pos, board.player_on_turn)

    if change_to_board:

        grid.animate_symbol(*cell_pos, symbol=board.player_on_turn)
        board.victory(board.player, board.opponent)

        if not board.winner:
            if board.player_on_turn == board.player:
                board.player_on_turn = board.opponent
            else:
                board.player_on_turn = board.player

        if ai_play:
            return False
        if ai_on:
            return True


def get_winner_label(board):
    if board.winner == "Tie":
        label = get_text("It's a Tie", 80)
    else:
        label = get_text(("Winner is " + board.winner), 80)

    return label


def game_instance(board_size, ai_on, grid_graphic):
    board = Board(board_size)
    grid = Grid(board, RESOLUTION, grid_graphic)
    prepare_grid(grid)

    ai_play = False

    back_btn = HoverButton(
        BACK_ARROW_NORMAL,
        BACK_ARROW_HOVER,
        (90, 710),
    )

    refresh_btn = HoverButton(
        REFRESH_NORMAL,
        REFRESH_ACTIVE,
        (934, 710),
    )

    turn_symbolx = PseudoButton(
        TURNX_NORMAL,
        TURNX_ACTIVE,
        (400, 70),
        board,
        "X"
    )

    turn_symbolo = PseudoButton(
        TURNO_NORMAL,
        TURNO_ACTIVE,
        (600, 70),
        board,
        "O"
    )

    sprites = [grid, back_btn, refresh_btn, turn_symbolo, turn_symbolx]
    running = True

    while running:

        click = False
        clicked_grid_bound1 = False
        clicked_grid_bound2 = False
        mouse_pos = (0, 0)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.display.quit()
                pg.quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    mouse_pos = pg.mouse.get_pos()
                    click = True

                    clicked_grid_bound1 = mouse_pos[0] > grid.offsetx and \
                                          mouse_pos[1] > grid.offsety

                    clicked_grid_bound2 = mouse_pos[0] < WIDTH - grid.offsetx \
                                          and \
                                          mouse_pos[1] < HEIGHT - grid.offsety

        if click:
            if back_btn.hover_state:
                break
            if refresh_btn.hover_state:
                board = Board(board_size)
                grid = Grid(board, RESOLUTION, grid_graphic)
                prepare_grid(grid)
                sprites[0] = grid
                turn_symbolx.board = board
                turn_symbolo.board = board

        if ((clicked_grid_bound1 and clicked_grid_bound2) and not board.winner) \
                or ai_play and not board.winner:
            ai_play = make_play(mouse_pos, board, grid, ai_play, ai_on)

        if board.winner and not grid.symbols_to_animate:
            label = get_winner_label(board)
            SCREEN.blit(label, (WIDTH // 4.096, HEIGHT // 1.14))

        update_sprite(sprites)
        pg.display.update()


main_menu()
