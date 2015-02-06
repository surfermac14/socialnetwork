$(function(){

	var getMsg = function(url1,tag){
		var $sentMessage = $(tag);
	var $item1;
	//console.log($sentMessage);

	$.getJSON(url1,{format:"json"});
	$.ajax({
		
		type: 'GET',
		url : url1,
		duration:5,
		success: function(sentMessages){
			$sentMessage.empty();
			$.each(JSON.parse(sentMessages),function(i,item){
					$sentMessage.append("<tr><td>"+item.name+" </td><td> "+item.message+"</td></tr>");
			})	;
		}
	});
	};

	
	

	// Message page switch between new,sent and received
	$('.my_list li a').on("click",function(){
	var p = $(this).closest("li").data("btn");
	var q=$('div').find(p);
	if(p==".sentMessages"){
		getMsg('/getSent','#sent');
	}
	if(p==".receivedMessages"){
		getMsg('/getReceived','#received');
	}
	
	$(".my_show").removeClass("my_show");
	q.addClass("my_show");
	});


	$('#submitmsg').on('click',function(){

		var $to =$('#to').val();
		
		var $msg = $('#msg').val();
		
		var obj = {

			name:$to,
			message:$msg
		};

		$.ajax({
			type: 'POST',
			url: '/sendmsg',
			data: obj,
			success:function(msgwithid){
				nothing =""
				$('#to').val(nothing);
				$('#msg').val(nothing);
			}
		});


	});
	

});