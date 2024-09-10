///////////////////////////////////////////////////////////
///////////////////////// Drawing /////////////////////////
///////////////////////////////////////////////////////////

function draw_ball(x, y)
{
	ctx.beginPath();
	ctx.arc(x, y, ball_radius, 0, 2 * Math.PI);
	ctx.fillStyle = "black";
	ctx.fill();
	ctx.closePath();
}

function draw_score()
{
	aurebesh.load().then(() => {
		let size = 100 * (board.height + board.width) / 3000;
		
		ctx.font = size.toString() + 'px "aurebesh"';
		ctx.fillStyle = "#009000";
		ctx.textAlign = "center";
		ctx.fillText(score[0] + "   |   " + score[1], board_x_max / 2, board_y_max / 6)
	});
}

function draw_paddle(x, paddle_coords)
{
	ctx.beginPath();
	ctx.rect(x, paddle_coords, paddle_width, paddle_height);
	if (x == left_paddle_x)
		ctx.fillStyle = "#505090";
	else
		ctx.fillStyle = "#900000";
	ctx.fill();
	ctx.closePath();
}

function draw_board(left_paddle_coords, right_paddle_coords)
{
	ctx.fillStyle = "#009000";
	ctx.fillRect(0, 0, board.width, board.height);
	ctx.clearRect(board_min, board_min, board_x_max - board_min, board_y_max - board_min);
	
	draw_ball(ball_x, ball_y);
	draw_score();
	draw_paddle(left_paddle_x, left_paddle_coords);
	draw_paddle(right_paddle_x, right_paddle_coords);
}