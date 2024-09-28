/**
 * 命名空间
 */
jQuery.namespace = function(){
    var a=arguments, o=null, i, j, d, rt;
    for (i=0; i<a.length; ++i) {
        d=a[i].split(".");
        rt = d[0];
        eval('if (typeof ' + rt + ' == "undefined"){' + rt + ' = {};} o = ' + rt + ';');
        for (j=1; j<d.length; ++j) {
            o[d[j]]=o[d[j]] || {};
            o=o[d[j]];
        }
    }
}

jQuery.namespace('tp.dic');
tp.dic.data={
		get:function(code){
	        //如果页面上没有缓存
	        if(!tp.dic.data[code]){
	            $.ajax({
	                url : contextpath+"/sys/uacm/dicm/dic"  ,
	                async : false ,
	                type : "POST",
	                data : {
	                    code : code
	                },
	                success : function(ret_dic){
	                    tp.dic.data[code] = ret_dic ;
	                },
	                error : function(){
	                    if(window.console){
	    					console.log("获取"+code+"字典表失败");
	    				}
	                }
	            });
	        }
	        return tp.dic.data[code] ;
		}
};

tp.dic.language={
		get:function(code){
			if(isI18n != 'true' || Util.isChinese(code)){
				//如果没有启用国际化
				return code ;
			}
	        //如果页面上没有缓存
	        if(!tp.dic.language[code]){
	            $.ajax({
	                url : contextpath+"/sys/uacm/language/data"  ,
	                async : false ,
	                dataType : 'text' ,
	                type : "POST",
	                data : {
	                    code : code
	                },
	                success : function(ret_dic){
	                	//如果开启了国际化，并且没有获取到code对应的值，则直接返回code
	                	if(ret_dic){
	                		tp.dic.language[code] = ret_dic ;
	                	}else{
	                		tp.dic.language[code] = code ;
	                	}
	                },
	                error : function(){
	                    if(window.console){
	    					console.log("获取"+code+"国际化失败");
	    				}
	                }
	            });
	        }
	        return tp.dic.language[code] ;
		}
}

/**
 * 获取URL上面的参数
 * @param $
 */
;(function ($) {
    $.extend({
        getParameter: function (name) {
            function parseParams() {
                var params = {},
                    e,
                    a = /\+/g,  // Regex for replacing addition symbol with a space
                    r = /([^&=]+)=?([^&]*)/g,
                    d = function (s) { return decodeURIComponent(s.replace(a, " ")); },
                    q = window.location.search.substring(1);

                while (e = r.exec(q))
                    params[d(e[1])] = d(e[2]);

                return params;
            }

            if (!this.queryStringParams)
                this.queryStringParams = parseParams();

            return this.queryStringParams[name];
        }
    });
})(jQuery);

/**
 * form表单序列化为json
 */
$.fn.serializeJson=function(){
    var serializeObj={};
    $(this.serializeArray()).each(function(){
        serializeObj[this.name]=this.value;
    });
    return serializeObj;
};


/**
 * 日期格式化
 */
(function($){
    $.formatDate = function(pattern,date){
        //如果不设置，默认为当前时间
        if(!date) date = new Date();
        if(typeof(date) ==="string" || typeof(date) ==="number"){
             if(date==""){
            	 date = new Date()
             } else {
	             date = new Date((date+"").replace(/-/g,"/")*1);
             }

        }
        /*补00*/
        var toFixedWidth = function(value){
             var result = 100+value;
             return result.toString().substring(1);
        };

        /*配置*/
        var options = {
                regeExp:/(yyyy|M+|d+|h+|m+|s+|ee+|ws?|p)/g,
                months: ['January','February','March','April','May',
                         'June','July', 'August','September',
                          'October','November','December'],
                weeks: ['Sunday','Monday','Tuesday',
                        'Wednesday','Thursday','Friday',
                            'Saturday']
        };

        /*时间切换*/
        var swithHours = function(hours){
            return hours<12?"AM":"PM";
        };

        /*配置值*/
        var pattrnValue = {
                "yyyy":date.getFullYear(),                      //年份
                "MM":toFixedWidth(date.getMonth()+1),           //月份
                "dd":toFixedWidth(date.getDate()),              //日期
                "hh":toFixedWidth(date.getHours()),             //小时
                "mm":toFixedWidth(date.getMinutes()),           //分钟
                "ss":toFixedWidth(date.getSeconds()),           //秒
                "ee":options.months[date.getMonth()],           //月份名称
                "ws":options.weeks[date.getDay()],              //星期名称
                "M":date.getMonth()+1,
                "d":date.getDate(),
                "h":date.getHours(),
                "m":date.getMinutes(),
                "s":date.getSeconds(),
                "p":swithHours(date.getHours())
        };

        return pattern.replace(options.regeExp,function(){
               return  pattrnValue[arguments[0]];
        });
    };

})(jQuery);

/**
 * json对象load到form上
 */
$.fn.loadFormData = function(data){
    return this.each(function(){
        var input, name;
        if(data == null){this.reset(); return; }
        for(var i = 0; i < this.length; i++){
            input = this.elements[i];
            //checkbox的name可能是name[]数组形式
            name = (input.type == "checkbox")? input.name.replace(/(.+)\[\]$/, "$1") : input.name;
            if(data[name] == undefined) continue;
            switch(input.type){
                case "checkbox":
                    if(data[name] == ""){
                        input.checked = false;
                    }else{
                        //数组查找元素
                        if(data[name].indexOf(input.value) > -1){
                            input.checked = true;
                        }else{
                            input.checked = false;
                        }
                    }
                break;
                case "radio":
                    if(data[name] == ""){
                        input.checked = false;
                    }else if(input.value == data[name]){
                        input.checked = true;
                    }
                break;
                case "button": break;
                default: input.value = data[name];
            }
        }
    });
};

/**
 * 公共方法
 */
var Util = {
		load : function(url , before , after){
			layer.closeAll();
			if(url){

				Util.run = null ;
				$(window).unbind("hashchange");
				$.ajaxSetup({ cache: true }) ;

				// 增加外部嵌入
				url = decodeURIComponent(url);
				if(url.indexOf("http://")!=-1 || url.indexOf("https://")!=-1){
					$("#page-content").html("<iframe id='tpContainerIframe' src='"+url+"' style='width:100%;height:690px; border: medium none;'/>");
					window.addEventListener('message',function(e){
						$("#tpContainerIframe").height(e.data);
					 });
					return ;
				}

				var perm_item_id = $("a[perm_item_url='"+url+"']").attr("perm_item_id");

//				try{
//					if (!!(window.attachEvent && !window.opera)) {
//					 	document.execCommand("stop");
//					} else {
//					 	window.stop();
//					}
//				}catch(e){}

				$("#page-content").load(url , "item_id="+perm_item_id ,  function(data,status,xhr){
					//如果加载时候出现错误
					if(xhr.status == '0' && xhr.statusText=='error'){
						$(this).empty();
						setTimeout( "Msg.reloadPage()" , 5000);//5秒后提示过期
						return ;
					}else if(status == "error" && (xhr.status==500||xhr.status==404)){
						$("#page-content").html(data);
					}

					//解决hash值后面带参数的问题（如#a=1?b=2这种写法）
					if(url.indexOf("?")!=-1){
						back_act_listener = url.substring(0 , url.indexOf("?"));
					}else{
						back_act_listener = url ;
					}
					//添加数据中心需要使用的参数
					var finalMenuItem = Util.getHash(location.hash , 'finalMenuItem');
					var cpparams = Util.getHash(location.hash , 'cpparams');
					var targetact = "";
					if(cpparams!="cpparams"&&cpparams!=""){
						cpparams = template.BASE64.decode(cpparams);
						cpparams =  JSON.parse(cpparams);
						targetact = cpparams.targetact;
					}
					//记住跳转的菜单(如果当的地址和传递进来的不一样)
					var _act = Util.getHash(location.hash , 'act') ;
					if(_act!=back_act_listener && _act.indexOf(back_act_listener+"?")==-1){
						if(!finalMenuItem&&!Util.isNotEmpty(targetact)){
							Util.setHash("#act=" + back_act_listener);
						}

					}
					//如果存在配置平台配置按钮删除
					if($(".fm-ul").length>0){
						$(".fm-ul").remove();
					}
					//如果是配置平台不加载运行前函数
					if(url.indexOf("cp/templateList/p")<0||(url.indexOf("cp/templateList/p")>-1&&cpparams=="")){
						//运行前回调函数
						if(typeof before == 'function'){
							before(data);
						};
					}

					//执行入口函数
					if(Util.run && typeof Util.run == 'function')Util.run();

					//初始化页面中的下拉字典
					Util.initSysDic();

					//初始化页面中的模糊匹配自动填充
					Util.autocomplete();

					//二级tab滑动
					Util.swiperTab();

					//运行后回调函数
					if(typeof after == 'function'){
						after(data);
					};

					//用户行为记录入库
					if(Util.UserBehaviorAnalysis){
						var leave =  Date.parse(new Date()) / 1000 ;
						Util.ajax({
							url : contextpath + "/comm/ub" ,
							param : $.extend(Util.UserBehaviorAnalysis,{
								leave : leave ,
								location : url ,
								times : leave - Util.UserBehaviorAnalysis.now
							})
						});
					}
					var parser = new UAParser();
					Util.UserBehaviorAnalysis = {
						now : Date.parse(new Date())/1000 ,
						referrer : url ,
						browser : parser.getResult().browser.name ,
						browser_v : parser.getResult().browser.version ,
						os :parser.getResult().os.name ,
						os_v : parser.getResult().os.version ,
						device : parser.getResult().ua
					}

				});
				if(typeof window.globalTPCallback == 'function'){
					window.globalTPCallback();
				};
			}
		} ,
		/**
		 * 通过 from 中的条件分页检索数据列表
		 * @param data
		 */
		getPageObjListByForm : function(data){
			if(!data || !data.formId){
				if(window.console){
					console.log("参数异常：请通过参数formId 指定from的ID。");
				}
				return  ;
			}

			var _from = $("#"+data.formId) ;
			if(!_from.attr("action")){
				if(window.console){
					console.log('参数异常：id为'+data.formId+'的form尚未配置action属性。');
				}
				return  ;
			}

			var param = {} ;
			var arr = _from.serializeArray();
			$(arr).each(function(i,o){
				if(o.value!=''){
					if(param[o.name]){
						param[o.name] = param[o.name]+","+o.value ;
					}else{
						param[o.name] = o.value ;
					}
				}
			});
			data['data'] = $.extend(data.data,param);
			data['url'] = _from.attr("action") ;
			this.getPageObjList(data);
		} ,
		//通过指定参数{}分页获取数据
		getPageObjList : function(data){
			if(!data || !data.url){
				if(window.console){
					console.log('getPageObjList方法中尚未配置url请求地址。');
				}
				return ;
			}
			data.param = data.data||{} ;
			data.param['pageNum'] = data.param['pageNum']||1  ;
			data.param['pageSize'] = data.param['pageSize']||10 ;
			this.ajax(data);
		},
		/**
		 * 通过 form 提交表单添加记录
		 * @param data
		 */
		addByForm : function(data){
			if(!data || !data.formId){
				if(window.console){
					console.log('参数异常：请通过参数formId 指定from的ID。');
				}
				return  ;
			}

			var _from = $("#"+data.formId) ;
			if(!_from.attr("action")){
				if(window.console){
					console.log('参数异常：id为'+data.formId+'的form尚未配置action属性。');
				}
				return  ;
			}

			//如果指明不去校验
			if(!data.ignoreValidate){
				//如果有自定义的校验规则
				if(data.validateRules && !_from.validate(data.validateRules).form()){
					return ;
				}
				if(!_from.validate().form()){
					return ;
				}
			}

			//校验通过之后，往后台发请求之前，将按钮禁用，避免重复提交
			$("#"+data.submitBtn).attr("disabled","disabled");
			$("#"+data.cancelBtn).attr("disabled","disabled");

			var param = {} ;
			//遍历form元素
			var arr = _from.serializeArray();
			$(arr).each(function(i,o){
//				if(o.value!=''){
					if(param[o.name]){
						param[o.name] = param[o.name]+","+o.value ;
					}else{
						param[o.name] = o.value ;
					}
//				}
			});
			//遍历自动填充元素，覆盖掉原有的值
//			_from.find('input[autocomplete=true]').each(function(i,o){
//				param[$(o).attr("name")] = $(o).attr("real-value") ;
//			});
			data['param'] = $.extend(param,data.param) ;
			data['url'] = _from.attr("action") ;

			this.ajax(data);
		} ,
		/**
		 * 与服务端交互
		 * @param data
		 */
		ajax : function(data){
			if(!data || !data.url){
				if(window.console){
					console.log('ajax方法中尚未配置url请求地址。');
				}
				return ;
			}
			var loading = "" ;
			$.ajax({
			    type: data.method || "POST",
			    url: data.url,
			    async : data.async==undefined?true:data.async ,
			    data: data.desEnode?DESUtils.encode(JSON.stringify(data.param||{}),"ehalldes"):JSON.stringify(data.param||{}),
			    dataType : data.dataType || "json",
			    contentType : 'application/json;charset=utf-8',
			    success: function(result){
			    	if(data.success && typeof(data.success) == "function"){
			    		data.success(result);
			    	}
			    },
			    error: function(err){
			    	if(err.status==200 && err.statusText=="OK" && data.success && typeof(data.success) == "function"){
			    		data.success(err.responseText);
			    		return ;
			    	}
			    	if(data.error && typeof(data.error) == "function"){
			    		data.error(err);
			    	}
			    } ,
			    beforeSend : function(){
			    	if(data.loading){
			    		loading = Msg.load();//发送请求之前显示loading
			    	}
			    } ,
			   complete: function( xhr ){
				   if(xhr.status==403){
					   Msg.info(tp_common_quan_xian_bu_zu , function(){
			    			Util.load(contextpath+"/403");
			    		});
			    	}
			        if(loading) Msg.close(loading);
			        if(xhr.status == '0' && xhr.statusText=='error'){
			        	setTimeout( "Msg.reloadPage()" , 5000);//5秒后提示过期
					}
		       }
			});
		},
		/**
		 * layer分页
		 * @param param
		 * @param type 1：只显示mini分页；2：按照宽度显示分页样式
		 */
		laypageMini : function(param , type){
			var miniPage = '<div id="layer_page_' +param.pageId+ '" class="bar pagejump-mini-con push-up-20">' +
			'	<div class="pagejump-box pull-right">' +
			'		<a id="mini_page_prev_'+param.pageId+'" class="prev fa fa-chevron-left"></a>' +
			'		<div class="pagejump-inputbox">' +
			'			<input id="mini_page_text_'+param.pageId+'" class="form-control pull-left" type="text"/>' +
			'		</div>' +
			'		<a id="mini_page_next_'+param.pageId+'" class="next fa fa-chevron-right"></a>' +
			'		<a id="mini_page_jump_'+param.pageId+'" class="btn btn-default pull-left push-left-10">'+tp_common_go+'</a>' +
			'	</div>' +
			'	<div class="pagejump-info pull-right"><span>'+param.data.pageNum+'</span><span>/</span><span>'+param.data.pages+'</span></div>' +
			'</div>' ;
			if(1==type){
				$("#"+param.pageId).html(miniPage);
			}else if(2==type){
				$("#"+param.pageId).append(miniPage);
				$("#layer_page_"+param.pageId).hide();
			}

			//向前的监听
			$("#mini_page_prev_"+param.pageId).click(function(){
				if(param.data.pageNum!=1 && typeof(param.callback) == "function"){
					if(param.callbackParam && param.callbackParam.length>0){
		        		param.callback(--param.data.pageNum , param.data.pageSize , param.callbackParam[0] , param.callbackParam[1] ,
		        				param.callbackParam[2] , param.callbackParam[3] , param.callbackParam[4] ,
		        				param.callbackParam[5] , param.callbackParam[6] , param.callbackParam[7]);
		        	}else{
		        		param.callback(--param.data.pageNum , param.data.pageSize);
		        	}
				}
			});
			//向后的监听
			$("#mini_page_next_"+param.pageId).click(function(){
				if(param.data.pageNum!=param.data.pages && typeof(param.callback) == "function"){
					if(param.callbackParam && param.callbackParam.length>0){
		        		param.callback(++param.data.pageNum , param.data.pageSize , param.callbackParam[0] , param.callbackParam[1] ,
		        				param.callbackParam[2] , param.callbackParam[3] , param.callbackParam[4] ,
		        				param.callbackParam[5] , param.callbackParam[6] , param.callbackParam[7]);
		        	}else{
		        		param.callback(++param.data.pageNum , param.data.pageSize);
		        	}
				}
			});
			//跳转的监听
			$("#mini_page_jump_"+param.pageId).click(function(){
				var page = $("#mini_page_text_"+param.pageId).val();
				if(page>0 && page<=param.data.pages && typeof(param.callback) == "function"){
					param.callback(page , param.data.pageSize);
				}
			});
		},
		/**
		 * 渲染模板
		 * @param param
		 */
		renderTemplet : function(param){
			if(!param || (!param.templetId && !param.contentHTML)){
				if(window.console){
					console.log('尚未指定模板。');
				}
			}else if(!param.containerId){
				if(window.console){
					console.log('尚未指定容器Id。');
				}
			}else if(param.data==undefined || param.data==''){
				$("#"+param.containerId).html(template(param.templetId));
			}else if(param.pageId && param.data.list && param.data.list.length>0){
				if(param.templetId){
					$("#"+param.containerId).html(template(param.templetId, {'data':param.data}));
				}else{
					var render = template.compile(param.contentHTML);
					$("#"+param.containerId).html(render({'data':param.data}));
				}
				if(param.pageId && param.data.pages>0){
					//显示声明mini分页
					if("mini" == param.pageType){
						this.laypageMini(param , 1);
						return ;
					}
					//如果没有定义为 mini ，则初始化响应式显示
					layui.laypage.render($.extend({
					    elem: param.pageId
					    ,count: param.data.total
					    ,curr: param.data.pageNum
						,limit : param.data.pageSize
					    ,limits : [10,50,100,500,1000]
						//,theme : '#c00'
					    ,layout: ['limit', 'skip', 'prev', 'page', 'next']
					    ,jump: function(obj, first){
					        if(!first && typeof(param.callback) == "function"){
					        	if(param.callbackParam && param.callbackParam.length>0){
					        		param.callback(obj.curr , obj.limit , param.callbackParam[0] , param.callbackParam[1] ,
					        				param.callbackParam[2] , param.callbackParam[3] , param.callbackParam[4] ,
					        				param.callbackParam[5] , param.callbackParam[6] , param.callbackParam[7]);
					        	}else{
					        		param.callback(obj.curr , obj.limit);
					        	}
							}
					    }
					  },param));
					//初始化mini分页
					this.laypageMini(param , 2);

					$("#"+param.pageId+" ."+"layui-laypage").width("100%");
					$("#"+param.pageId+" ."+"layui-laypage-limits").addClass("pull-left");
					$("#"+param.pageId+" ."+"layui-laypage-skip").before('<span class="pull-left layui-laypage-count">当前第 '+param.data.startRow+' - '+param.data.endRow+' 条 共计 '+param.data.total+' 条</span>');

					//如果没有定义为 mini或者扩展自定义分页 ，则响应式显示
	            	function assertShowPageTool(){
	            		var wid = $(window).width() ;
	            		if(wid<960){
	            			$("#"+param.pageId+" ."+"layui-laypage").hide();
	            			$("#layer_page_"+param.pageId).show();
	            		}else{
	            			$("#layer_page_"+param.pageId).hide();
	            			$("#"+param.pageId+" ."+"layui-laypage").show();
	            		}
	            	}
	            	var resizeTimer = null;
	            	$(window).bind('resize', function (){
	            		if (resizeTimer) clearTimeout(resizeTimer);
	            		resizeTimer = setTimeout(assertShowPageTool() , 500);
	            	});
					//响应式显示
	            	assertShowPageTool();
				}
			}else if(param.pageId && param.data.list && param.data.list.length==0){
				if(Boolean(param.nodatacolums)){
					$("#"+param.containerId).html("<tr><td colspan='"+param.nodatacolums+"'>未检索到记录<td></tr>");
				}else{
					$("#"+param.containerId).html(tp_common_weijiansuodaojilu);
				}
				$("#"+param.pageId).empty();
			}else if(param.data!=undefined){
				$("#"+param.containerId).html(template(param.templetId, param.data));
			}else{
				$("#"+param.containerId).html(tp_common_weijiansuodaojilu);
				$("#"+param.pageId).empty();
			}
			//初始化字典
			Util.initSysDic($("#"+param.containerId).find("select"));
			//初始化自动填充
			Util.autocomplete($("#"+param.containerId).find("input[autocomplete=true]"));
			Util.autocomplete($("#"+param.containerId).find("input[automatictp=true]"));
		},
		/**
		 * @param calback 成功之后的回调
		 * @param async true异步调用（默认）；false同步调用
		 * @returns {String}
		 */
		getToken : function(calback , async){
			var token = "" ;
			$.ajax({
			  url: contextpath+"/getToken",
			  type : "POST" ,
			  async: async===false?false:true ,
			  success : function(data){
					if(typeof calback == "function"){
						calback(data);
					}
					token =  data ;
				}
			});
			return token ;
		},
		/**
		 * 删除选中的记录
		 * @param data
		 */
		deleteRecord : function(data){
			if(!data || !data.url){
				if(window.console){
					console.log('请传url参数。');
				}
				return ;
			}
			if(data.records.length>0){
				Msg.confirm(data.msg||tp_common_querenshanchu,function(){
					$.ajax({
						url : data.url ,
						type: "POST",
						data : {
							ids : typeof data.records == 'object' ? data.records.join(',') : data.records ,
							mapping : data.mapping
						},
						success : function(result){
							//删除成功之后将复选框的状态取消
							$("input[type='checkbox']").prop('checked',false);
							if(data.success && typeof(data.success) == "function"){
					    		data.success(result);
					    		Msg.success();
					    	}else{
					    		Msg.success();
					    	}
						},
						error:function(){
							Msg.error();
						}
					});
				});
			}else{
				Msg.warning(tp_common_xuanzeshanchujilu);
			}
		},
		/**
		 * 渲染datatables
		 * @param param
		 * @returns
		 */
		dataTables : function(param){
            if(!param.NoKeyDown){
			  //回车事件formId
			  $("#"+param.formId).keydown(function(e){
				 var e = e || event,
				 keycode = e.which || e.keyCode;
				 if (keycode==13 && common.action.dataTable) {
					 common.action.dataTable.ajax.reload();
				 }
			  });
			}
			if(!param.gridId){
				if(window.console){
					console.log('请传递渲染的DOM元素');
				}
				return ;
			}
			if(!param.columns){
				if(window.console){
					console.log('请传递渲表格的 columns 参数');
				}
				return ;
			}
			if(param.formId){
				var _form = $("#"+param.formId) ;
				//如果 url 为空则将form的action作为 url
				if(!param.url && $(_form).attr("action")){
					param.url = $(_form).attr("action") ;
				}
				var fParam = {} ;
				var arr = _form.serializeArray();
				if(arr.length>0){
					//获取form中的所有表单项
					$(arr).each(function(i,o){
						if(o.value!=''){
							if(fParam[o.name]){
								fParam[o.name] = fParam[o.name]+","+o.value ;
							}else{
								fParam[o.name] = o.value ;
							}
						}
					});
				}
				//form中的参数附加到自己传递的参数
				param.data = $.extend(fParam,param.data);
			}

			if(!param.url && !param.localData){
				if(window.console){
					console.log('请传递请求数据的 url 参数');
				}
				return ;
			}
			//固定操作列-wenhm
			var is_opt=false;
			if($('#'+param.gridId).find("thead tr").find("th:last-child").html()=="操作") {
				is_opt = true;
			}
			//默认是显示行号
//			if(param.hideRowNumber!=true){
//				$("#"+param.gridId).find("tr").first().prepend("<th style='width: 56px;' id='"+param.gridId+"_dt_row_num'><i class='fa fa-list-ol'></i></th>");
//				if(!(typeof param.columns[0].data=='function' && param.columns[0].data()=='dt_row_number')){
//					param.columns.unshift({data: function(){return "dt_row_number";}});
//				}
//			}

			var options = '<option value="10">10</option>' +
        	'<option value="50">50</option>' +
        	'<option value="100">100</option>' +
        	'<option value="500">500</option>' +
        	'<option value="1000">1000</option>' ;
			if(param.aLengthMenu && param.aLengthMenu[0]){
				options = "" ;
				$(param.aLengthMenu[0]).each(function(i , o){
					options += '<option value="'+o+'">'+o+'</option>' ;
				});
			}

			//固定操作列-wenhm
			var dataTablesPage = {
	        	//Custom lengthmenu style ren.jq
				sLengthMenu : '<div class="pull-left push-right-10">'+tp_common_meiyexianshi+'</div><select class="form-control pull-left select" style="font-size:12px;">' +
	        	options +
	        	'</select><div class="pull-left push-left-10">'+tp_common_tiao+'</div>',
	        	sZeroRecords : tp_common_weijiansuodaojilu,
	        	//sProcessing : "&lt;img src=’./loading.gif’ /&gt;",
	        	sInfo : tp_common_current_item + " _START_ - _END_ "+tp_common_tiao+"　"+tp_common_total_item+" _TOTAL_ "+tp_common_tiao,
	        	sInfoEmpty : tp_common_weijiansuodaojilu,
	        	sInfoFiltered : "(从 _MAX_ 条记录中过滤)",
	        	sSearch : "搜索：",
	        	oPaginate : {
	        		sFirst : tp_common_shouye ,
	        		sPrevious : tp_common_qianyiye,
	        		sNext : tp_common_houyiye,
	        		sLast : tp_common_weiye
		        },
		        sZeroRecords: tp_common_weijiansuodaojilu
	        };
			//如果是mini分页
			if(param.pageType=="mini"){
				dataTablesPage = {
			        	sLengthMenu : '',
			        	sZeroRecords : tp_common_weijiansuodaojilu,
			        	sInfo : "",
			        	sInfoEmpty : tp_common_weijiansuodaojilu,
			        	sInfoFiltered : "",
			        	sSearch : "搜索：",
			        	oPaginate : {
			        		sFirst : tp_common_shouye,
			        		sPrevious : "<<",
			        		sNext : ">>",
			        		sLast : tp_common_weiye
				        },
				        sZeroRecords: tp_common_weijiansuodaojilu
			        };
			}
			var table = $.extend({
				processing: false,//显示正在处理的加载
		        paging: true, //翻页功能
		        searching: false ,//隐藏掉检索框
		        iDisplayLength : (param.data && param.data.pageSize) ? param.data.pageSize : 10,
		        bFilter: false, //过滤功能
		        bSort: false, //排序功能
		        bSortMulti :  false ,
		        bSearchable : false ,
		        bInfo: true,//页脚信息
		        bLengthChange : true , //隐藏左上角分页
		        aLengthMenu : param.aLengthMenu || [[10, 50, 100,500,1000], [10, 50, 100,500,1000]]  ,
		        fnDrawCallback: function(obj){
		        	$('#'+param.gridId+"_length").find("select").each(function() {
						$(this).selectpicker();
					});
		        	if(param.pageType=="mini"){
		        		//如果是小窗口，则隐藏自定义跳转
		        		$("#div_dt_pgo"+param.gridId).hide();
		        		//第几页的按钮隐藏
		        		$("#"+param.gridId+"_paginate").find("span").hide();
		        	}
		        	if(obj && obj.json && obj.json.total>0){
		        		$('#'+param.gridId+"_length").show();
		        	}else{
		        		$('#'+param.gridId+"_length").hide();
		        	}

		        	//文本框键盘监听跳转到第几页
		        	function dt_pgo_key_up(e , _this){
		            	//只能输入数字
		            	if(! /^\d+$/.test(_this.value)){
		            		_this.value = parseInt(_this.value);
		                }
		                if(e.keyCode==13){
		                	//小数转整数
		                	this.value = parseInt(_this.value);
		                	//大于0才分页
			                if($(_this).val() && $(_this).val()>0){
			                    var redirectpage = $(_this).val()-1;
			                }else{
			                    var redirectpage = 0;
			                }
			                $('#'+param.gridId).dataTable().fnPageChange(redirectpage);
		                }
		            }
		            $('#dt_pgo'+param.gridId).keyup(function(e){
		            	dt_pgo_key_up(e, this);
		            });
		            $('#dt_mini_pgo'+param.gridId).keyup(function(e){
		            	dt_pgo_key_up(e , this);
		            });

		            //点击跳转按钮
		            function jump_page_btn_go(input_dom){
		            	var redirectpage = $('#' + input_dom + param.gridId).val();
		            	if(redirectpage>0){
		            		$('#'+param.gridId).dataTable().fnPageChange(redirectpage-1);
		            	}else{
		            		Msg.warning(tp_common_hefayema);
		            	}
		            }
		            $("#jump_page_btn"+param.gridId).click(function(){
		            	jump_page_btn_go("dt_pgo");
		            });
		            $("#jump_page_mini_btn"+param.gridId).click(function(){
		            	jump_page_btn_go("dt_mini_pgo");
		            });

		            if(param.pageType!='mini' && !param.sPaginationType){
		            	//如果没有定义为 mini或者扩展自定义分页 ，则响应式显示
		            	function assertShowFoobar(){
		            		var wid = $(window).width() ;
		            		if(wid<960){
		            			$("#"+param.gridId + "_length").hide();
		            			$("#"+param.gridId + "_info").hide();
		            			$("#"+param.gridId + "_previous").text("<");
		            			$("#"+param.gridId + "_next").text(">");
		            			$("#div_dt_pgo"+param.gridId).hide();
		            			$("#div_dt_mini_pgo"+param.gridId).show();
		            		}else{
		            			$("#"+param.gridId + "_previous").text(tp_common_qianyiye);
		            			$("#"+param.gridId + "_next").text(tp_common_houyiye);
		            			$("#"+param.gridId + "_length").show();
		            			$("#"+param.gridId + "_info").show();
		            			$("#div_dt_pgo"+param.gridId).show();
		            			$("#div_dt_mini_pgo"+param.gridId).hide();
		            		}
		            	}
		            	assertShowFoobar();
		            	var resizeTimer = null;
		            	$(window).bind('resize', function (){
		            		if (resizeTimer) clearTimeout(resizeTimer);
		            		resizeTimer = setTimeout(assertShowFoobar() , 500);
		            	});
		            }

		            //行号
		            if(param.showRowNumber==true){
		            	var api = this.api();
		            	var startIndex= api.context[0]._iDisplayStart;//获取到本页开始的条数
		            	api.column(param.rowNumColumnIndex).nodes().each(function(cell, i) {
		            		cell.innerHTML = (startIndex + i + 1) ;
		            		//解决串列
		            		$("#"+param.gridId+"_dt_row_num").css("width" , cell.innerHTML.length);
		            	});
		            }
		            //渲染后执行自定义回调
		            if(typeof param.drawCallback == "function"){
		        		param.drawCallback(obj);
		        	}
		        },
		        aoColumnDefs: [
					{
						"bSortable": false,
						"aTargets": ['unsortable']//标题添加class:unsortable禁用此列排序功能
					}
				],
		        bAutoWidth: true,//自动宽度
		        errMode : "none" ,
		        //Custom elements order ren.jq
		        sDom: '<"top">rt<"bottom"lip><"clear">',
		        oLanguage: dataTablesPage ,
		        sScrollX: true,  //此处不能为空 maqt
		        sScrollXInner: "100%",  //此处设置为110%之后，所有的Grid都会出现滚动条，暂时设置为空
		        bScrollCollapse: true ,
		        bStateSave: true ,
		        initComplete : function(settings, json){
		        	if(typeof param.callback == "function"){
		        		param.callback(settings, json);
		        	}
		        	//全选功能
		        	$('#'+param.gridId+"_wrapper").find("input[name='check_all']").change(function(){
		        		if($(this).is(":checked")){
		        			$('#'+param.gridId+"_wrapper tr").each(function(){
		        				$(this).find("td:first").find("input[type='checkbox']").prop('checked','checked');
		        			});
		        			$('#'+param.gridId+"_wrapper").find("tbody tr").addClass('active');
		        		}else{
		        			$('#'+param.gridId+"_wrapper tr").each(function(){
		        				$(this).find("td:first").find("input[type='checkbox']").prop('checked',false);
		        			});
		        			$('#'+param.gridId+"_wrapper").find("tbody tr").removeClass('active');
		        		}
		        	});
		        	//翻页之后将全选去掉
//		        	$('#'+param.gridId+"_paginate").on("click", "a", function() {
//		                $('#'+param.gridId+"_wrapper").find("input[name='check_all']").prop('checked',false);
//		            });
		        }
		    }, param);
			//固定操作列-wenhm & ren.jq
			if(is_opt){
				if($(window).width()<768) {
				}else{
					if(param.fixedColumns!="0") {
						table = $.extend(table,{fixedColumns:{
							leftColumns: 0,
							rightColumns: 1
						}})
					}
				}
			}
			//固定操作列-wenhm & ren.jq
			if(param.url){
				var loading = "" ;
				//如果加载后台数据
				table = $.extend(table , {
					serverSide: true,
			        bServerSide : true ,
			        ajax: {
			        	data : param.data || {} ,
			        	url: param.url ,
			            type: "POST",
			            dataSrc: "list" ,
					    dataType:"json",
					    contentType : 'application/json;charset=utf-8' ,
					    error : function(xhr, msg){
					    	layer.closeAll();
					    	layer.msg(tp_common_requesterror);
					    } ,
					    beforeSend : function(){
					    	if(param.loading){
					    		loading = Msg.load();//发送请求之前显示loading
					    	}
					    } ,
					    complete: function( xhr , a ,b){
				        	//每次重新加载之后将全选去掉
				            $('#'+param.gridId+"_wrapper").find("input[name='check_all']").prop('checked',false);

					    	if(xhr.status==403){
					    		Msg.info(tp_common_quan_xian_bu_zu,function(){
					    			Util.load(contextpath+"/403");
					    		});
					    	}
					    	if(loading) Msg.close(loading);
					        if(xhr.status == '0' && xhr.statusText=='error'){
					        	setTimeout( "Msg.reloadPage()" , 5000);//5秒后提示过期
							}
					        //以下是服务配置管理的操作按钮，鼠标悬停时弹出下拉操作菜单的部分，fp特有
					      //Util.swiperDbtn();
					        $(".hover-drop-btn").mouseover(function(){
								$(this).parent(".hover-drop").addClass("open");
								var optmun = $(this).parent().find("li").length;
								var topD = $(this).offset().top;
								var leftD = $(this).offset().left;
								var bodyH = $('body').height();
								var bodyW = $('body').width();
								var dropH = optmun*37
								var dropbtnW = $(this).parent(".hover-drop").width();

								$(this).parent(".hover-drop").find(".dropdown-menu.open").css("right",bodyW - leftD - dropbtnW - 20);
								$(this).parent(".hover-drop").find(".dropdown-menu.open").css("left","auto");
								$(this).parent(".hover-drop").find(".dropdown-menu.open").css("position","fixed");
								$(this).parent(".hover-drop").find(".dropdown-menu.open").css("height",dropH);
								$(this).parent(".hover-drop").find(".dropdown-menu.open").css("width",160);
								$(this).parent(".hover-drop").find(".dropdown-menu.open").css("min-width",160);
								if(dropH > bodyH - topD - 30){
									if(dropH > topD){
										if(topD > bodyH - topD - 30){

											$(this).parent(".hover-drop").find(".dropdown-menu.open").css("top",10);
											$(this).parent(".hover-drop").find(".dropdown-menu.open").css("max-height",topD );
										}else{

											$(this).parent(".hover-drop").find(".dropdown-menu.open").css("top",topD+30)
											$(this).parent(".hover-drop").find(".dropdown-menu.open").css("max-height",bodyH - top - 40);
										}
									}else{

										$(this).parent(".hover-drop").find(".dropdown-menu.open").css("top",topD - dropH - 5);
									}
								}else{

									$(this).parent(".hover-drop").find(".dropdown-menu.open").css("top",topD + 20);
								}

							});
					        $(".hover-drop-btn").mouseout(function(){
					        	$(this).parent(".hover-drop").removeClass("open");
					        });
					    }
			        }
				}) ;
			}else if(param.localData){
				//如果只加载本地数据
				table = $.extend(table , {
					serverSide: false,
			        bServerSide : false ,
					aaData : param.localData
				}) ;
			}
			return $('#'+param.gridId).on('preInit.dt', function ( e, settings, processing ) {

		    }).off('click').on( 'click', 'tr', function(){
		    	if($(this).find("td").length==1){
		    		//如果只有一列，则取消掉选中效果(#37724点击锁定的操作列不想要选中的效果)
		    		return false ;
		    	}
		    	if(param.selectedChange != false){
		    		//如果没有明确指定，则进行点中高亮
		    		$(this).toggleClass('active');
//这一行导致服务配置管理有bug	    			$(this).parents('#'+param.gridId+"_wrapper").find('div[class="DTFC_RightBodyLiner"]').find("tr[data-dt-row='" + (this.rowIndex-1) + "']").toggleClass('active');
		    	}
		        var checkbox = $(this).find(":checkbox") ;
		        if(checkbox.length>0){
		        	checkbox = $(checkbox[0]);
		        	if(checkbox.is(":checked")){
		        		checkbox.prop('checked',false);
		        	}else{
		        		checkbox.prop('checked',"checked");
		        	}
		        }
				var radio = $(this).find(":radio") ;
				if(radio.length>0 && radio.is(":checked")){
					radio.prop('checked',false);
					$(this).removeClass('active');
				}else if(radio.length>0){
					radio.prop('checked',"checked");
					$(this).parent().find('tr').removeClass('active');
					$(this).addClass('active');
				}
		    }).on('xhr.dt', function ( e, settings, json, xhr ) {
		    	//判断是否显示列表下面的分页工具栏
	        	if(json && json.size==0){
	        		$('#'+param.gridId+"_info").hide();
	        		$('#'+param.gridId+"_paginate").hide();
	        	}else{
	        		$('#'+param.gridId+"_info").show();
	        		$('#'+param.gridId+"_paginate").show();
	        	}
		    }).DataTable(table);
		},
		/**
		 * 添加和修改的form弹窗
		 * @param setting
		 */
		formModal : function(setting){
			if(!setting.modalId){
				if(window.console){
					console.log('请传递请modal 元素 id 属性');
				}
				return ;
			}
			//通过template将form模板渲染到其容器元素(为了避免form的reset方法无效)
			if(setting.templateId){
				$("#"+setting.modalId).html(template(setting.templateId , setting.templateData));
				Util.initSysDic($("#"+setting.modalId).find("select"));//初始化字典
				Util.autocomplete($("#"+setting.modalId).find("input[autocomplete=true]"));//初始化自动填充
				Util.autocomplete($("#"+setting.modalId).find("input[automatictp=true]"));//初始化自动填充
				if(!$("#"+setting.modalId).find("select").is(":hidden")){
					$("#"+setting.modalId).find("select").selectpicker('refresh');//调用API 重新渲染
				}
			}
			//渲染表单的弹出窗
			$("#"+setting.modalId).unbind("show.bs.modal").on('show.bs.modal', function () {
				//如果窗口已经是渲染之后的则到此终止
				if(!$("#"+setting.modalId).is(":hidden")){
					return ;
				}
				//渲染之后回调
				if(typeof setting.render == "function"){
					setting.render();
				}
				if(!setting.formId){
					if(window.console){
						console.log('请传递请form 元素 id 属性');
					}
					return ;
				}
				//获取 token
				Util.getToken(function(data){
					$("#"+setting.formId).append("<input name='token' value='"+data+"' type='hidden'>");
				});
				if(!setting.NoKeyDown){
					//回车事件formId
					$("#"+setting.formId).keydown(function(e){
						 var e = e || event,
						 keycode = e.which || e.keyCode;
						 if (keycode==13) {
							 $("#"+setting.submitBtn).trigger("click");
						 }
					});
				}
				//表单提交添加记录
				$("#"+setting.submitBtn).unbind("click").click(function(){
					Util.addByForm({
						formId : setting.formId ,//表单id
						success : function(data){
							//隐藏表单弹窗
							$("#"+setting.modalId).modal('hide');
							//成功之后的回调
							if(typeof setting.submit == "function"){
								setting.submit(data);
							}
							//请求成功之后移除禁用属性
							$("#"+setting.submitBtn).removeAttr("disabled");
						} ,
						validateRules : setting.validateRules ,
						submitBtn : setting.submitBtn
					});
				});
			}).modal({backdrop: 'static', keyboard: false});
		} ,
		/**
		 * des加密
		 * @param data
		 */
		desEnc : function(data){
			return strEnc(data,'tp','des','param');
		},
		/**
		 * des解密
		 * @param data
		 */
		desDec : function(data){
			return strDec(data,'tp','des','param');
		},
		/**
		 * 初始化性别字典下拉框
		 * 如果 $select 不为空，则只初始化当前这个下拉框
		 */
		initSysDic : function($select){
			$($select||$("select")).each(function(i , o){
				//如果是隐藏的则直接返回
				if($(this).is("hidden")){
					return ;
				} else if($(this).attr("vtype")=='def'){
					//自定义的下拉列表标记，无需公共方法进行select组件的初始化过程
					return ;
				}
				var code = $(this).attr("code");
				//如果是没有code则直接返回
				if(!code){
					return ;
				}
				var value = $(this).attr("value");
				if($(o).children().length==0){

					var defalutContent = $(this).attr("defalutContent");
					var multiple = $(this).attr("multiple");
					if(!multiple) {
						if(Util.isNotEmpty(defalutContent)) {
							$(o).append("<option value=''>"+defalutContent+"</option>");
						}else{
							$(o).append("<option value=''>"+tp_common_choose+"</option>");//请选择
						}
					}

					//如果页面上没有缓存
					if(!tp.dic.data[code]){
						$.ajax({
							url : contextpath+"/sys/uacm/dicm/dic"  ,
							async : false ,
							type : "POST",
							data : {
								code : code
							},
							success : function(ret_dic){
								tp.dic.data[code] = ret_dic ;
								$.each(ret_dic , function(ii,oo){
									if(value == oo.CODEVALUE){
										$(o).append("<option value='"+oo.CODEVALUE+"' selected='selected'  >"+tp.dic.language.get(oo.CODENAME)+"</option>");
									}else{
										$(o).append("<option value='"+oo.CODEVALUE+"'>"+tp.dic.language.get(oo.CODENAME)+"</option>");
									}
								});
								//如果下拉框改变，则去掉默认值
								$(o).change(function(){
									$(o).removeAttr("value");
								})
								$(o).selectpicker("refresh");
							},
							error : function(){
			                    if(window.console){
			    					console.log("获取"+code+"字典表失败");
			    				}
							}
						});
					}else{
						$.each(tp.dic.data[code] , function(ii,oo){
							if(value == oo.CODEVALUE){
								$(o).append("<option value='"+oo.CODEVALUE+"' selected='selected'  >"+tp.dic.language.get(oo.CODENAME)+"</option>");
							}else{
								$(o).append("<option value='"+oo.CODEVALUE+"'>"+tp.dic.language.get(oo.CODENAME)+"</option>");
							}
						});
						//如果下拉框改变，则去掉默认值
						$(o).change(function(){
							$(o).removeAttr("value");
						})
						$(o).selectpicker("refresh");
					}
				}
			});
		},
		/**
		 * 将性别key转化为value
		 * @param key
		 */
		convertSysDic : function(dic , key){
			var value = "";
			//如果缓存中不存在这个字典表
			if(!tp.dic.data[dic]){
				$.ajax({
					url : contextpath+"/sys/uacm/dicm/dic"  ,
					async : false ,
					type : "POST",
					data : {
						code : dic
					},
					success : function(ret_dic){
						tp.dic.data[dic] = ret_dic ;
					},
					error : function(){
						if(window.console) console.log("获取"+dic+"字典表失败");
					}
				});
			}
			$(tp.dic.data[dic]).each(function(i,o){
				if(o.CODEVALUE==key){
					value = tp.dic.language.get(o.CODENAME) ;
				}
			});
			return value ;
		},
		/**
		 * 根据逗号分割，将key转化为value
		 * @param key
		 */
		convertSysDicSplitByComma : function(dic , key){
			var value = "";
			$(tp.dic.data[dic]).each(function(i,o){
				var keys = key.split(",");
				for(j=0;j<keys.length;j++){
					if(o.CODEVALUE==keys[j]){
						if(value ==""){
							value = tp.dic.language.get(oo.CODENAME);
						}else{
							value = value+","+tp.dic.language.get(o.CODENAME) ;
						}
					}
				}
			});
			return value ;
		},
		/**
		 * 页面Tab切换(pt:页面TAB展示；ptc页面TAB内容;lp页数；type 类型)
		 * 向浏览器中放入Hash值
		 */
		setHash : function(hash){
			//判断hash中是否有go的跳转
			var act = this.getHash(location.hash,'act') ;
			//如果传进来的hash中没有跳转地址，则默认加上URL地址上默认的
			if(hash.indexOf("act=")==-1 && act){
				hash += "&act="+ act;
			}
			window.location.hash = hash;
		},
		/**
		 * 替换指定hash值
		 */
		replaceHash : function(paramName, paramValue){
			var hash = window.location.hash;
			for(var i=0; i<arguments.length; i+=2){
				paramName = arguments[i];
				paramValue = arguments[i+1];
				var p = hash.match(new RegExp(paramName + "=([^\&]*)", "i"));
				if(p != null){
					hash = hash.replace(p[0], paramName + "=" + paramValue);
				}
				else {
					var s = paramName + "=" + paramValue;
					if(hash.length > 0){
						hash += "&" + s;
					} else {
						hash += s;
					}
				}
			}

			window.location.hash = hash;
		},
		/**
		 * 截取参数方法，hash：截取的字符串，name：截取的参数名，nvl：该参数不存在时的返回值
		 */
//		getHash : function(hash,name,nvl){
//			if(!nvl){
//				nvl = "";
//			}
//			var svalue = hash.match(new RegExp("[\?\&]?" + name + "=([^\&\#]*)(\&?)", "i"));
//			if(svalue == null){
//				return nvl;
//			}else{
//				svalue = svalue ? svalue[1] : svalue;
//				svalue = svalue.replace(/<script>/gi,"").replace(/<\/script>/gi,"").replace(/<html>/gi,"").replace(/<\/html>/gi,"").replace(/alert/gi,"").replace(/<span>/gi,"").replace(/<\/span>/gi,"").replace(/<div>/gi,"").replace(/<\/div>/gi,"");
//				return decodeURIComponent(svalue);
//			}
//		},
		getHash : function(hash,name,nvl){
			if(!nvl){
				nvl = "";
			}
			var svalue=null;
			var val=(hash+"").split("#")[1];
			var arr=(val+"").split("&");
			$.each(arr, function(){
				var equalsindex = (this+"").indexOf("=");
				var ky=(this+"").substring(0,equalsindex);
				if(ky==name){
					svalue=(this+"").substring(equalsindex+1);
				}
			});
			if(svalue == null){
				return nvl;
			}else{
				try{
					return decodeURIComponent(svalue);
				}catch(e){
					return svalue ;
				}
			}
		},
		/**
		 * 判断对象是否为空
		 *
		 * @param {Object}
		 *            v
		 * @return {Boolean} 不为空返回true，否则返回false。
		 */
		isNotEmpty : function(v){
			if(typeof (v)=="object"){
				if($.isEmptyObject(v)){
					return false;
				}else{
					return true;
				}
			}else{
				if (v == null || typeof (v) == 'undefined' || v == "" || v == "unknown") {
					return false;
				} else {
					return true;
				}
			}
		} ,
		/**
		 * 空对象转换
		 *
		 * @param {Object}
		 *            v
		 * @return {String} 不为空返回本身，否则返回"无"。
		 */
		nvlToStr : function(v){
			if (v == null || typeof (v) == 'undefined' || v == "" || v == "unknown") {
				return "无";
			} else {
				return v;
			}
		} ,
		/**
		 * 空对象转换
		 *
		 * @param {Object}
		 *            v
		 * @return {String} 不为空返回本身，否则返回""。
		 */
		nvlToNull : function(v){
			if (v == null || typeof (v) == 'undefined'|| v == "undefined" || v == "" || v == "unknown") {
				return "";
			} else {
				return v;
			}
		} ,
		/**
		 *
		 * @param str 字符串
		 * @param num	保留长度
		 * @returns
		 */
		subStr : function(str , length){
			if(str && str.length>length){
				return str.substring(0,length)+"...";
			}
			return str ;
		} ,
		autocomplete : function(_this , config){
			$(_this||$("input[autocomplete=true]")||$("input[automatictp=true]")).each(function(i,o){
				$(o).autocomplete($.extend({
					items : $(o).attr("items") || 20 ,
			        source:function(query,process){
			        	var name = $(o).attr("name") ;
			        	var mapping = $(o).attr("mapping") ;
			        	var sql = $(o).attr("sql") ;
			        	var param = {} ;
			        	param[name] = query ;
			        	param['mapping'] = mapping ;
			        	if(sql){
			        		param['sql'] = sql ;
			        	}
			        	Util.ajax({
			        		param : param ,
			        		url : $(o).attr("action") ,
			        		success : function(data){
			        			Util.changeAutocompletePosition(o);
			        			//重新发送请求之后清空value值
					        	$("input[name='"+name+"']").change(function(){
					        		$("input[name='"+name+"_code']").val('');
					        	});
			        			return process(data);
			        		}
			        	});
			        },
			        formatItem:function(item){
			        	var mapping = $(o).attr("mapping") ;
			        	var hidecode = $(o).attr("hidecode") ;
			        	if(mapping == "getUserForAutocomplete") {
			        		return item["VALUE"]+" - ("+Util.convertSysDic("DICT_COMM_GENDER" , item["USER_SEX"])+","+item["UNIT_NAME"]+")";
			        	}else if(hidecode==true || hidecode=="true"){
			        		return item["VALUE"] ;
			        	}else{
			        		return item["VALUE"]+" - "+item["CODE"];
			        	}
			        },
			        setValue:function(item){
			        	var mapping = $(o).attr("mapping") ;
			        	var reg=new RegExp("^getUumUnitNameList");
			        	var reg2=new RegExp("^getUgmUnitNameList");
			        	if((reg.test(mapping)||reg2.test(mapping))&&item["TYPE"]=="1"){
			        		return {'data-value':item["VALUE2"]+"-"+item["VALUE"],'real-value':item["UNIONCODE"]};
			        	}else{
			        		return {'data-value':item["VALUE"],'real-value':item["CODE"]};
			        	}
			        }
			    },config));
			});
		},
		changeAutocompletePosition : function(o){
			var ondiv_flag = 0;
			$(o).parent().mouseover(function(){
				ondiv_flag = 1;
			});
			$(o).parent().mouseout(function(){
				ondiv_flag = 0;
			})
			var X = Math.ceil($(o).offset().top+$(o).height());
			var Y = Math.ceil($(o).offset().left);
			var bodyH = $('body').height();
			var tH = X-20;
			var bH = bodyH-X-50;
			var auto_ul;
			setTimeout(function(){
				auto_ul = $(o).parent().find("ul");
				if(auto_ul.length > 0){
					var optmun = $(o).parent().find("li");
					var dropdownH = optmun.length*37+3;
					if(dropdownH < bH){
						if(bH<160){

							auto_ul.css("max-height",tH);
							auto_ul.css("min-height",37);
							auto_ul.css("top",X - dropdownH -40);
						}else{
							auto_ul.css("max-height",bH);
							auto_ul.css("min-height",37);
							auto_ul.css("top",X + 5);
						}
					}else{
						if(dropdownH < tH){
							auto_ul.css("max-height",tH);
							auto_ul.css("min-height",37);
							auto_ul.css("top",X - dropdownH -40);
						}else{
							if(bH>tH){
								auto_ul.css("max-height",bH);
								auto_ul.css("min-height",37);
								auto_ul.css("top",X + 25);

							}else{
								auto_ul.css("max-height",tH);
								auto_ul.css("min-height",37);
								auto_ul.css("top",X - tH -10);
							}
						}
					}
					auto_ul.animate({scrollTop:0},0);
					auto_ul.css("height",dropdownH);
					auto_ul.css("left",Y+"px");
					auto_ul.css("min-width",$(o).outerWidth());
					auto_ul.css("width",$(o).outerWidth());
					auto_ul.css("position","fixed");
				}
				if(document.addEventListener){
					document.addEventListener('DOMMouseScroll',function(e){
						 var direct=0;
						      e=e || window.event;
						      if(e.wheelDelta){//IE/Opera/Chrome
						    	  direct=e.wheelDelta;
						      }else if(e.detail){//Firefox
						    	  direct=e.detail;
						      }
						      if(typeof(auto_ul) != "undefined" && auto_ul.length>0){
						    	  var scrollheight = auto_ul[0].scrollHeight-auto_ul[0].scrollTop-auto_ul[0].clientHeight;
							      if(ondiv_flag == 0 && direct != 0){
							    	 $(o).parent().find("ul").css("display","none");
							      }else if(auto_ul.scrollTop()==0 && direct < 0 && ondiv_flag == 1){
							    	  e.preventDefault();
							      }else if(scrollheight == 0 && direct > 0 && ondiv_flag == 1){
							    	  e.preventDefault();
							      }
						      }
					},false);
				}
				window.onmousewheel=document.onmousewheel=function(e){
					 var direct=0;
				      e=e || window.event;
				      if(e.wheelDelta){//IE/Opera/Chrome
				    	  direct=e.wheelDelta;
				      }else if(e.detail){//Firefox
				    	  direct=e.detail;
				      }
				      if(typeof(auto_ul) != "undefined"){
				    	  var scrollheight = auto_ul[0].scrollHeight-auto_ul[0].scrollTop-auto_ul[0].clientHeight;
					      if(ondiv_flag == 0 && direct != 0){
					    	 $(o).parent().find("ul").css("display","none");
					      }
					      //注释byliumiao，好像没啥用，而且导致前台报错
//					      else if(auto_ul.scrollTop()==0 && direct > 0 && ondiv_flag == 1){
//					    	  e.preventDefault();
//					      }else if(scrollheight == 0 && direct < 0 && ondiv_flag == 1){
//					    	  e.preventDefault();
//					      }
				      }
			};//IE/Opera/Chrome
			}, 10);
			$(o).unbind("keydown").keydown(function () {
				$(this).parent().find("ul").css("display","none");
				auto_ul.css("position","absolute");
			});
		},
		summernote : function(config){
			$.ajax({
			  url: 'https://api.github.com/emojis'
			}).then(function(data) {
			  window.emojis = Object.keys(data);
			  window.emojiUrls = data;
			});

			if(!config.id){
				if(window.console){
					console.log('请传递 summernote id 属性');
				}
				return ;
			}
			$("#"+config.id).summernote($.extend({
				lang: 'zh-CN',
				height: 300 ,
				callbacks: {
		            /*onImageUpload: function(files) {
		            	data = new FormData();
		                data.append("file", files[0]);
		                $.ajax({
		                    data: data,
		                    type: "POST",
		                    url: contextpath + '/upload/'+config.module||summernote,
		                    cache: false,
		                    contentType: false,
		                    processData: false,
		                    success: function(data) {
		                    	$("#"+config.id).summernote('insertImage', contextpath + "/" + data.path, 'image name');
		                    }
		                });
		            }*/
		        },
		        fontNames : ["Arial", "Arial Black", "Comic Sans MS",
		 					"Courier New", "Helvetica Neue", "Helvetica", "Impact",
		 					"Lucida Grande", "Tahoma", "Times New Roman", "Verdana","微软雅黑","黑体","宋体","仿宋","楷体"],
		        hint: {
		            match: /:([\-+\w]+)$/,
		            search: function (keyword, callback) {
		              callback($.grep(emojis, function (item) {
		                return item.indexOf(keyword)  === 0;
		              }));
		            },
		            template: function (item) {
		              var content = emojiUrls[item];
		              return '<img src="' + content + '" width="20" /> :' + item + ':';
		            },
		            content: function (item) {
		              var url = emojiUrls[item];
		              if (url) {
		                return $('<img />').attr('src', url).css('width', 20)[0];
		              }
		              return '';
		            }
		        }
			},config));
		},
		tree : function(settings , data){
			if(!settings.treeId){
				if(window.console){
					console.log('请传递 tree Id');
				}
				return ;
			}

			var enable_edit = settings.allowEdit != undefined ? settings.allowEdit : true ;

			var setting = {
					async: {
						enable: !data,
						autoParam: settings.autoParam || ["id"],
						url: settings.url
					},
					check: {
						enable: true
					},
					edit: {
						enable: enable_edit ,
						renameTitle: "重命名" ,
						removeTitle: "删除节点"
					},
					data: {
						simpleData: {
							enable: data ,
							idKey: settings.idKey || "id",
							pIdKey: settings.pIdKey || "pId"
						},
						key: {
							name: settings.name || "name"
						}
					},
					view: {
						addHoverDom: function addHoverDom(treeId, treeNode) {
							if(enable_edit){
								var sObj = $("#" + treeNode.tId + "_span");
								if (treeNode.editNameFlag || $("#addBtn_"+treeNode.tId).length>0) return;
								var addStr = "<span class='button add' id='addBtn_" + treeNode.tId
									+ "' title='添加节点' onfocus='this.blur();'></span>";
								sObj.after(addStr);
								var btn = $("#addBtn_"+treeNode.tId);
								if (btn) btn.bind("click", function(){
									if(settings.add && typeof settings.add=='function' ){
										settings.add(treeId, treeNode);
									}else{
										if(window.console){
											console.log('尚未传递添加的回调方法');
										}
									}
								});
							}
						},
						removeHoverDom: function removeHoverDom(treeId, treeNode) {
							if(enable_edit)
								$("#addBtn_"+treeNode.tId).unbind().remove();
						}
					},
					callback: {
						beforeRemove:	function (treeId, treeNode) {
							Msg.confirm("确认删除该节点。",function(){
								if(settings.remove && typeof settings.remove=='function' ){
									//如果回调方法返回值为true，则删除节点
									if(settings.remove(treeId, treeNode)){
										$.fn.zTree.getZTreeObj(treeId).selectNode(treeNode);
									}
								}else{
									if(window.console){
										console.log('尚未传递删除的回调方法');
									}
									return false;
								}
							});
							return false ;
						}	,
						beforeRename: function (treeId, treeNode, newName) {
							if (newName.length == 0) {
								Msg.warning("节点名称不能为空。");
								return false;
							}
							if(settings.rename && typeof settings.rename=='function' ){
								return settings.rename(treeId, treeNode, newName) ;
							}else{
								if(window.console){
									console.log('尚未传递修改名称的回调方法');
								}
								return true ;
							}
						},
						onCheck : function(event, treeId, treeNode){
							$.fn.zTree.getZTreeObj(treeId).selectNode(treeNode);
							if(settings.checked && typeof settings.checked=='function' ){
								return settings.checked(event, treeId, treeNode) ;
							}
						},
						onClick: function(event, treeId, treeNode){
							if(!treeNode.checked){
								$.fn.zTree.getZTreeObj(treeId).checkNode(treeNode);
							}
							if(settings.click && typeof settings.click=='function' ){
								return settings.click(event, treeId, treeNode) ;
							}
						}
					}
				}
				if(data){
					return $.fn.zTree.init($("#"+settings.treeId), $.extend(setting,settings) , data);
				}
				return $.fn.zTree.init($("#"+settings.treeId), $.extend(setting,settings));
		},
		setCookie : function setCookie(name,value,expiredays) {
			var exdate=new Date()
			exdate.setDate(exdate.getDate() + expiredays)
			document.cookie = name+ "=" +escape(value) + ((expiredays==null) ? "" : ";expires="+exdate.toGMTString())
		} ,
		getCookie : function getCookie(name) {
			if (document.cookie.length>0) {
			  c_start=document.cookie.indexOf(name + "=")
			  if (c_start!=-1) {
			    c_start=c_start + name.length+1
			    c_end=document.cookie.indexOf(";",c_start)
			    if (c_end==-1) c_end=document.cookie.length
			    return unescape(document.cookie.substring(c_start,c_end))
			    }
			  }
			return ""
		},
		checkServiceLimit:function(serviceID){
			var result = true;
			Util.ajax({url:contextpath +"/fp/serveapply/checkLimit",dataType : "text",async:false,param:{serviceID:serviceID},method:"POST",success:function(data){
				if(data!=="OK"){//达到申请上限，不允许申请
					layer.msg("服务申请已达上限，不可再次申请！", {
						time: 2000 //2s后自动关闭
					});
					result = false;
				}
			}});
			return result;
		},
		//校验服务是否已经审核完成
		checkServiceOver:function(serviceID){
			var result = true;
			Util.ajax({url:contextpath +"/fp/serveapply/checkOver",dataType : "text",async:false,param:{serviceID:serviceID},method:"POST",success:function(data){
				if(data!=="OK"){//达到申请上限，不允许申请
					layer.msg("上一月填报还没有填报或没有审核完成，需要先填报上一次申请！", {
					time: 2000 //2s后自动关闭
					});
					result = false;
				}
			}});
			return result;
		},
		//Tab的滑动功能
		swiperTab:function(){
			var swiper = new Swiper('.swiper-container', {
			    pagination: null,
			    slidesPerView: 'auto',
			    paginationClickable: true,
			    spaceBetween: 0,
			    freeMode: true,
			    resistanceRatio: 0.5,
			    observer : true ,
			    observerParents : true
			});
		},
		//Tab的滑动功能
		/*Btn的滑动功能
		swiperBtn:function(){
			var swiper = new Swiper('.swiper-container-btn', {
			    pagination: '.swiper-pagination',
			    slidesPerView: 'auto',
			    paginationClickable: true,
			    spaceBetween: 0,
			    freeMode: true,
			    resistanceRatio: 0.5

			});
		}
		//Btn的滑动功能*/
		//Btn的滑动功能-ren.jq-START
		swiperBtn:function(){
			var swiper = new Swiper('.swiper-container-btn',{
			    slidesPerView: 'auto',
			    paginationClickable: true,
			    spaceBetween: 0,
			    freeMode: true,
			    resistanceRatio: 0.5
//			    on: {
//			    	 resize: function(){
//			    		 setTimeout("swiper.update()", 1000)
//
//				        }
//			      }
			});

			//滑动功能提示框-ren.jq-START
			$("<div class='swiper-note' style='z-index: 999;'>" +
					"<span class='fa fa-hand-o-up'></span>按钮是可以滑动的哦<button type='button' class='close' data-dismiss='alert'><span aria-hidden='true'>×</span><span class='sr-only'>Close</span></button>" +
					"</div>").appendTo(".swiper-btngroup:first-child");
				function swipernote(){
						$(".swiper-btngroup").each(function(){
							var w = 0;
							var d = $(this).find(".link_btn").length;
							$(this).find(".link_btn").each(function(){
								w += parseInt($(this).width());
							})
							var p= $(this).width();
							if((w+d*30) > p){
								$(this).find(".swiper-note").addClass("active");
								$(this).find(".swiper-container-btn").width("98%");
								$(this).find(".close").on('click',function(){
									$(this).parents('.swiper-note').removeClass("active");
								});
							}else{
								$(this).find(".swiper-container-btn").width("auto");
							}
						})
						var t = setTimeout('$(".swiper-note").removeClass("active")',11000);
					};
				swipernote();
//				$(window).resize(function(){
//						swipernote();
//						//swiper.update();
//				});
			//滑动功能提示框-ren.jq-END

		},
		//Btn的滑动功能-ren.jq-END
		slFoldable:function(){
			//ren.jq-判断多维度分类何时一行显示不下所有分类需要折叠与展开
				$(".select-line-foldable .fold-btn").unbind("click").on("click",function(e){
					$(this).closest(".select-line-foldable").toggleClass("active");
					if($(this).closest(".select-line-foldable").hasClass("active")){
						$(this).removeClass("fa fa-caret-down");
						$(this).addClass("fa fa-caret-up");
			        }else{
			        	$(this).removeClass("fa fa-caret-up");
			        	$(this).addClass("fa fa-caret-down");
			        }
			    });
				var selectfoldable = function(a){
					$(".select-line-foldable").each(function(){
						var d = $(this).find("span").length
						var b = $(this).find("a").length
						var p = $(this).children("div").width();
						var w = 0
						$(this).children("div").find("a").each(function(){
							w += parseInt($(this).width());
						})
						if((w +  11 * d + 12 * b) < p){
							$(this).children(".fold-btn").hide();

						}else{
							$(this).children(".fold-btn").show();
						}
					 });
				};
				selectfoldable();
				$(window).resize(function(){
					selectfoldable();
		        });
			}
			//ren.jq
		//Btn的滑动功能-ren.jq-END
		/**
		 * 裁剪图片
		 * @param cb 回调函数
		 * @param module 模块的名字
		 * @param type 1：压缩；2：裁剪
		 * @param path 图片路径
		 * @param width	宽度
		 * @param height	高度
		 * @param x	X轴
		 * @param y	Y轴
		 */
		,crop : function(cb , module , type , path , width , height , x , y , rotate){
			$.post(contextpath+"/crop/"+module , {
				type : type||1,
				path : path ,
				width : width ,
				height : height ,
				x : x||0 ,
				y : y||0 ,
				rotate : rotate||0
			} , function(data){
				if(typeof cb == 'function'){
					cb(data);
				}
			});
		} ,
		//IP转成整型
		ip2int : function(ip){
		    var num = 0;
		    ip = ip.split(".");
		    num = Number(ip[0]) * 256 * 256 * 256 + Number(ip[1]) * 256 * 256 + Number(ip[2]) * 256 + Number(ip[3]);
		    num = num >>> 0;
		    return num;
		}  ,
		//整型解析为IP地址
		int2iP : function(num){
			//如果是IPv6
			if((num+'').indexOf(':')!=-1 || (num+'').indexOf('.')!=-1){
				return num ;
			}
		    var str;
		    var tt = new Array();
		    tt[0] = (num >>> 24) >>> 0;
		    tt[1] = ((num << 8) >>> 24) >>> 0;
		    tt[2] = (num << 16) >>> 24;
		    tt[3] = (num << 24) >>> 24;
		    str = String(tt[0]) + "." + String(tt[1]) + "." + String(tt[2]) + "." + String(tt[3]);
		    return str;
		} ,
		isIE : function(){
			if (!!window.ActiveXObject || "ActiveXObject" in window)
				  return true;
			else
				  return false;
		},
		getChkColumn : function(){
			if(Util.isIE()){
				return "<input onclick='this.checked = !this.checked' ondblclick='this.checked = !this.checked' type='checkbox'>";;
			}else{
				return "<input onclick='this.checked = !this.checked' type='checkbox'>";;
			}
		},
		//解码html
		htmlDecode : function(value){
			if(value==null||value=="") {
				return "";
			}
		  return $('<div/>').html(value).text();
		},
		htmlEncode : function(str) {
			if(str==null||str=="") {
				return "";
			}
		    return $('<div/>').text(str).html();
		},
		removeHtmlTab:function (tab) {
			if(tab==null){
				return "";
			}else{
				return tab.replace(/<[^<>]+?>/g,'');//删除所有HTML标签
			}
		},
		//读取json数据
		getJsonContent:function(url,callback,error){
			$.ajax({
		        type: "get",
		        async: true,
		        url: contextpath +"/"+ url ,
		        dataType: "jsonp",
		        jsonp: "callback",//传递给请求处理程序或页面的，用以获得jsonp回调函数名的参数名(一般默认为:callback)
		        jsonpCallback:"jsonp_"+url.substring(url.lastIndexOf('/')+1,url.indexOf('.json')),//自定义的jsonp回调函数名称，默认为jQuery自动生成的随机函数名，也可以写"?"，jQuery会自动为你处理数据
		        success: function(json){
		        	if(typeof(callback) == "function"){
		        		callback(json.result);
		        	}
		        },
		        error: function(){
		        	Msg.error("未查询到相关内容，请联系管理员");
		        	if(typeof(error) == "function"){
		        		error();
		        	}
		        }
			});
		},
		//返回跳转页面
		moduleJumpCcancle:function(){
			var cpparams = Util.getHash(location.hash, "cpparams", "");
			if(cpparams==""){
				Util.setHash("#p=");
			}else{
				cpparams = template.BASE64.decode(cpparams);
				cpparams =  JSON.parse(cpparams);
				var parentp = Util.getHash(cpparams.parenthash, "p", "");
				//因为是内部跳转act没有改变
				var act = Util.getHash(location.hash, "act", "");
				var gobackact = cpparams.gobackact;
				if(!Util.isNotEmpty(gobackact)){
					gobackact = act;
				}
				Util.run = null ;
				$(window).unbind("hashchange");
				//parentp如果为空，说明父页面是列表页面，在跳转后setHash，如果不为空，说明父页面是表单页面，在load中setHash
				$("#page-content").load(gobackact,function(){
					//返回表单
					if(gobackact.indexOf("cp/templateList/p")<0||(gobackact.indexOf("cp/templateList/p")>-1&&(Util.isNotEmpty(parentp)))){
						if(Util.run && typeof Util.run == 'function')Util.run('form');
						Util.setHash(cpparams.parenthash);
						//如果存在配置平台配置按钮删除
						if($(".fm-ul").length>0){
							$(".fm-ul").remove();
						}
					}else{
						//返回列表
						if(Util.run && typeof Util.run == 'function')Util.run();
					}
				});
				//返回列表
				if(gobackact.indexOf("cp/templateList/p")>-1&&!Util.isNotEmpty(parentp)){
					Util.setHash(cpparams.parenthash);
				}
			}
		},
		isChinese : function(str) {
			var reg = /^[A-Za-z0-9_-]+$/;
			return !reg.test(str) ;
		},
		//获取当前客户端信息
		getClientInfo : function(){
			var userAgentInfo = navigator.userAgent;
			   var Agents = new Array("Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod");
			   var agentinfo = null;
			   for (var i = 0; i < Agents.length; i++) {
			       if (userAgentInfo.indexOf(Agents[i]) > 0) { agentinfo = userAgentInfo; break; }
			   }
			   if(agentinfo){
			        return agentinfo;
			   }else{
			        return "PC";
			   }
		},
		//小程序下载附件
		downloadFile : function(wholeUrl,name,url){
            if(isMiniprogram){
                Util.ajax({url:contextpath +"/getDownloadFilePath",async:false,param:{filename:name,filepath:url},method:"POST",success:function(data){
                    if(data.errorStatus=="0"){
                        var urlEncode =encodeURIComponent(data.srcUrl);
                        wx.miniProgram.navigateTo({
                            url:'/pages/webviewDownload/webviewDownload?url=' + urlEncode + '&fileName=' + name
                        })
                    }else{
                        Msg.warning("请求异常！错误信息："+data.errorMsg);
                    }
                }
                })
            }else{
                window.open(wholeUrl);
            }
        }
}

/**
* 自定义方法被artTemplate引用，对日期格式化
*/
template.helper('dateFormat', function (date, format) {
	if(!date){
		return ;
	}
    date = new Date(date);
    var map = {
        "M": date.getMonth() + 1, //月份
        "d": date.getDate(), //日
        "h": date.getHours(), //小时
        "m": date.getMinutes(), //分
        "s": date.getSeconds(), //秒
        "q": Math.floor((date.getMonth() + 3) / 3), //季度
        "S": date.getMilliseconds() //毫秒
    };
    format = format.replace(/([yMdhmsqS])+/g, function(all, t){
        var v = map[t];
        if(v !== undefined){
            if(all.length > 1){
                v = '0' + v;
                v = v.substr(v.length-2);
            }
            return v;
        }
        else if(t === 'y'){
            return (date.getFullYear() + '').substr(4 - all.length);
        }
        return all;
    });
    return format;
});

/**
 * 字典转换
 */
template.helper('convertSysDic', function (dic , data) {
	if(!data || !dic) return ;
    return Util.convertSysDic(dic , data);
});
/**
 * 字典转换根据逗号
 */
template.helper('convertSysDicSplitByComma', function (dic , data) {
	if(!data || !dic) return ;
    return Util.convertSysDicSplitByComma(dic , data);
});
/**
 * IP转换
 */
template.helper('int2iP', function (data) {
    return Util.int2iP(data);
});

/**
 * 截取字符串
 */
template.helper('subStr', function (str , length) {
    return Util.subStr(str , length);
});

var Msg = {
		/**
		 * 操作成功提示
		 * @param m
		 */
		success : function(m){
			layer.msg(Util.htmlEncode(m)||tp_common_success, {
			  icon: 1,
			  time: 2000 //2s后自动关闭
			});
		},
		/**
		 * 操作失败提示
		 * @param m
		 */
		error : function(m){
			layer.msg(Util.htmlEncode(m)||tp_common_fail, {
			  icon: 11,
			  time: 2000 //2s后自动关闭
			});
		},
		/**
		 * 警示
		 * @param m
		 */
		warning : function(m,callback,callback1){
//			layer.alert(m, {
//			  title: '系统提示',
//			  icon: 0
//			},function(index){
//				layer.close(index);
//				if(typeof callback == "function"){
//					callback();
//				}
//			});
			var layerObj = layer.confirm(Util.htmlEncode(m), {
		         title: tp_common_warning,
		         btn: [tp_common_confirm,tp_common_cancel],
		         resize: false
		    }, function(){
			      layer.close(layerObj);
			     if(typeof callback == "function"){
			      callback();
			     }
		    }, function(){
			     layer.close(layerObj);
			     if(typeof callback1 == "function"){
			      callback1();
			     }
		    });
		},
		/**
		 * 提示
		 * @param m
		 */
		info : function(m,callback,callback1){
//			layer.alert(m, {
//			  title: '系统提示',
//			  icon: 5
//			});
			var layerObj = layer.confirm(Util.htmlEncode(m), {
		         title: tp_common_warning,
		         btn: [tp_common_confirm,tp_common_cancel],
		         resize: false
		    }, function(){
			      layer.close(layerObj);
			     if(typeof callback == "function"){
			      callback();
			     }
		    }, function(){
			     layer.close(layerObj);
			     if(typeof callback1 == "function"){
			      callback1();
			     }
		    });
		},
		/**
		 * 确认
		 * @param m
		 */
		confirm : function(m,callback,callback1){
			   var layerObj = layer.confirm(Util.htmlEncode(m), {
			         title: tp_common_warning,
			         btn: [tp_common_confirm,tp_common_cancel],
			         resize: false
			    }, function(){
			      layer.close(layerObj);
			     if(typeof callback == "function"){
			      callback();
			     }
			    }, function(){
			     layer.close(layerObj);
			     if(typeof callback1 == "function"){
			      callback1();
			     }
			    });
		},
		prompt : function(param){
			var obj = $.extend({
				  formType: 2,
				  title: tp_common_warning,
				  resize: false
				} , param);
			var index = layer.prompt(obj, function(value, index, elem){
				if($.isFunction(param.callback)){
					param.callback(value, index, elem);
				}
			  layer.close(index);
			});
		} ,
		/**
		 * 加载
		 * @param m
		 */
		load : function(config){
			//如果加载层存在则不需要再次创建
			if($("div[type='loading']").length==0){
				return layer.load(1, $.extend({
					time : 60000,//60秒后默认关闭
					shade: [0.1,'#000'], //0.1透明度的白色背景
					resize: false,
					content: '<div class="exam-loader-centerbox"><div class="loader"><div class="loader-inner line-scale"><div></div><div></div><div></div><div></div><div></div></div></div><div class="exam-loader-text">'+tp_common_loading+'</div></div>'
				},config));
			}
		},
		/**
		 * 关闭
		 * 传入的obj为空时关闭所有层，
		 * 传入的obj='dialog' 关闭信息框
		 * 传入的obj='page' 关闭所有页面层
		 * 传入的obj='iframe' 关闭所有的iframe层
		 * 传入的obj='loading' 关闭加载层
		 * 传入的obj='tips' 关闭所有的tips层
		 * @param m
		 */
		close : function(obj){
			if(Util.isNotEmpty(obj)){
				layer.close(obj);
			} else {
				layer.closeAll();
			}
		},
		/**
		 * 弹出显示页面层
		 * @param setting
		 */
		open : function(setting){
			if(!setting.title){//title不设置默认不显示title
				setting.title = false;
			}
			//通过template将html模板渲染到其容器元素
			if(setting.templateId){
//				if(!setting.contentId){
//					if(window.console){
//						console.log('请传递 contentId属性');
//					}
//					return;
//				}
				var containerId = setting.contentId;
				if(setting.containerId){
					containerId = setting.containerId;
				}
				$("#"+containerId).html(template(setting.templateId , {'data':setting.templateData}));
			}
			layer.open($.extend({
				  type : 1,
				  anim: -1,
				  area: setting.area, //宽高['500px', '300px']
				  skin : 'layui-layer-rim', //加上边框
				  title : setting.title, //可以传普通的字符串，如果你不想显示标题栏传false
				  resize: false,
				  content: $("#"+setting.contentId),
				  end:function(){
					  if(setting.contentId){
						  $("#"+setting.contentId).hide();
					  }else{
						  $(setting.content).hide();
					  }
				  },
				},setting));
		} ,
		reloadPage : function(){
			//提示框只弹出一次
			if($("#sessionTimeut_reloadPage").length!=0) return ;
			//如果浏览器窗口宽小于弹窗的宽，则直接刷新，不做提示
			if($(window).width()<700){
				location.reload();
				return;
			}
			//如果有 abort 的请求进入到这里，则再次重试3遍，如果依旧 abort 则任务session丢了
			var sessionTimeout = 0 ;
			for(var i=0 ; i<3; i++){
				$.ajax({
					url : contextpath + "/ping" ,
					async : false ,
					complete: function( xhr ){
						if(xhr.status == '0' && xhr.statusText && xhr.statusText.toLowerCase().indexOf('error')!=-1){
				        	++sessionTimeout ;
						}
			       }
				});
			}
			if(sessionTimeout != 3){
				return ;
			}

			var dialog = '<div  class="pull-left">' +
			'			<div class="modal-dialog modal-lg push-up-0 push-down-0 push-left-0 push-right-0" style="max-width:570px;">' +
			'		<div class="modal-content modal-content-noborder">' +
			'			<div class="modal-header">' +
//			'				<button id="uam_pop_close" type="button" class="close" data-dismiss="modal">' +
//			'					<span aria-hidden="true">×</span><span class="sr-only">Close</span>' +
//			'				</button>' +
			'				<h4 class="modal-title">登录状态过期</h4>' +
			'			</div>' +
			'			<div class="modal-body">' +
			'				<div class="prompt-contant push-up-0">' +
			'					<div class="prompt-img">' +
			'						<img src="'+contextpath+'/resource/image/common/refresh_prompt.png" alt="" class="bar">' +
			'					</div>' +
			'					<div class="prompt-text">' +
			'						<p class="prompt-text-title">登录状态过期</p>' +
			'						<p class="prompt-text-info">您的登录状态可能已经过期，点击确定立即刷新当前页面，<span id="alert_time_out_second_span" style="color:red;">30</span>秒后自动刷新。</p>' +
			'					</div>' +
			'					<div class="clear"></div>' +
			'				</div>' +
			'			</div>' +
			'			<div class="modal-footer">' +
			'				<button type="button" id="sessionTimeut_reloadPage" class="btn btn-primary pull-right" style="background-color:#263339;border-color:#263339;">确定</button>' +
			'			</div>' +
			'		</div>' +
			'	</div>' +
			'</div>';
			layer.open({
				  type: 1,
				  shade: false,
				  closeBtn : 0 ,
				  resize: false,
				  area: '580px' ,
				  title: false, //不显示标题
				  content: dialog ,
				  success: function(){
					  $("#sessionTimeut_reloadPage").click(function(){
						  location.reload();
					  });
					  var interval = setInterval(function(){
						var val = $("#alert_time_out_second_span").text()*1 - 1 ;
						if(val==0){
							location.reload();
							clearInterval(interval);
						}
						//避免显示负数
						$("#alert_time_out_second_span").text(val<0?0:val);

					},1000);
				  }
			});

		}
}

//是否开启在线监控
if(checkAlive=="true"){
	setInterval(function(){
		$.ajax({
			   async:false,
			   url: caspath + "/alive",
			   type: "GET",
			   dataType: 'jsonp',
			   jsonp: "callback",
			   data : {
				   tgt : tgt
			   } ,
		       jsonpCallback:"alive",
			   success: function (json) {
				   if(!json){
					   var iframe = document.createElement("iframe");
					   document.body.appendChild(iframe);
					   iframe.style.display = "none";
					   iframe.src = contextpath + "/invalidate";
					   Msg.warning("用户已掉线，请重新登录。",function(){
						   location.href = contextpath+"/logout";
					   });
				   }
			   }
		});
	},60000);//1000为1秒钟
}

/**
 * 清空条件选项
 * pram	选项外层标签DOM的id
 */
template.clearCondition=function($this){
	$("#"+$this).find('input[type="text"]').each(function(){
		$(this).val("");
	});
	$("#"+$this).find('select').each(function(){
		$(this).selectpicker('val', '');
		$(this).selectpicker('refresh');
	});
}

/**
 * base64
 * @type
 */
template.BASE64={
	 // public method for encoding
	 encode:function (input) {
	  var output = "";
	  var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
	  var i = 0;
	  input = template.CODE.utf8_encode(input);
	  while (i < input.length) {
	   chr1 = input.charCodeAt(i++);
	   chr2 = input.charCodeAt(i++);
	   chr3 = input.charCodeAt(i++);
	   enc1 = chr1 >> 2;
	   enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
	   enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
	   enc4 = chr3 & 63;
	   if (isNaN(chr2)) {
	    enc3 = enc4 = 64;
	   } else if (isNaN(chr3)) {
	    enc4 = 64;
	   }
	   output = output +
	   template.CODE.keyStr.charAt(enc1) + template.CODE.keyStr.charAt(enc2) +
	   template.CODE.keyStr.charAt(enc3) + template.CODE.keyStr.charAt(enc4);
	  }
	  return output;
	 },
	 // public method for decoding
	 decode:function (input) {
	  var output = "";
	  var chr1, chr2, chr3;
	  var enc1, enc2, enc3, enc4;
	  var i = 0;
	  input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
	  while (i < input.length) {
	   enc1 = template.CODE.keyStr.indexOf(input.charAt(i++));
	   enc2 = template.CODE.keyStr.indexOf(input.charAt(i++));
	   enc3 = template.CODE.keyStr.indexOf(input.charAt(i++));
	   enc4 = template.CODE.keyStr.indexOf(input.charAt(i++));
	   chr1 = (enc1 << 2) | (enc2 >> 4);
	   chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
	   chr3 = ((enc3 & 3) << 6) | enc4;
	   output = output + String.fromCharCode(chr1);
	   if (enc3 != 64) {
	    output = output + String.fromCharCode(chr2);
	   }
	   if (enc4 != 64) {
	    output = output + String.fromCharCode(chr3);
	   }
	  }
	  output = template.CODE.utf8_decode(output);
	  return output;
	 }
};
template.CODE={
	keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
	 // private method for UTF-8 encoding
	utf8_encode:function (string) {
	  string = string.replace(/\r\n/g,"\n");
	  var utftext = "";
	  for (var n = 0; n < string.length; n++) {
	   var c = string.charCodeAt(n);
	   if (c < 128) {
	    utftext += String.fromCharCode(c);
	   } else if((c > 127) && (c < 2048)) {
	    utftext += String.fromCharCode((c >> 6) | 192);
	    utftext += String.fromCharCode((c & 63) | 128);
	   } else {
	    utftext += String.fromCharCode((c >> 12) | 224);
	    utftext += String.fromCharCode(((c >> 6) & 63) | 128);
	    utftext += String.fromCharCode((c & 63) | 128);
	   }
	  }
	  return utftext;
	 },
	 // private method for UTF-8 decoding
	 utf8_decode:function (utftext) {
	  var string = "";
	  var i = 0;
	  var c = c1 = c2 = 0;
	  while ( i < utftext.length ) {
	   c = utftext.charCodeAt(i);
	   if (c < 128) {
	    string += String.fromCharCode(c);
	    i++;
	   } else if((c > 191) && (c < 224)) {
	    c2 = utftext.charCodeAt(i+1);
	    string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
	    i += 2;
	   } else {
	    c2 = utftext.charCodeAt(i+1);
	    c3 = utftext.charCodeAt(i+2);
	    string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
	    i += 3;
	   }
	  }
	  return string;
	 }
};