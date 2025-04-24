def draw_box(x, y, width, height, title, content):
    # Draw the top border
    print(term.move_xy(x, y) + '┌' + '─' * (width - 2) + '┐')

    # Draw the title line
    title_line = f'│{title.center(width - 2)}│'
    print(term.move_xy(x, y + 1) + title_line)

    # Draw the middle lines with content
    content_lines = content.split('\n')
    for i in range(height - 3):
        if i < len(content_lines):
            content_line = f'│{content_lines[i].ljust(width - 2)}│'
        else:
            content_line = '│' + ' ' * (width - 2) + '│'
        print(term.move_xy(x, y + 2 + i) + content_line)

    # Draw the bottom border
    print(term.move_xy(x, y + height - 1) + '└' + '─' * (width - 2) + '┘')