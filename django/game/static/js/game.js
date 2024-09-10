///////////////////////////////////////////////////////////
//////////////////////// Variables ////////////////////////
///////////////////////////////////////////////////////////

const aurebesh = new FontFace("aurebesh", "url(../../static/aurebesh.otf)");
document.fonts.add(aurebesh);
aurebesh.load();

const board = document.getElementById("board");
const ctx = board.getContext("2d");
const dimensions = 16/9;
let keys = {};

let board_min;
let board_x_max;
let board_y_max;

let paddle_height;
let paddle_width;
let left_paddle_x;
let right_paddle_x;
let paddle_speed;
let left_paddle_current_y;
let right_paddle_current_y;

let ball_radius;
let ball_speed;
let ball_x;
let ball_y;
let ball_angle = Math.random() > 0.5 ? 180 : 0;

let score = [0,0];



///////////////////////////////////////////////////////////
////////////////////// Key functions //////////////////////
///////////////////////////////////////////////////////////

function move_ball()
{
	let future_x = ball_x + Math.cos(ball_angle * Math.PI / 180) * ball_speed * (board.width + board.height) / 2000;
	let future_y = ball_y + Math.sin(ball_angle * Math.PI / 180) * ball_speed * (board.width + board.height) / 2000;
	if (wall_collisions(future_x, future_y) == 0)
	{
		paddle_collisions(future_x, future_y);
		draw_board(left_paddle_current_y, right_paddle_current_y);
		setTimeout(move_ball, 1);
	}
}

function victory(future_x)
{
	if (future_x < board_x_max / 2)
	{
		score[1]++;
		ball_angle = 180;
		begin_point(3 * (board_x_max) / 4, (board_y_max + board_min) / 2);
	}
	else
	{
		score[0]++;
		ball_angle = 0;
		begin_point(1 * (board_x_max) / 4, (board_y_max + board_min) / 2);
	}
}

function begin_point(x_coords, y_coords)
{
	left_paddle_current_y = board.height / 2 - paddle_height / 2;
	right_paddle_current_y = board.height / 2 - paddle_height / 2;
	ball_speed = 2.5;
	ball_x = x_coords;
	ball_y = y_coords;
	draw_board(left_paddle_current_y, right_paddle_current_y);
	setTimeout(move_ball, 1500);
}



///////////////////////////////////////////////////////////
////////////////////// Initial moves //////////////////////
///////////////////////////////////////////////////////////

resize();
begin_point(board.width / 2, board.height / 2);