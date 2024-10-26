const canvas = document.getElementById("board");
const ctx = canvas.getContext("2d");
const dimensions = 16/9;

function draw_rect()
{
	ctx.beginPath();
	ctx.scale(canvas.width, canvas.height);
	ctx.fillStyle = "#009000";
	ctx.fillRect(0, 0, canvas.width, canvas.height);
	ctx.closePath();
}

function resize()
{
    if (window.innerWidth / window.innerHeight > dimensions)
    {
        canvas.width = window.innerHeight * dimensions;
        canvas.height = window.innerHeight;
    }
    else
    {
        canvas.width = window.innerWidth;
        canvas.height = window.innerWidth / dimensions;
    }
	draw_rect();
}

window.addEventListener('resize', resize);

resize();
draw_rect();