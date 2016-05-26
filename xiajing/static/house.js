        var house_list_120;
        var house_list_90;
        var house_result_list_120;
        var house_result_list_90;
        var type='120';
        var mytime=null;
        var begin_num = 1;
        var random_num = 0;
        var index = 0;
        
        function initdata(){
            $.ajax({type:"get",dataType:"json",url:"initdata",success:function(msg){
                    house_list_120 = msg["house_list_120"]
                    house_list_90 = msg["house_list_90"]
                    house_result_list_120 = msg["house_result_list_120"]
                    house_result_list_90 = msg["house_result_list_90"]
                    chooseHouseType(type);
                }
            });
        }
        function setAllbtUnclick() {
            var divlist = $(".nav-container > div");
            for(var i = 0; i < divlist.length; i++){
                id=divlist[i].id;
                $("#"+id).css("color","#CD7F32");
            }
        }
        function setResultList(type){
			$("#order-number").val("");
			//clear result list
			$("#result").empty();
			var resultlist;
			var namelist;
			var result_num = 0;
            if (type == "90"){
				namelist = house_list_90;
                resultlist = house_result_list_90;
            } else {
				namelist = house_list_120;
                resultlist = house_result_list_120;
            }
			var new_keylist = new Array();
			for(var key in resultlist){
				result_num++;;
				new_keylist.push(key);
			}
			new_keylist.sort();
			for(var i = 0; i < new_keylist.length; i++){
				var index = new_keylist[i];
				var result = resultlist[index];
	            var createResult = $("<p></p>").css("margin-top","20px").text(index+":"+result);
    	        $("#result").prepend(createResult);
			}
			//set remain list
			$("#house-number-sold").text(""+result_num);
			$("#house-number-remain").text(""+namelist.length);
		}
        function chooseHouseType(housetype){
            setAllbtUnclick();
            $("#"+housetype+"bt").css("color","red");
            type = housetype;
			setResultList(type);
            var box=window.document.getElementById("box");
            box.innerHTML="准备抽取"+housetype+"房型";
            console.log(type);
        }
        function doit(){
            var bt=window.document.getElementById("bt");

            if(mytime==null){
                index = $("#order-number").val();;
                if(index == "") {
		            alert("请填写序号");
         		    return;
		        }
	            var resultlist;
    	        if (type == "90"){
        	        resultlist = house_result_list_90;
            	} else {
                	resultlist = house_result_list_120;
				}
				if(parseInt(index) in resultlist){
					alert("该序号已经抽取过！请重新填写");
					return;
				}
                bt.innerHTML="停止抽房";
                startshow();
                var random_url = "/random?type="+type+"&index="+index;
                $.ajax({url:random_url, async:false, success:function(msg){
                    console.log(msg);
        		    random_num = parseInt(msg);
		        }});
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
            var num=random_num;
            var result = namelist[num];
            namelist.splice(num, 1);
            resultlist[index] = result;

            box.innerHTML=result;
            var createResult = $("<p></p>").css("margin-top","20px").text(index+":"+result);
            $("#result").prepend(createResult);
			var result_num = 0;
			for(var key in resultlist){
				result_num++;
			}
			//set remain list
			$("#house-number-sold").text(""+result_num);
			$("#house-number-remain").text(""+namelist.length);
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


