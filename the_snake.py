from random import choice, randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


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
        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject, описывающий яблоко
    и действия с ним.
    """

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        return rect

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле
        задаёт атрибуту position новое значение.
        """
        return (randint(1, 31) * GRID_SIZE), (randint(1, 23) * GRID_SIZE)


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку и её поведение.
    Этот класс управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self) -> None:
        super().__init__()
        self.length = 1
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = DOWN
        self.next_direction = None
        self.last = None
        self.current_length = 1

    def draw(self):
        """Отрисовывает змейку на экране"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
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
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        return head_rect

    def position_new(self):
        """Новая позицию змейки"""
        if self.direction == DOWN:
            return list.insert(
                self.positions, 0, (self.width, self.height + GRID_SIZE))
        elif self.direction == UP:
            return list.insert(
                self.positions, 0, (self.width, self.height - GRID_SIZE))
        elif self.direction == LEFT:
            return list.insert(
                self.positions, 0, (self.width - GRID_SIZE, self.height))
        elif self.direction == RIGHT:
            return list.insert(
                self.positions, 0, (self.width + GRID_SIZE, self.height))

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент, если длина змейки не увеличилась.
        """
        self.head_snake = self.get_head_position()
        self.width, self.height = self.head_snake[:2]

        if self.current_length < self.length:
            self.current_length += 1
            self.position_new()
        else:
            if self.direction == DOWN:
                if self.height + GRID_SIZE >= SCREEN_HEIGHT:
                    list.insert(
                        self.positions,
                        0,
                        (self.width, self.height + GRID_SIZE - SCREEN_HEIGHT),
                    )
                else:
                    self.position_new()
            elif self.direction == UP:
                if self.height <= 0:
                    list.insert(
                        self.positions,
                        0,
                        (self.width, self.height - GRID_SIZE + SCREEN_HEIGHT),
                    )
                else:
                    self.position_new()
            elif self.direction == LEFT:
                if self.width <= 0:
                    list.insert(
                        self.positions,
                        0,
                        (self.width - GRID_SIZE + SCREEN_WIDTH, self.height),
                    )
                else:
                    self.position_new()
            elif self.direction == RIGHT:
                if self.width + GRID_SIZE >= SCREEN_WIDTH:
                    list.insert(
                        self.positions,
                        0,
                        (self.width + GRID_SIZE - SCREEN_WIDTH, self.height),
                    )
                else:
                    self.position_new()

            self.last = list.pop(self.positions)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.current_length = 1
        list.clear(self.positions)
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
        snake.move()

        if apple.draw().colliderect(snake.get_head_position()):
            snake.length += 1
            apple.position = apple.randomize_position()

        for i in snake.positions[1:]:
            snake_position = (i, (GRID_SIZE, GRID_SIZE))
            if snake.get_head_position().colliderect(snake_position):
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
