import pygame
import sys
import time

# Inicializa o Pygame
pygame.init()

# Definindo constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FONT = pygame.font.Font(None, 28)  # Fonte ajustada para melhor visualização
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (173, 216, 230)
HIGHLIGHT_COLOR = (255, 182, 193)
SOLUTION_COLOR = (144, 238, 144)

# Configurações da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Algoritmo de Knapsack Visualizado")

# Dados do problema
valores = [60, 100, 120]
pesos = [5, 8, 12]
capacidade = 28
n = len(valores)

# Função para desenhar o estado da matriz dp
def draw_table(dp, current_i, current_w, solution_path):
    screen.fill(WHITE)

    # Ajustar tamanho da célula para garantir que a matriz não ultrapasse a janela
    max_columns = min(capacidade + 1, SCREEN_WIDTH // 30)
    cell_width = SCREEN_WIDTH // max_columns
    cell_height = SCREEN_HEIGHT // (n + 5)

    # Exibe os pesos na linha superior
    for w in range(max_columns):
        rect_x = w * cell_width
        rect_y = 0
        weight_surface = FONT.render(str(w), True, BLACK)
        weight_rect = weight_surface.get_rect(center=(rect_x + cell_width // 2, rect_y + cell_height // 2))
        screen.blit(weight_surface, weight_rect)

    # Desenha os valores da matriz dp
    for i in range(n + 1):
        for w in range(min(capacidade + 1, max_columns)):
            rect_x = w * cell_width
            rect_y = (i + 1) * cell_height

            # Destacar a célula atual
            if (i, w) in solution_path:
                color = SOLUTION_COLOR
            elif (i == current_i and w == current_w):
                color = HIGHLIGHT_COLOR
            else:
                color = BLUE

            # Desenha a célula
            pygame.draw.rect(screen, color, (rect_x, rect_y, cell_width, cell_height))
            pygame.draw.rect(screen, BLACK, (rect_x, rect_y, cell_width, cell_height), 1)
            
            # Limpa o espaço e desenha o número
            valor = dp[i][w]
            text_surface = FONT.render(str(valor), True, BLACK)
            text_rect = text_surface.get_rect(center=(rect_x + cell_width // 2, rect_y + cell_height // 2))
            # Apenas mostra valores diferentes de 0 para uma visualização limpa
            if valor != 0 or (i == current_i and w == current_w):
                pygame.draw.rect(screen, color, (rect_x + 2, rect_y + 2, cell_width - 4, cell_height - 4))
                screen.blit(text_surface, text_rect)

    # Exibir os rótulos
    for i in range(1, n + 1):
        item_label = FONT.render(f"Item {i} (V:{valores[i-1]} P:{pesos[i-1]})", True, BLACK)
        screen.blit(item_label, (10, (i + 1) * cell_height))

    capacity_label = FONT.render("Capacidades", True, BLACK)
    screen.blit(capacity_label, (SCREEN_WIDTH // 2 - 50, 10))

    pygame.display.flip()

# Algoritmo de knapsack usando programação dinâmica
def knapsack(valores, pesos, capacidade):
    n = len(valores)
    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacidade + 1):
            if pesos[i - 1] <= w:
                dp[i][w] = max(valores[i - 1] + dp[i - 1][w - pesos[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

            # Desenhar e pausar para visualização
            draw_table(dp, i, w, [])
            time.sleep(0.05)  # Ajuste o tempo de pausa conforme preferência

    solution_path = find_solution(dp, pesos, capacidade)
    draw_table(dp, n, capacidade, solution_path)
    time.sleep(5)

    return dp[n][capacidade]

# Função para encontrar a solução a partir da matriz dp
def find_solution(dp, pesos, capacidade):
    i = len(pesos)
    w = capacidade
    solution_path = []

    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            solution_path.append((i, w))
            w -= pesos[i - 1]
        i -= 1

    return solution_path

# Função principal
def main():
    while True:
        screen.fill(WHITE)
        text_surface = FONT.render("Pressione ESPAÇO para iniciar a visualização", True, BLACK)
        screen.blit(text_surface, (50, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                max_valor = knapsack(valores, pesos, capacidade)
                text_surface = FONT.render(f"Valor máximo: {max_valor}", True, GREEN)
                screen.fill(WHITE)
                screen.blit(text_surface, (50, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                time.sleep(5)
                return

if __name__ == "__main__":
    main()
