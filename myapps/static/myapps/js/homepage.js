$(function () {
    let width = 64;
    let height = 41;
    let $container = $('.container');
    let rows = $container.get(0).offsetHeight / height;
    let cols = $container.get(0).offsetWidth / width;
    for (let i = 0; i < rows - 1; i++) {
        for (let j = 0; j < cols - 1; j++) {
            let $item = $(`<div class="item"></div>`).css({
                "width": width + 'px',
                "height": height + 'px',
                "left": j * width + 'px',
                "top": i * height + 'px',
                "transition": `all 0.5s linear ${(i + j) * 0.1}s`
            });
            let $zheng = $(`<div class="zheng"></div>`).css({
                "background-position": `${-width * j}px ${-height * i}px`
            })
            $item.append($zheng);
            let $fan = $(`<div class="fan"></div>`).css({
                "background-position": `${-width * j}px ${-height * i}px`,
            });
            $item.append($fan);
            $container.append($item);
        }
    }
    let index = 1;
    $('.item').each(function () {
        console.log(1);
    })
    setInterval(() => {
        $('.item').each(function () {
            $(this).css('transform', `rotateY(${(index%2)*180}deg)`)
        });
        index++;
    }, 5000)
})