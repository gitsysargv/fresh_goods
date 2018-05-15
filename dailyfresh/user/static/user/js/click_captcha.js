$(function () {
    var error_c = true;  // 点击验证码错误，点击3次后转为false
    var count = 0;  //计数3次
    $('#img').click(function(event){
                count++;
                if(count>3){
                    return;
                }
                var $imag2 = $('<img>');  // 生成图标

                var x=event.offsetX;//获取点击时鼠标相对图片坐标
                var y=event.offsetY;

                $imag2.css({left:x, top:y, position:'absolute'}).prop({src:"/static/user/images/1.png"});
                $('#d').append($imag2);

                if(count===1){
                    $('#x1').val(x);
                    $('#y1').val(y);
                }
                else if(count===2){
                    $('#x2').val(x);
                    $('#y2').val(y);
                }
                else if(count===3){
                    $('#x3').val(x);
                    $('#y3').val(y);
                    error_c = false;
                }

            })

    // 点击切换图片验证码 改变src的地址，即改变get参数
    $('#hyg').click(function(){
        var $src = $("#img").prop('src') + '?';
        var $index = $src.indexOf('?')+1;
        $src = $src.substring(0, $index);
        $("#img").prop('src', $src+"date="+ new Date());
        // 重置数据
        count = 0;
        error_c = true;
        $('#d img').not('#img').remove();
    });

    $('#register').submit(function () {
        if (error_c == true){
            $('#d').next().html('请按顺序点击文字').show();
            return false;
        }
        else {
            $('#d').next().hide();
            return true;
        }
    })
});
