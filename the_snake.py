from random import choice, randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

RANDOM_MIN_X = 1
RANDOM_MAX_X = GRID_WIDTH - 1
RANDOM_MIN_Y = 1
RANDOM_MAX_Y = GRID_HEIGHT - 1

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты.
    Он содержит общие атрибуты игровых объектов (позиция и цвет объекта)
    Содержит и заготовку метода для отрисовки объекта на игровом поле — draw.
    """

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = APPLE_COLOR

    def draw(self):
        """Это абстрактный метод,
        который предназначен для переопределения в дочерних классах.
        """


class Apple(GameObject):
    """Класс, унаследованный от GameObject, описывающий яблоко
    и действия с ним.
    """

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(self.position)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, snake_position):
        """Устанавливает случайное положение яблока на игровом поле"""
        while True:
            self.position = (
                randint(RANDOM_MIN_X, RANDOM_MAX_X) * GRID_SIZE,
                randint(RANDOM_MIN_Y, RANDOM_MAX_Y) * GRID_SIZE,
            )

            if self.position not in snake_position:
                return self.position


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку и её поведение.
    Этот класс управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.direction = DOWN
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def draw(self):
        """Отрисовывает змейку на экране"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляет последний элемент, если длина змейки не увеличилась.
        """
        x, y = self.get_head_position()

        list.insert(
            self.positions,
            0,
            (
                (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
            ),
        )

        if len(self.positions) > self.length:
            self.last = list.pop(self.positions)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([DOWN, UP, LEFT, RIGHT])


def handle_keys(game_object):
    """обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Логика игры"""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.move()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
