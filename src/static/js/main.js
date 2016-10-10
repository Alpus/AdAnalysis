var p_func_ctx = document.getElementById('p-func-plot').getContext('2d');
var S_func_ctx = document.getElementById('S-func-plot').getContext('2d');
var z_func_ctx = document.getElementById('z-func-plot').getContext('2d');
var p_plot = new Chart(
    p_func_ctx,
    {
        type: 'line',
        data: {
            labels: [], datasets: [{label: 'p(w)', data: [], backgroundColor: "rgba(153,255,51,0.4)"}]
        }
    }
)
var S_plot = new Chart(
    S_func_ctx,
    {
        type: 'line',
        data: {
            labels: [], datasets: [{label: 'S(t)', data: [], backgroundColor: "rgba(153,255,51,0.4)"}]
        }
    }
)
var z_plot = new Chart(
    z_func_ctx,
    {
        type: 'line',
        data: {
            labels: [], datasets: [{label: 'z(t)', data: [], backgroundColor: "rgba(153,255,51,0.4)"}]
        }
    }
)
function write_plot(expression, plot, variable) {
    var parser = math.parser();

    args = []
    vals = []
    for (let number = 0.0; number < 1.02; number += 0.02) {
        args.push(Math.round(number * 100) / 100);
        parser.set(variable, number);
        vals.push(parser.eval(expression));
    }

    console.log(plot.config.data.datasets[0].label)
    name = plot.config.data.datasets[0].label
    plot.config.data = {
        labels: args,
        datasets: [{
            label: name,
            data: vals,
            backgroundColor: "rgba(153,255,51,0.4)"
        }]
    };
    plot.update()
}

let p_expression = $("#p-func").val();
let S_expression = $("#S-func").val();
let z_expression = $("#z-func").val();
write_plot(p_expression, p_plot, 'w')
write_plot(S_expression, S_plot, 't')
write_plot(z_expression, z_plot, 't')

$('#p-func').on('input', function(event) {
    let expression = $('#p-func').val();
    write_plot(expression, p_plot, 'w')
});

$('#S-func').on('input', function(event) {
    let expression = $('#S-func').val();
    write_plot(expression, S_plot, 't')
});

$('#z-func').on('input', function(event) {
    let expression = $('#z-func').val();
    write_plot(expression, z_plot, 't')
});
