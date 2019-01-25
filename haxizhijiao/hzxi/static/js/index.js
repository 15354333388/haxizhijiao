/*科室人员首次页面*/
	$.ajax({
		type: "GET", //用POST方式传输
		url:http+'/index.php/beroung/Index/index', //目标地址
		dataType: "JSON", //数据格式:JSON
		data: {},
		success: function(data) {
		if(data.status==ok){	
		}else{
			alert(data.msg);
			}
		}
	})
	/*点击科室人员变化*/
	$("")


/*历史详情首次页面*/

	/*点击演练历史*/
	


	/*点击培训历史*/
	

	/*点击考核历史*/
	

/*最新考核、作业、培训*/