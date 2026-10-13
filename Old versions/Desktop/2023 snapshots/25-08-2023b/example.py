elif dropdown_open == True and placed_new_item == False and icon_index == 6 and connection_type == 1:
# Ask for player input
while True:
    try:
        if placement_grid[row + 1][col] != -1:
            pipe_section += 1
            left_arrow_appears()  # Left arrow appears
            q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
            q = int(q)
            covering_the_arrow(screen)
            Q[pipe_section] = q
            Q_grid[row][col - 1] = Q[pipe_section]
            pipe_section_grid[row][col - 1] = pipe_section
            T[pipe_section] = [T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset]]
            T[pipe_section_grid[row][col - 1]] = T[pipe_section]

            pipe_section += 1
            right_arrow_appears()  # Right arrow appears
            q = show_input_box(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
            q = int(q)
            covering_the_arrow(screen)
            Q[pipe_section] = q
            Q_grid[row][col + 1] = Q[pipe_section]
            pipe_section_grid[row][col + 1] = pipe_section
            T[pipe_section] = [T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset]]
            T[pipe_section_grid[row][col + 1]] = T[pipe_section]

            # T of the triplet
            T_grid[row][col] = float(T[pipe_section_grid[row + 1][col]][-1] - Tloss_pipe[dataset])