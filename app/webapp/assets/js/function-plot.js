// Adapted from http://www.javascripter.net/faq/plotafunctiongraph.htm

// let fun1 = eval("(function func(x) { return -x + 1; })");
// let fun2 = eval("(function func(x) { return Math.pow(x, 6.14); })");
var padding_bottom_left = 100;
var padding_top_right = 50;
var canvas_w_h;

function draw(canvas_id, func, sex) {
    func = parseEquation(func);
    var canvas = document.getElementById(canvas_id);
    if (null == canvas || !canvas.getContext) return;

    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    var axes = {};
    canvas_w_h = ctx.canvas.height;
    axes.x0 = 100;
    axes.y0 = canvas.height - 100;
    axes.scale = canvas_w_h - padding_top_right - padding_bottom_left; // amount of pixels from x=0 to x=1

    showAxes(ctx, axes);
    let fun = eval("(function func(x) { return " + func + "; })");
    if (sex == 1){
        funGraph(ctx, axes, fun, "rgb(66,44,255)", 2);
    } else {
        funGraph(ctx, axes, fun, "rgb(255,44,44)", 2);
    }
}

function funGraph(ctx, axes, func, color, thick) {
    var x0 = axes.x0,
        y0 = axes.y0,
        scale = axes.scale;
    var xx, yy, dx = 4; // dx is the distance between two calculated points
    var iMax = Math.round((canvas_w_h - padding_top_right - padding_bottom_left) / dx);
    ctx.beginPath();
    ctx.lineWidth = thick;
    ctx.strokeStyle = color;

    for (var i = 0; i <= iMax; i++) {
        xx = i * dx;
        yy = scale * func(xx / scale);
        ctx.lineTo(x0 + xx, y0 - yy);
    }
    ctx.stroke();
}

function showAxes(ctx, axes) {
    var x0 = axes.x0;
    var y0 = axes.y0;
    ctx.beginPath();
    ctx.strokeStyle = "rgb(128,128,128)";
    ctx.moveTo(padding_bottom_left, y0);
    ctx.lineTo(canvas_w_h, y0); // X axis
    ctx.moveTo(x0, 0);
    ctx.lineTo(x0, canvas_w_h - padding_bottom_left); // Y axis
    ctx.stroke();

    ctx.font = "18px Arial";
    ctx.fillStyle = "white";
    ctx.fillText("0 %", padding_bottom_left - 20, canvas_w_h - 60);

    ctx.moveTo(padding_bottom_left - 10, padding_top_right);
    ctx.lineTo(padding_bottom_left + 10, padding_top_right); // 100% at y axis
    ctx.stroke();
    ctx.font = "18px Arial";
    ctx.fillStyle = "white";
    ctx.fillText("100 %", padding_bottom_left - 70, padding_top_right + 7);

    ctx.moveTo(canvas_w_h - padding_top_right, canvas_w_h - padding_bottom_left + 10);
    ctx.lineTo(canvas_w_h - padding_top_right, canvas_w_h - padding_bottom_left - 10); // 100% at x axis
    ctx.stroke();
    ctx.font = "18px Arial";
    ctx.fillStyle = "white";
    ctx.fillText("100 %", canvas_w_h - padding_top_right - 20, canvas_w_h - padding_bottom_left + 30);
}

function parseEquation(equation) {
    equation = equation.replace("^", "**");
    equation = equation.replace("sin", "Math.sin");
    equation = equation.replace("cos", "Math.cos");
    equation = equation.replace("tan", "Math.tan");
    equation = equation.replace("asin", "Math.asin");
    equation = equation.replace("acos", "Math.acos");
    equation = equation.replace("atan", "Math.atan");
    equation = equation.replace("sqrt", "Math.sqrt");
    equation = equation.replace("PI", "Math.PI");   // allow
    equation = equation.replace("Pi", "Math.PI");   // all
    equation = equation.replace("pi", "Math.PI");   // three
    equation = equation.replace("e", "Math.E");
    equation = equation.replace("log2", "Math.log2");
    equation = equation.replace("abs", "Math.abs");
    return equation;
}