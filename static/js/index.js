 /**
 阻止回车的时候表单提交
 */
function ClearSubmit(e) {
    if (e.keyCode == 13) {
        return false;
    }
}

/**
 * 自执行函数，用于设置 #map-d3 的高度
 */
(function(){
  var map_height = document.body.clientHeight - 230;
  map_height = parseInt(map_height / 100) * 100;

  document.getElementById("map-d3").style.height = map_height + "px";
})();

$(function() {
var vm = new Vue({
  el : '#app',
  extends: CommonTools,

  data : function() {
    return {
      // 搜索关键字
      keyword : '',

      // 当前是否为高级搜索模式
      advancedSearch : false,

      // 高级搜索 : TODO
      // 名字
      name : '',
      // 学院
      institution:'',
      // 搜索类型： 简单/高级
      search_type : '高级',

      // 判断是否已点搜索按钮
      has_searched : false,

      // 热点词
      hot_key_list : ['数据挖掘','机器学习','社交网络','深度学习','医疗健康','人工智能','数据库','云计算'],

      // 标志在非index页面时，导航栏处显示搜索框
      not_index : false,

      /* 输入搜索内容时，显示隐藏提示框 */
      show_hide_tip : false,

      /**
       * 记录每次需要异步获取联想关键字的 setTimeout 函数
       *
       * 作用在于可以减少快速输入搜索内容时的 异步请求次数
       */
      recode_setTimeout : undefined,

      // 联想词列表
      associative_words_list : [],

      /**
       * 该参数 目的 是 解决点击联想框/热点词 后重复响应  keyword 的 watch 事件 ==> 产生联想事件，
       * 因此，当 click_from_exists = true 时，表示词条来源于联想框，不需要再次发送 ajax 请求
       * */

      click_from_exists : false,
	  }
  },

  watch:{
    /**
     * 监听 keyword 的变化
     */
    keyword : function(){

      // 若 keyword 为空 or 变更来自于 联想框/热点词
      if(!this.keyword || this.click_from_exists){

        // 设置来源，防止点击热点词后 手动搜素不再出现联想框 的情况
        this.click_from_exists = false;

        // 隐藏联想框
        this.show_hide_tip = false;

        return;
      }

      // 清空上一个尚未响应的函数
      clearTimeout(this.recode_setTimeout);

      // 设置输入时间间隔为 0.6s
      this.recode_setTimeout = setTimeout(this.getAssociativeWordsByAjax.bind(this),600)

    },


  },

  methods: {
     open : function(t){
       if(t=='Need'){
          content = ['../static/publicNeed.html', 'yes']
        }

      layer.open({
          type: 2,
          title:t,
          area: ['1100px', '80%'], //宽高
          content: content
       });
    },

    /**
     * 通过 ajax 获取搜索框中的联想词
     */
    getAssociativeWordsByAjax : function(){
      // TODO

      this.show_hide_tip = true;

      this.associative_words_list = ['社交网络','深度学习','医疗健康','人工智能'];
    },

    /**
     * 点击搜索热点词 / 联想词
     * @param {*} event ： 点击事件的受体
     */
    search_hot_word : function(event){
      // 标志当前变更来源于 已有字符，不必再触发 ajax 联想请求
      this.click_from_exists = true;

      t = event.target.innerText;
      this.keyword = t;


      this.go_search();
    },


    /**
     * 开始搜索
     */
    go_search : function(){
        username = document.getElementById("username");
            //if($("#username").text())
            if(!username)
            {
                window.location.href="/login";
                return
            }
        // 关闭联想框
        this.show_hide_tip = false;

        // 标识搜索开始，显示地图
        this.has_searched = true;

        url='../static/searchreasult.html?keyword='+encodeURI(encodeURI(this.keyword))+'&name='+encodeURI(encodeURI(this.name))+'&institution='+encodeURI(encodeURI(this.institution));
//        window.location.href=url
        // $(window).attr('location',url);
    },


    /**
     * 修改搜索方式 ： 简单 / 高级
     */
    change_search : function(){
        if(this.search_type=='高级'){
          this.search_type='简单';
          this.advancedSearch = true;
        }else{
          this.search_type='高级';
          this.advancedSearch = false;
        }
    },

    
  },

  
  created:function() {
  },
});
});