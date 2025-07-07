Page({
    data: {
        placeholder: 'Hello editor!',
        readOnly: false,
        contents: {
            html: `<div id="magicdomid-1_19" class="ace-line align-center heading-h1  locate lineguid-B2nSe8" dir="auto"><span class=" ">祝福</span></div><div id="magicdomid-1_26" class="ace-line blockquote blockquote  locate lineguid-17mqsc" dir="auto"><span class=" ">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 祥林嫂是一个受尽封建礼教压榨的穷苦农家妇女。丈夫死后，狠心的婆婆要将她出卖。她被逼出逃，到鲁镇鲁四老爷家做佣工，受尽鄙视、虐待。很快她又被婆婆家抢走，并且拿走了她在鲁四老爷家打工的所有工钱，然后卖到贺家成亲。贺老六是个纯朴忠厚的农民，很快又有了儿子阿毛，祥林嫂终于过上了安稳日子。</span></div><div id="magicdomid-1_27" class="ace-line locate lineguid-6UxLlZ" dir="auto"><span class=" ">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 然而命运多舛，贺老六因伤寒病复发而死，不久，阿毛又被狼吃掉。经受双重打击的祥林嫂，丧魂落魄，犹如行尸走肉，于是，走投无路的她只能去再次投奔到鲁四老爷家。可是人们还说她改嫁“有罪”，要她捐门槛“赎罪”，不然到了“阴间”还要受苦。她千辛万苦积钱捐了门槛后，依然摆脱不了人们的歧视。</span></div><div id="magicdomid-1_37" class="ace-line locate lineguid-AWIi9E" dir="auto"><span class=" ">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class=" backgroundcolor " style="background-color: #FFF362; ">最后，她沿街乞讨，在鲁镇一年一度的“祝福”的鞭炮声中，惨死在街头。但是，人们非但没有可怜她，还都骂她是一个谬种</span></div><div id="magicdomid-1_38" class="ace-line" dir="auto"><br></div><div id="magicdomid-1_34" class="ace-line" dir="auto"><br></div><div id="magicdomid-1_35" class="ace-line image-upload single-line" dir="auto"><span><div contenteditable="false" class="image-container single-elem-cls"><span class="image-wrapper"><span class="point tl n-icon-dragable"></span><span class="point tr n-icon-dragable"></span><span class="point br n-icon-dragable"></span><span class="point bl n-icon-dragable"></span><img src="https://gss1.bdstatic.com/9vo3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268%3Bg%3D0/sign=4afed6cb0323dd542173a06ee932d4e3/562c11dfa9ec8a13e2cafd4ffd03918fa1ecc049.jpg" data-faketext=" " data-uuid="LxW0dlVX" class="editor_image" style="width: 369px;height: 491.7763636363636px"></span></div></span></div><div id="magicdomid-1_36" class="ace-line" dir="auto"><br></div>
`
        },
        plugins: ['mention', 'insertImage' ,'undo', 'redo'],
        placeholderStyle: {
            color: '#FFFD00',
            fontSize:"25px"
        }
    },
    onLoad: function () {

    },
    onShow: function () {

    },
    onHide: function () {
    },

    onEditorReady: function (res) {
        console.log('onEditorReady '  + JSON.stringify(res))
    },
    onEitorInputValueChange: function(res) {
        console.log('onEitorInputValueChange '  + JSON.stringify(res))
    },

    onMentionSelect: function(res) {
        console.log('onMentionSelect ' + JSON.stringify(res))
    },

    onMentionClick: function(res) {
        console.log('onMentionClick ' + JSON.stringify(res))
    },

    onInsertImages: function (res) {
        console.log('onInsertImages '  + JSON.stringify(res));
        res.insertImagesCallback(res.images);
    }
})
