/**
 * JsDebug 2
 *     - An Open Source Framework Writen in Javascript for Debugging HTML, CSS and Javascript.
 * @author xuld
 * @license MIT LICENSE
 * @version 2
 * @example
 *    simple log:    log("My Value");
 *    				 trace("My Value");
 *    				 assert(a > 1, " a must be greater than 1.");
 *    
 *       All log apis are members of function named trace such as 'log', 'warm', 'error', 'info', 'runTime'.
 *       The log function is an alterative name of trace.log.
 *    
 *    
 *    log an object: trace([1,2]);  //  get '[1, 2]' 
 *    log runTime:  trace.runTime(function(){}, 1000); // get 0
 *
 *    
 *    YOU MUST NOT REMOVE THIS NOTICE
 *
 *    Homepage:  http://work.xuld.net/jsdebug
 *    Copyright (c) 2011 xuld
 *
 */



(function(undefined){
	
	var options = {
		maxHistory: 50,      // 历史记录。
		text: '调试',		 // 文本。
		unLogged: '当前有{0}个日志没有显示',
		ignoreAssert: true,  // 是否显示  assert 成功信息。
		deep: 2,			 // 遍历对象的最大级数。
		maxLog: 1024,        // 最大的日志缓存。
		display: true,		 // 是否默认打开。
		names: {
			'warn': '<b>[警告]</b>',
			'info': '<b>[提示]</b>',
			'debug': '<b>[调试]</b>',
			'runTime': '<b>[时间]</b>',
			'value': '<b>&gt;&gt;</b>&nbsp;'
		}
	};
	
	
	
	// Badly-formed code, are you insisting on reading?
	
	document.write('<style>\
            #js_debug_window {\
                margin: 100px;\
                position: fixed;\
				top: 0;\
				font-family:  "Courier New" ;\
				font-size:12px;\
				color: #1B4705;\
                right: 0;\
				background-color: #A2DC15;\
				opacity: 0.9;\
				padding: 0px;\
				border: solid 1px #78B202;\
				filter: alpha(opacity=90);\
                _position: absolute;\
                _border: 2px solid #BBB;\
				_top: expression(eval( document.documentElement.scrollTop +8));\
				_right: expression(eval( document.documentElement.scrollLeft +8));\
				z-index:1000\
            }\
			\
			#js_debug_window .header{\
				cursor: default;\
				padding: 3px;\
				background-color:#5E9A00;\
				border-bottom: solid 1px #78B202;\
			}\
			\
			#js_debug_window .button{\
				width:20px;\
				float: right;\
				background: none;\
				border: 1pt solid #CDF5B2;\
				margin-left:2px;\
				padding-left: 4px;\
				padding-right: 4px;\
				height:18px;\
			}\
			\
			#js_debug_window .header h3{\
				margin: 0px;\
			}\
			\
			#js_debug_window ul.content{\
				margin: 0px;\
				padding: 0px;\
				list-style: none;\
				overflow-y: auto;\
			}\
			\
			#js_debug_window  ul.content li{\
				padding:3px;\
				border-bottom: 1pt solid #CDF5B2;\
			}\
			\
			#js_debug_window input.text{\
				font-family:  "Courier New" ;\
				border: 1pt solid #CDF5B2;\
				background: transparent;\
				font-size:12px;\
				vertical-align: bottom;\
				padding:1px 3px;\
			}\
			\
			#js_debug_window .content ul.inspect li{\
				border-bottom: none;\
			}\
			\
			#js_debug_window .content ul.inspect{\
				list-style: none;\
				display: none;\
			}\
			\
			#js_debug_window .menu{\
				position: absolute;\
				width:90px;\
				right: 0px;\
				display: none;\
				background-color: #D2F6BA;\
			}\
			\
			#js_debug_window .menu a{\
				display: block;\
				padding:4px;\
				color: #0BC2BF;\
			}\
			\
			#js_debug_window .content ul.inspect li .item{\
				float: left;\
				width: 100px;\
			}\
			\
			#js_debug_window a{\
				text-decoration: none;\
			}\
			\
			#js_debug_window a:hover{\
				background-color: #AAF585;\
			}\
			\
			#js_debug_window span.ref{\
				color: white;\
				background: gray;\
				padding:2px;\
			}\
			#js_debug_window span.box{\
				cursor: pointer;\
			}\
			#js_debug_window span.box:hover{\
				background-color: #AAF585;\
			}\
			\
			#js_debug_window span.const{\
				color: #cc2168;\
			}\
			\
			.py-high {\
				background-color: #A5D89E;\
				opacity: 0.6;\
				filter: alpha(opacity=60);\
			}\
			\
			#js_debug_window .warn{\
				color: #C77222;\
			}\
			\
			#js_debug_window .info{\
				color: #5E7BBF;\
			}\
			\
			#js_debug_window .error{\
				color: #FF1E2A;\
			}\
			\
			#js_debug_window .m{\
				font-style: italic;\
			}\
			\
			#js_debug_window .runTime{\
				color: #034603; \
				font-style: italic;\
			}\
            \
        </style>\
        <div id="js_debug_window">\
        	<div class="header">\
        		<input type="button" class="button" value="×" onclick="JsDebug.close()" title="关闭，使用 F8 打开。">\
				<input type="button" class="button" value="+" onclick="JsDebug.move()" title="改变窗口位置">\
				<input type="button" class="button" value="○" onclick="JsDebug.clearLogs()" title="清除内容">\
				<input type="button" class="button" value="ˇ" onclick="JsDebug.openMenu()" title="打开菜单">\
        		<h3 id="py_header_title">' + options.text + ' </h3>\
        	</div>\
			<div class="menu" id="js_debug_tool">\
				<a href="javascript:;" onmousedown="JsDebug.mouseinfo()">显示鼠标坐标</a>\
				<a href="javascript:;" onmousedown="JsDebug.bringToFront()">置顶</a>\
				<a href="javascript:;" onmousedown="JsDebug.cookies()">cookies</a>\
				<a href="javascript:;" onmousedown="trace(\' 按 F8 打开或关闭本窗口 \'); trace(\' 使用函数 trace 输出到本窗口。\')">帮助</a>\
				<a href="javascript:;" onmousedown="trace(\' JsDebug 2 by xuld  \')">关于</a>\
			</div>\
			<ul class="content" style="width:480px; height:300px;" id="js_debug_content">\
			\
			</ul>\
			<div class="footer">\
				<input type="button" class="button" value=">" onclick="JsDebug.run(); JsDebug. showValue(\'\')">\
				<input type="text" style="width:450px;" class="text" id="js_debug_editor" onkeyup="JsDebug.handle(event);">\
			</div>\
        </div>\
	');
	
		
	var add = document.addEventListener ? function(elem, type, fn){
			elem.addEventListener(type, fn, false);
		} : function(elem, type, fn){
			elem.attachEvent('on' + type, fn);
		},

		remove = document.removeEventListener ? function(elem, type, fn){
			elem.removeEventListener(type, fn, false);
		} : function(elem, type, fn){
			elem.detachEvent('on' + type, fn);
		},
		
		run = function(v){
			return window.eval(v);
		},
		
		// from PyJs
		format = function(format, object){
			if (format == null) return "";
			var toString = this,
				arr = typeof object == 'object' && object && arguments.length === 2 ? object: Array.prototype.slice.call(arguments, 1);
			return format.replace(/\{+?(\S*?)\}+/g, function(match, name) {
				var start = match.charAt(1) == '{',
					end = match.charAt(match.length - 2) == '}';
				if (start || end) return match.slice(start, match.length - end);
				return name in arr ? toString(arr[name]) : "";
			});
		},
		
		history = [],
		
		historyList = ['trace.dir()', ' = document.getElementById()', 'trace.runTime()', '$()'],
		
		push = function(value){
			if(history.length > options.maxHistory){
				history.shift();
			}
			
			history.push(value);
			p = history.length;
		},
		
		p = 0,
		
		getPop = function(){
			if(p <= 0)
				return null;
			return history[--p] || '';
		},
		
		num = 0,
	
		encodeUTF8 = function(s){
			return s.replace(/\\u([0-9a-f]{3})([0-9a-f])/gi,function(a,b,c){return String.fromCharCode((parseInt(b,16)*16+parseInt(c,16)))})
		},
		
		encodeScript = function(text){
			var c = {
				'\r': 'r',
				'\n': 'n',
				'\t': 't',
				'\a': 'a'
			};
			return text.replace(/\r|\n|\t/g, function(m){
				return '\\' + c[m];
			});
		},
		
		getPush = function(){
			if(p < history.length)
				return history[++p] || '';
			var c = p - history.length;
			if(c < historyList.length)
				p++;
			return historyList[c] || '';
		},
		
		encode = function(text){
			var map = {
				'<': '&lt;',
				'>': '&gt;',
				' ': '&nbsp;',
				'\"': '&quot;',
				'\r\n': '<br>',
				'\r': '<br>',
				'\n': '<br>',
				'\t': '&nbsp;&nbsp;&nbsp;&nbsp;'
			};
			if(text)
				return text.replace(/<|>| |"|\r?\n|\t/g, function(v){
					return map[v];
				});
			return '';
		};
	
	this.JsDebug = {
		
		version: '1.0',
		
		moveList: [
			[100, 0],
			[200, 200],
			[480, 400],
			[1000, 600]
		],
		
		by: 'xuld',
		
		currentMove: 1,
		
		init: function(){
			this.dom = document.getElementById('js_debug_window');
		},
		
		close: function(){
			document.getElementById('js_debug_window').style.display = 'none';
		},
		
		moveTo: function(p){
			p = this.moveList[p % this.moveList.length];
			this.resizeTo(p[0], p[1]);
		},
		
		bringToFront: function(){
			document.getElementById('js_debug_window').style.zIndex = 100000000;
		},
		
		move: function(){
			this.moveTo(this.currentMove++);
		},
		
		show: function(){
			document.getElementById('js_debug_window').style.display = '';
		},
		
		toggle: function(){
			var dom = document.getElementById('js_debug_window').style;
			dom.display = dom.display == 'none' ? '' : 'none';
		},
		
		openMenu: function(){
			document.getElementById('js_debug_tool').style.display = 'block';
			add(document, 'mousedown', JsDebug.hideMenu);
		},
		
		cookies: function(){
			trace(document.cookie);
		},
		
		lock: function(){
			JsDebug.log = E;
		},
		
		unlock: function(){
			JsDebug.log = JsDebug.e;
		},
		
		log: function(type, value){
			
			if(num++ >= options.maxLog){
				JsDebug.hint(options.unLogged.replace('{0}', num - options.maxLog));
				return;
			}
			
			var li = document.createElement('li'), content = document.getElementById('js_debug_content');
			content.appendChild(li);
			
			li.className = type;
			li.innerHTML = (options.names[type] || '')+ value;
			content.scrollTop = content.scrollHeight;
		},
		
		clearLogs: function(){
			JsDebug.hint(options.text);
			cache.length = 0;
			document.getElementById('js_debug_content').innerHTML = ''; num = 0;
		},
		
		hideMenu: function(){
			document.getElementById('js_debug_tool').style.display = 'none';
			remove(document, 'mousedown', JsDebug.hideMenu);
		},
		
		hint: function(value){
			document.getElementById('py_header_title').innerHTML = value;
		},
		
		run: function(){
			var js = document.getElementById('js_debug_editor').value;
			if (js.length) {
				JsDebug.log('value', encode(js));
				push(js);
				JsDebug.log('n', inspect( run(js)   ));
			}
		},
		
		highlightElement: function(elem){
			elem.className += ' py-high';
			setTimeout(function(){
				elem.className = elem.className.replace(' py-high', '');
			}, 1000);
		},
		
		mouseinfo: function(){
			add(document, 'mousemove', function(e){
				JsDebug.hint("" + (e.pageX || e.screenX) + " " + (e.pageY || e.screenY));
			});
		},
		
		showInner: function(e, elem, id, from){
			if(typeof cache[id] !== "string"  ) {
				if(from < 0){
					if(from == -3)
						cache[id] = encode(encodeUTF8(cache[id].toString()));
					else if(from == -4)
						cache[id] = encode(cache[id].innerHTML);
				} else {
					cache[id] = dirObj(cache[id], from || 0);
				}
				
				
			}
			
			
			var data = cache[id];
			cache[id] = elem.innerHTML;
			elem.innerHTML = data;
			
			if(e.stopPropagation){
				e.stopPropagation() ;
			} else {
				e.cancelBubble = true;
			}
			return false;
			
		},
		
		showValue: function(t){
			document.getElementById('js_debug_editor').value = t;
		},
		
		handle: function(e){
			e = e || window.event;
			
			var v;
			switch(e.keyCode){
				case 10:
				case 13:
					JsDebug.run();
					v = '';
					break;
				case 38:
					v = getPop();
					break;
				case 40:
					v = getPush();
					break;
				default:
					return;
			}
			
			
			if(v !== null)
				JsDebug. showValue(v);
			if(e.preventDefault)
				e.preventDefault();
			return e.returnValue = false;
		},
		
		resizeTo: function(x, y){
			var dom = document.getElementById('js_debug_content');
			document.getElementById('js_debug_window').style.width = dom.style.width = x + 'px';
			dom.style.height = y + 'px';
			document.getElementById('js_debug_editor').style.width = x - 35 + 'px';
		}
	};
	
	var cache = [];
	
	function dirObj(obj, set){
		var r = [];
		for (var i in obj) {
				if (set-- > 0) 
					continue;
				try {
					r.push(i + ':' + inspect(obj[i], -1) + '');
				} catch (e) {
				};
		}
		
		return r.join(r.length > options.deep?',<br>' : ', ');
	}
	
	function trace(){
		out.apply('trace', arguments);
	}
	
	function out(values){
		if (arguments.length == 0) return;
		if (typeof values == "string") {
			if(arguments.length > 1)
				values = format.apply(inspect, arguments);
			else
				values = encode(encodeScript(values)) ;
		} else 
			values = inspect(values);
		
		
		JsDebug.log(this, values);
	}
	
	function inspect(obj, deep){
		deep = deep || options.deep;
		switch (typeof obj) {
			case "function":
				
				cache.push(obj);
				//  函数
				return '<span class="box" onclick="return JsDebug.showInner(event, this, ' + (cache.length -1 ) + ', -3)">function&nbsp;()</span>';
				
			case "object":
		
				if (obj == null) return '<span  class="ref">null</span>';
				
				if(Date == obj.constructor || obj.constructor == RegExp)
					return obj.toString();
				
				var len = cache.length;
				
				
				cache.push(obj);
				
				if ('setInterval' in obj && 'resizeTo' in obj) {
					return '<span class="box" onclick="return JsDebug.showInner(event, this, ' + len + ', 0)">window <i>' + obj.document.title + '</i></span>';
				}
				if ('nodeType' in obj) {
						if(obj.nodeType == 9)
							return '<span class="box" onclick="return JsDebug.showInner(event, this, ' + len + ', 0)">document <i>' + obj.title + '</i></span>';
						if (obj.tagName) {
							
							
							var r = ['&lt;', obj.tagName.toLowerCase()];
							
							
							for(var i = 0, len8 = obj.attributes.length; i < len8; i++){
								
								var v = obj.attributes[i].value, n = obj.attributes[i].name;
								if (typeof obj[n] != 'function' && v != 'null' && v) {
									r.push(' ');
									r.push( n );
									r.push('="<span class="const">');
									r.push(v)
									r.push('</span>"');
								}
							}
							
							r.push('&gt;');
							r.push('<span class="box" onclick="return JsDebug.showInner(event, this, ' + len + ', -4)">..</span>');
							r.push('&lt;/')
							r.push(obj.tagName.toLowerCase());
							r.push('&gt;');
							
							
							return r.join('');
						}else{
							
							return obj.nodeName + '&nbsp;<span class="box" onclick="return JsDebug.showInner(event, this, ' + len + ', -4)">..</span>';
						}
					}
				
				try{
					if(obj.length  !== undefined){
						obj[0];
					}
				}catch(e){
					return '[Object]';
				}
				
				var r = [];
				
				if(obj.length !== undefined){
					
					for(var i = 0; i < obj.length; i++){
						r.push(inspect(obj[i], -1));
					}
					
					
					return '[' + r.join(', ') + ']';
				} 
				
				for(var item in obj){
					if(r.length > deep){
						break;
						
					}
					r.push(item + ':' + inspect(obj[item], -1));
				}
				
				
				if(r.length > deep)
					r.push('<span class="box" onclick="return JsDebug.showInner(event, this, ' + len + ', ' + r.length + ')">..</span>')
				
				
				return '{' + r.join(', ') + '}';
				
			case "string":
				return '<span  class="const">"' + encode(encodeScript(obj)) + '"</span>';
			case "undefined":
				return '<span  class="ref">undefined</span>';
			case "boolean":
			case "number":
				return '<span  class="const">' + obj + '</span>';
			default:
				return obj.toString();
		}
	}
	
	function copy(dest, src){
		for(var i in src){
			dest[i] = src[i]   ;
		}
	}
	
	function assert(bValue){
		if(!bValue)
			out.apply('error', arguments.length == 1 ? ['assert  Error'] : Array.prototype.slice.call( arguments ,1) );
		else if(!options.ignoreAssert)
			out.call('m', 'assert  OK');
	}
	
	if(this.trace)
		copy(trace, this.trace);
		
	if(this.assert)
		copy(trace, this.assert);
	
	copy(trace, {
		
		alert: function(message){
			alert(message);
		},
		
		log: function(){
			var r = [];
			for(var i = 0; i < arguments.length  ; i++){
				r.push(inspect(arguments[i], 1));
			}
			
			JsDebug.log('trace', r.toString());
		},
		
		debug: function(v){
			if(!JsDebug.off){
				out.apply('debug', arguments);
			}
		},
		
		info: function(v){
			out.apply('info', arguments);
		},
		
		warn: function(v){
			out.apply('warn', arguments);
		},
		
		dir: function(v){
			JsDebug.log('', dirObj(v));
		},
		
		error: function(v){
			out.apply('error', arguments);
		},
		
		ifDebug: function(f) {
			if (!JsDebug.off) return;
			try {
				f();
				return "";
			} catch(e) {
				return e;
			}
		},

		clear: function() {
			JsDebug.clearLogs();
		},

		empty: function(msg) {
			JsDebug.log('m', "OK    " + ( msg || ""));
		},

		ifNot: function(condition, msg) {
			if (!condition) trace.warn(msg);
		},
		
		test: function(fn, times){
			JsDebug.log('runTime', trace.runTime(fn, times) + '     ' + inspect(fn)  + '   ' + (times || 1000));
		},

		runTime: function(fn, times) {
			times = times || 1000;
			JsDebug.lock();
			var d = new Date();
			while (times-->0)
				fn();
			d = new Date() - d;
			JsDebug.unlock();
			return d;
		}
	});
	
	function E(){}
	
	
	
	add(document, 'keydown', function(e){
		if (e.keyCode == 119) {
			JsDebug.toggle();
		}
	});
	
	window.onerror = function(msg,url,line){
		trace.error('#' + line + ' ' + msg);
	};
	
	
	JsDebug.e = JsDebug.log;
	
	if(!options.display){
		JsDebug.hide();
	}
	
	copy(assert, {
		
		notNull: function(value, argsName) {
			return assert(value != null, "{0} 为 null 。", argsName || "参数");
		},

		between: function(value, min, max, argsName){
			return assert(value >= min && (max === undefined || value < max), "{0} 超出索引, 它必须在 [{1}, {2}) 间。",  argsName || "参数", min, max === undefined ? "+∞" : max);
		},
		
		instanceOf: function(v, types, message) {
			if (!types.length || typeof types == 'string') types = [types];
			var ty = typeof v;
			return assert(types.filter(function(type) {
				return type == ty;
			}).length, message || "类型错误。");
		},

		notEmpty: function(value, argsName) {
			return assert(value && value.length, "{0} 为空 。", argsName || "参数");
		},

		notStatic: function(value, argsName) {
			return assert(typeof value == 'object' && value, "{0} 为引用变量。", argsName || "参数");
		}
	
	});
	
	JsDebug.moveTo(2);
	
	copy(this, {
		trace: trace,
		log: trace.log,
		assert: assert,
		dir: trace.dir
	});
	
	
	
})();
