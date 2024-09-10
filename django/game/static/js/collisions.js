///////////////////////////////////////////////////////////
/////////////////////// Collisions ////////////////////////
///////////////////////////////////////////////////////////

function wall_collisions(future_x, future_y)
{
	if (future_x < board_min + ball_radius || future_x + ball_radius > board_x_max)
	{
		victory(future_x);
		return (1);
	}
	if (future_y < board_min + ball_radius)
	{
		future_y = board_min + ball_radius;
		ball_angle = -ball_angle;
	}
	if (future_y > board_y_max - ball_radius)
	{
		future_y = board_y_max - ball_radius;
		ball_angle = -ball_angle;
	}
	ball_x = future_x;
	ball_y = future_y;
	return (0);
}

function speed_up_ball()
{
	if (ball_speed < 10)
		return (0.1);
	return (0);
}

function paddle_collisions(future_x, future_y)
{
	if (future_x <= left_paddle_x + paddle_width + ball_radius && future_x >= left_paddle_x
		&& future_y >= left_paddle_current_y - ball_radius && future_y <= left_paddle_current_y + paddle_height + ball_radius)
	{
		let position_in_paddle = (2 * (ball_y + ball_radius - left_paddle_current_y) / (paddle_height + ball_radius * 2)) - 1;
		ball_angle = 80 * position_in_paddle;
		ball_x += ball_radius / 10;
		ball_speed += speed_up_ball();
	}

	if (future_x >= right_paddle_x - ball_radius && future_x <= right_paddle_x + ball_radius / 2
		&& future_y >= right_paddle_current_y - ball_radius && future_y <= right_paddle_current_y + paddle_height + ball_radius)
	{
		let position_in_paddle = (2 * (ball_y + ball_radius - right_paddle_current_y) / (paddle_height + ball_radius * 2)) - 1;
		ball_angle = 180 - 80 * position_in_paddle;
		ball_x -= ball_radius / 10;
		ball_speed += speed_up_ball();
	}
}