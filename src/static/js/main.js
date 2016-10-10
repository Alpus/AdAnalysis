let $tabs = $('.tabbable li');

$('#prevtab').on('click', function() {
    $tabs.filter('.active').prev('li').find('a[data-toggle="tab"]').tab('show');
});

$('#nexttab').on('click', function() {
    $tabs.filter('.active').next('li').find('a[data-toggle="tab"]').tab('show');
});

var p_func_ctx = document.getElementById('p-func-plot').getContext('2d');
var S_func_ctx = document.getElementById('S-func-plot').getContext('2d');
var z_func_ctx = document.getElementById('z-func-plot').getContext('2d');
var plot = undefined
function write_plot(name, expression, ctx, variable) {
    console.log(name, expression, ctx, variable)
    var parser = math.parser();

    args = []
    vals = []
    for (let number = 0.0; number < 1.02; number += 0.02) {
        args.push(Math.round(number * 100) / 100);
        parser.set(variable, number);
        vals.push(parser.eval(expression));
    }
    plot = new Chart(ctx, {
      type: 'line',
      data: {
        labels: args,
        datasets: [{
          label: name,
          data: vals,
          backgroundColor: "rgba(153,255,51,0.4)"
        }]
      }
    });
}

let p_expression = $("#p-func").val();
let S_expression = $("#S-func").val();
let z_expression = $("#z-func").val();
write_plot('p(w)', p_expression, p_func_ctx, 'w')
write_plot('S(t)', S_expression, S_func_ctx, 't')
write_plot('z(t)', S_expression, z_func_ctx, 't')

$('#p-func').on('input', function(event) {
    let expression = $('#p-func').val();
    write_plot('p(w)', expression, p_func_ctx, 'w')
});

$('#S-func').on('input', function(event) {
    let expression = $('#S-func').val();
    write_plot('S(t)', expression, S_func_ctx, 't')
});

$('#z-func').on('input', function(event) {
    let expression = $('#z-func').val();
    write_plot('z(t)', expression, z_func_ctx, 't')
});
