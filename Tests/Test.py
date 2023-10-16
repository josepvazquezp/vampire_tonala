import pygame
import pymunk
import sys
import os

def main():
    # Inicialización de Pygame
    pygame.init()
    
    # Definir el tamaño de la ventana del juego
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Juego con Pymunk")
    
    # Cargar la imagen de fondo
    background = pygame.image.load("background.jpg")
    background_rect = background.get_rect()

    # Asegúrate de que la imagen de fondo se repita (tile)
    background = pygame.transform.scale(background, (background_rect.width, height))  # ajusta la altura, pero mantiene el ancho original para el efecto de mosaico
    
    # Inicialización de Pymunk
    space = pymunk.Space()
    space.gravity = 0, -1000  # solo un ejemplo, no se aplica ninguna física en este código

    player = pygame.image.load("Sprite-Antonio.jpg")  # Asegúrate de que "player.jpg" esté en tu directorio de trabajo o proporciona la ruta correcta
    player = pygame.transform.scale(player, (40, 60))  # Cambia el tamaño a tu gusto
    player_rect = player.get_rect()
    player_rect.topleft = (width // 2, height // 2)  # Empieza en el centro de la pantalla

    
    
    # Variables para el movimiento del personaje
    player_speed = 5
    move_left = False
    move_right = False

    # Bucle principal del juego
    clock = pygame.time.Clock()  # Crea un objeto clock
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    move_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False

        # Actualiza la posición del personaje
        if move_left:
            player_rect.x -= player_speed
        if move_right:
            player_rect.x += player_speed

        # Mover el fondo si el jugador se mueve
        if move_left or move_right:
            background_rect.x -= player_speed if move_right else -player_speed
        
        # Repetir (tile) la imagen de fondo si llega a su extremo
        if background_rect.right < width:
            background_rect.left = 0
        elif background_rect.left > 0:
            background_rect.right = width

        # Dibujar el fondo
        screen.blit(background, background_rect)

        # Dibujar el jugador
        screen.blit(player, player_rect)
        
        # Actualizar la pantalla de Pygame
        pygame.display.flip()
        
        # Actualizar el espacio de Pymunk
        space.step(1/50)  # 50 FPS, modificar según sea necesario
        
        # Reloj para manejar la velocidad de fotogramas
        clock.tick(50)

if __name__ == "__main__":
    main()
