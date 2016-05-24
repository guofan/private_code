        var house_list_120;
        var house_list_90;
        var house_result_list_120;
        var house_result_list_90;
        var type;
        var mytime=null;
        var begin_num = 1;
        var random_num = 0;
        var index = 0;

        var resultlist = eval("house_result_list_"+type);
        if(resultlist.length != 0){
            $.each(resultlist,function(index, result){
                var createResult = $("<p></p>").css("margin-top","20px").text(index+":"+result);
                $("#result").prepend(createResult);
            });
        }
        function initdata(){
            $.ajax({type:"get",dataType:"json",url:"initdata",success:function(msg){
                    house_list_120 = msg["house_list_120"]
                    house_list_90 = msg["house_list_90"]
                    house_result_list_120 = msg["house_result_list_120"]
                    house_result_list_90 = msg["house_result_list_90"]
                }
            });
        }
        function doit(){
            var bt=window.document.getElementById("bt");

            if(mytime==null){
                index = $("#order-number").val();;
                console.log(index);
                bt.innerHTML="停止抽房";
                startshow();
                random_num = $.ajax({url:"/random?"+type, async:true});
                console.log(random_num)
            }else{
                bt.innerHTML="开始抽房";
                clearTimeout(mytime);
                mytime=null;
                stopshow();
            }
        }

        function stopshow(){
            var namelist;
            var resultlist;
            if (type == "90"){
                namelist = house_list_90;
                resultlist = house_result_list_90;
            } else {
                namelist = house_list_120;
                resultlist = house_result_list_120;
            }
            $("#order-number").val("");
            var box=window.document.getElementById("box");
            var num=parseInt(random_num.responseText);
            var result = namelist[num];
            namelist.splice(num, 1);
            resultlist.push(result);

            box.innerHTML=result;
            var createResult = $("<p></p>").css("margin-top","20px").text(index+":"+result);
            $("#result").prepend(createResult);
        }

        function startshow(){
            var namelist;
            if (type == "90"){
                namelist = house_list_90
            } else {
                namelist = house_list_120
            }

            var box=window.document.getElementById("box");
            var num=Math.floor((Math.random()*100000))%namelist.length;
            box.innerHTML=namelist[num];
            mytime=setTimeout("startshow()",1);
        }


