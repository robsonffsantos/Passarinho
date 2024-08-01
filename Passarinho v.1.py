import pygame
import sys
from pygame.locals import *

#iniciar pygame, tela, relogio
pygame.init()
dimensoes = (640, 640)

pygame.display.set_caption('Passarinho')
tela = pygame.display.set_mode(dimensoes, 0, 32)

clock = pygame.time.Clock()

#imagens
plataforma_meia_img = pygame.image.load('imagens/plat/plat03.png')
arvore_img = pygame.image.load('imagens/fundo/Arvore.png')
copa_img = pygame.image.load('imagens/fundo/copa.png')
ninho_img = pygame.image.load('imagens/fundo/ninho.png')
grama_img = pygame.image.load('imagens/fundo/grama.png')
venceu_img = pygame.image.load('imagens/frases/venceu.png')
menu_img = pygame.image.load('imagens/frases/Tela_Inicial.png')
espinho_img = pygame.image.load('imagens/fundo/espinho.png')
perdeu_img = pygame.image.load('imagens/frases/perdeu.png')
creditos_img = pygame.image.load('imagens/frases/credito.png')

inimigo_img = []
inim = pygame.image.load('imagens/inimigo/inimigo_0.png')
inimigo_img.append(inim)
inim = pygame.image.load('imagens/inimigo/inimigo_1.png')
inimigo_img.append(inim)

#Musicas
jump_snd = pygame.mixer.Sound('sons/huh.wav')
dead_snd = pygame.mixer.Sound('sons/ouch0.ogg')
vitoria_snd = pygame.mixer.Sound('sons/well_done_ccbY3.ogg')
inimigo_snd = pygame.mixer.Sound('sons/vulture-1.ogg')

pygame.mixer.music.load('sons/mushroom_dance_0.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

#variaveis
mov_dir = False
mov_esq = False
pulo = 0
no_ar = 0
scroll = [0,0]
global fps_animacao
fps_animacao = {}
inimigo_velocidade = 12
pause = False
menu = True
ind = 0.01
mov = 12
mov_ini = True
cont = 1

#retangulo do personagem
rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)

#outros retangulos
ninho_rect = pygame.Rect(240, 80, 64, 64)
espinho_1_rect = pygame.Rect(352, 544, 24, 16)
espinho_3_rect = pygame.Rect(288, 992, 24, 16)
espinho_4_rect = pygame.Rect(544, 1248, 24, 16)
espinho_6_rect = pygame.Rect(448, 1696, 24, 16)
espinho_7_rect = pygame.Rect(288, 1824, 24, 16)
espinho_8_rect = pygame.Rect(384, 1952, 24, 16)
espinho_9_rect = pygame.Rect(224, 2144, 24, 16)
inimigo_1_rect = pygame.Rect(64, 1856, 64, 64)
inimigo_2_rect = pygame.Rect(288, 1568, 64, 64)
inimigo_3_rect = pygame.Rect(480, 1056, 64, 64)
inimigo_4_rect = pygame.Rect(192, 512, 64, 64)

#funçoes
def carregar_animacao(path, duracao_fps):
    global fps_animacao
    animacao_nome = path.split('/')[-1]
    animacao_frame = []
    n = 0
    for frame in duracao_fps:
        fps_animacao_id = animacao_nome + '_' + str(n)
        loc_imag = path + '/' + fps_animacao_id + '.png'
        img_loc = pygame.image.load(loc_imag)
        fps_animacao[fps_animacao_id] = img_loc.copy()
        for i in range(frame):
            animacao_frame.append(fps_animacao_id)
        n = n + 1
    return animacao_frame

def teste_colisao(rect, blocos):
    lista_colisao = []
    for bloco in blocos:
        if rect.colliderect(bloco):
            lista_colisao.append(bloco)
    return lista_colisao

def mover(rect, movimento, blocos):
    tipos_colisao = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movimento[0]
    lista_colisao = teste_colisao(rect, blocos)
    for bloco in lista_colisao:
        if movimento[0] > 0:
            rect.right = bloco.left
            tipos_colisao['right'] = True
        elif movimento[0] < 0:
            rect.left = bloco.right
            tipos_colisao['left'] = True
    rect.y += movimento[1]
    lista_colisao = teste_colisao(rect, blocos)
    for bloco in lista_colisao:
        if movimento[1] > 0:
            rect.bottom = bloco.top
            tipos_colisao['bottom'] = True
        elif movimento[1] < 0:
            rect.top = bloco.bottom
            tipos_colisao['top'] = True
    return rect, tipos_colisao

def carregar_mapa(caminho):
    f = open(caminho + '.txt', 'r')
    dados = f.read()
    f.close()
    dados = dados.split('\n')
    mapa = []
    for linha in dados:
        mapa.append(list(linha))
    return mapa

def mudar_ativo(acao, frame, novo_valor):
    if acao != novo_valor:
        acao = novo_valor
        frame = 0
    return acao, frame

def venceu():
    tela.blit(venceu_img, (160, 160))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()

    pygame.display.update()
    pygame.time.wait(5000)

def perdeu():
    tela.blit(perdeu_img, (160, 160))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()

    pygame.display.update()
    pygame.time.wait(2000)

def menu_jogo():
    global menu
    creditos = False
    
    while menu == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    menu = False
                if event.key == K_BACKSPACE:
                    creditos = True
                    menu = False
                    while creditos == True:
                        tela.blit(creditos_img, (0,0))
                        if event.key == K_BACKSPACE:
                            menu = True
                            creditos = False
                            
                        pygame.display.update()
                        pygame.time.wait(6000)                  
                    
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
            
        tela.fill((127, 140, 200))
        tela.blit(menu_img, (0, 0))                
        pygame.display.update()
        clock.tick(60)    

#carregar mapa, imagens
mapa = carregar_mapa('outros/mapa')

dados_animacao = {}
dados_animacao['andando'] = carregar_animacao('imagens/bird', [10,10])
dados_animacao['idle'] = carregar_animacao('imagens/idle', [15,15])
dados_animacao['pulando'] = carregar_animacao('imagens/idle', [4,4])
                                                
bird_ativo = 'idle'
bird_frame = 0
bird_flip = False
    
#loop principal
while True:
    if menu == True:
        menu_jogo()
        
    tela.fill((127, 140, 237)) #preenche tela com cor
    tela.blit(arvore_img, (0 - scroll[0], 0 - scroll[1]))
    tela.blit(copa_img, (0, - 384 - scroll[1]))
    tela.blit(ninho_img, (226, 80 - scroll[1]))
    tela.blit(grama_img, (0, 2528 - scroll[1]))
    tela.blit(espinho_img, (352, 544 - scroll[1]))
    tela.blit(espinho_img, (288, 992 - scroll[1]))
    tela.blit(espinho_img, (544, 1248 - scroll[1]))
    tela.blit(espinho_img, (448, 1696 - scroll[1]))
    tela.blit(espinho_img, (288, 1824 - scroll[1]))
    tela.blit(espinho_img, (384, 1952 - scroll[1]))
    tela.blit(espinho_img, (224, 2144 - scroll[1]))

    tela.blit(inimigo_img[int(ind)], (64, 1856  - scroll[1]))
    ind += 0.03
    if ind > 1.99:
        ind = 0
    tela.blit(inimigo_img[int(ind)], (288, 1568 - scroll[1]))
    ind += 0.03
    if ind > 1.99:
        ind = 0
    tela.blit(inimigo_img[int(ind)], (480, 1056 - scroll[1]))
    ind += 0.03
    if ind > 1.99:
        ind = 0
    tela.blit(inimigo_img[int(ind)], (192, 512 - scroll[1]))
    ind += 0.03
    if ind > 1.99:
        ind = 0
         
    scroll[1] += (rect_boneco.y - scroll[1] - 322)/20

    rect_blocos = []
    i = 0
    for camada in mapa:#carrega blocos imagem
        j = 0
        for bloco in camada:
            if bloco == '2':
                tela.blit(plataforma_meia_img, (j * 64, (i*2) * 32 - scroll[1]))
                rect_blocos.append(pygame.Rect(j * 64, (i*2) * 32, 64 , 32))
            if bloco == '3':
                rect_blocos.append(pygame.Rect(j*64, i*64, 64, 64))
            j = j + 1
        i = i + 1

    boneco_movimento = [0,0]#movimento bird
    if mov_dir == True:
        boneco_movimento[0] += 5
    if mov_dir == True and (rect_boneco[0] >= dimensoes[0] - 64):
        boneco_movimento[0] = 0
    if mov_esq == True:
        boneco_movimento[0] -= 5
    if mov_esq == True and (rect_boneco[0] <= 0):
        boneco_movimento[0] = 0
    boneco_movimento[1] += pulo
    pulo += 0.5
    if pulo > 6:
        pulo = 6

    if boneco_movimento[0] == 0:#carregar sequencia img
        bird_ativo, bird_frame = mudar_ativo(bird_ativo, bird_frame, 'idle')
    if boneco_movimento[0] < 0:
        bird_flip = False
        bird_ativo, bird_frame = mudar_ativo(bird_ativo, bird_frame, 'andando')
    if boneco_movimento[0] > 0:
        bird_flip = True
        bird_ativo, bird_frame = mudar_ativo(bird_ativo, bird_frame, 'andando')

    rect_boneco, colisoes = mover(rect_boneco, boneco_movimento, rect_blocos)

    if colisoes['bottom'] == True:
        no_ar = 0
        pulo = False
    else:
        no_ar += 3

    bird_frame = bird_frame + 1
    if bird_frame >= len(dados_animacao[bird_ativo]):
        bird_frame = 0
    bird_img_id = dados_animacao[bird_ativo][bird_frame]
    bird_img = fps_animacao[bird_img_id]
    tela.blit(pygame.transform.flip(bird_img, bird_flip,False), (rect_boneco.x - scroll[0], rect_boneco.y - scroll[1]))#carrega jogador       

    if rect_boneco.colliderect(ninho_rect):
        vitoria_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        venceu()

    if rect_boneco.colliderect(espinho_1_rect):
        dead_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(espinho_3_rect):
        dead_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(espinho_4_rect):
        dead_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(espinho_6_rect):
        dead_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(espinho_7_rect):
        dead_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(espinho_8_rect):
        dead_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(espinho_9_rect):
        dead_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(inimigo_1_rect):
        inimigo_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(inimigo_2_rect):
        inimigo_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(inimigo_3_rect):
        inimigo_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
    if rect_boneco.colliderect(inimigo_4_rect):
        inimigo_snd.play()
        rect_boneco = pygame.Rect(64, dimensoes[1] * 4 - 70, 64, 64)
        perdeu()
        
    for event in pygame.event.get():#para fechar
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                mov_dir = True
            if event.key == K_LEFT:
                mov_esq = True
            if event.key == K_SPACE:
                if no_ar < 15:
                    jump_snd.play()
                    pulo = -12
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                mov_dir = False
            if event.key == K_LEFT:
                mov_esq = False
                    
    pygame.display.update()
    clock.tick(60)
