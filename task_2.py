import argparse
import turtle


def koch_segment(t: turtle.Turtle, length: float, level: int) -> None:
    """Рекурсивно малює один відрізок кривої Коха."""
    if level == 0:
        t.forward(length)
        return
    length /= 3.0
    koch_segment(t, length, level - 1)
    t.left(60)
    koch_segment(t, length, level - 1)
    t.right(120)
    koch_segment(t, length, level - 1)
    t.left(60)
    koch_segment(t, length, level - 1)


def koch_snowflake(t: turtle.Turtle, length: float, level: int) -> None:
    """Малює повну сніжинку (три відрізки Коха)."""
    for _ in range(3):
        koch_segment(t, length, level)
        t.right(120)


def parse_args():
    p = argparse.ArgumentParser(
        description="Намалювати фрактал «сніжинка Коха» з заданим рівнем рекурсії."
    )
    p.add_argument(
        "-n", "--level",
        type=int, default=3,
        help="рівень рекурсії (не від’ємне ціле, напр. 0..7). За замовчуванням: 3"
    )
    p.add_argument(
        "-L", "--length",
        type=float, default=300.0,
        help="початкова довжина сторони сніжинки в пікселях (за замовчуванням 300)"
    )
    p.add_argument(
        "-s", "--speed",
        type=int, default=0,
        help="швидкість черепашки 0..10 (0=миттєво). За замовчуванням 0"
    )
    p.add_argument(
        "--bg", default="white", help="колір фону (напр. black, #202020)"
    )
    p.add_argument(
        "--line", default="dodgerblue", help="колір лінії (напр. red, #00aaff)"
    )
    return p.parse_args()


def main():
    args = parse_args()
    if args.level < 0:
        raise SystemExit("Рівень рекурсії має бути невід’ємним цілим числом.")

    # Підготовка полотна
    screen = turtle.Screen()
    screen.title(f"Koch Snowflake (level={args.level})")
    screen.bgcolor(args.bg)

    t = turtle.Turtle(visible=False)
    t.speed(args.speed)
    t.color(args.line)
    t.pensize(2)

    # Центруємо фігуру: стартуємо в лівому нижчому положенні трикутника
    # (грубо, щоб сніжинка була в кадрі для типових рівнів)
    t.penup()
    t.setheading(0)
    t.goto(-args.length / 2, args.length / 3)
    t.pendown()
    t.showturtle()

    koch_snowflake(t, args.length, args.level)

    t.hideturtle()
    # Клік мишкою — закрити
    screen.exitonclick()


if __name__ == "__main__":
    main()
