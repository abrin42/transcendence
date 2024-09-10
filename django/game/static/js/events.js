///////////////////////////////////////////////////////////
///////////////////////// Events //////////////////////////
///////////////////////////////////////////////////////////

function resize()
{
	let old_board_width = board.width;
	let old_board_height = board.height;

    if (window.innerWidth / window.innerHeight > dimensions)
    {
        board.width = window.innerHeight * dimensions;
        board.height = window.innerHeight;
    }
    else
    {
        board.width = window.innerWidth;
        board.height = window.innerWidth / dimensions;
    }

	board_min = board.width / 180;
	board_x_max = board.width - board_min;
	board_y_max = board.height - board_min;

	paddle_height = board.height / 7;
	paddle_width = board_min;
	left_paddle_x = board.width / 50;
	right_paddle_x = board_x_max - board.width / 50;
	left_paddle_current_y = left_paddle_current_y / old_board_height * board.height;
	right_paddle_current_y = right_paddle_current_y / old_board_height * board.height;
	paddle_speed = board.height / 60;

	ball_radius = ((board.width + board.height) / 3) / 65;
	ball_x = ball_x / old_board_width * board.width;
	ball_y = ball_y / old_board_height * board.height;
	
	draw_board(left_paddle_current_y, right_paddle_current_y);
}

window.addEventListener('resize', resize);

window.addEventListener('keydown', (e) =>
{
	if (e.key == 'w' || e.key == 's' || e.key == 'i' || e.key == 'k'
		|| e.key == 'W' || e.key == 'S' || e.key == 'I' || e.key == 'K')
	{
		keys[e.key] = true;
		handleKeyPress();
	}
});

window.addEventListener('keyup', (e) => {keys[e.key] = false});

let last_time_pressed = 0;

function handleKeyPress()
{
	if (Date.now() > last_time_pressed + 1)
	{
		last_time_pressed = Date.now();
		if (keys['w'] == true || keys['W'] == true)
		{
			left_paddle_current_y -= paddle_speed;
			if (left_paddle_current_y < board_min)
				left_paddle_current_y = board_min;
			draw_board(left_paddle_current_y, right_paddle_current_y);
		}
		if (keys['s'] == true  || keys['S'] == true )
		{
			left_paddle_current_y += paddle_speed;
			if (left_paddle_current_y > board_y_max - paddle_height)
				left_paddle_current_y = board_y_max - paddle_height;
			draw_board(left_paddle_current_y, right_paddle_current_y);
		}
		
		if (keys['i'] == true  || keys['I'] == true )
		{
			right_paddle_current_y -= paddle_speed;
			if (right_paddle_current_y < board_min)
				right_paddle_current_y = board_min;
			draw_board(left_paddle_current_y, right_paddle_current_y);
		}
		if (keys['k'] == true  || keys['K'] == true )
		{
			right_paddle_current_y += paddle_speed;
			if (right_paddle_current_y > board_y_max - paddle_height)
				right_paddle_current_y = board_y_max - paddle_height;
			draw_board(left_paddle_current_y, right_paddle_current_y);
		}
	}
	requestAnimationFrame(handleKeyPress);
}