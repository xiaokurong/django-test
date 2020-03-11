//服务器分组数量展示
var myChart2 = echarts.init(document.getElementById('server_count'));

$.get('http://127.0.0.1:8000/saltapi/servergroupapi',function(data){
        var groupname = new Array();
        var count1 = new Array()

        for (var i=0; i < data.list.length;i++)
        {
            groupname[i]=data.list[i].group_name
            count1[i] = data.list[i].c
        }
//        console.log('groupname is : '+groupname)
//        console.log(groupname)
//        console.log('count1 is : '+count1)
        myChart2.setOption({
            title: {
                text: '服务器分组'
            },
            tooltip: {},
            legend: {
                data: ['数量']
            },
            xAxis: {
                data: groupname ,
                "axisLabel":{
                interval: 0
                }
            },
            yAxis: {},
            series : [{
                    name: '数量',
                    type: 'bar',
                    data: count1 ,
                }],
        });
});


//历史命令展示

$.get('http://127.0.0.1:8000/saltapi/historyapi',function(history){

        var xData = new Array();
        var yData = new Array();
        for (var i=0; i < history.data.length;i++)
        {
            xData.push(history.data[i].command_name);
            yData.push(history.data[i].c);
        }
//        console.log('xData length is : '+xData.length);
//        console.log('xData is : '+xData);
        var dom = document.getElementById("history_cmd");
        var myChart3 = echarts.init(dom);
        var app = {};
        option = null;
        option = {
            title: {
                text: '历史命令排行'
            },
            color: ['#3398DB'],
            tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                    type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: xData,
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: [
                {
                    name: '直接访问',
                    type: 'bar',
                    barWidth: '60%',
                    data: yData
                }
            ]
        };
        ;
        if (option && typeof option === "object") {
            myChart3.setOption(option, true);
        }

});





// 服务器增量展示
//var myChart1 = echarts.init(document.getElementById('server_add'));
$.get('http://127.0.0.1:8000/saltapi/serverapi',function(data){
    var dom = document.getElementById("server_add");
    var myChart4 = echarts.init(dom);
    var app = {};
    option = null;
    var xAxisData = [];
    var data1 = [];
    var data2 = [];
    for (var i=0; i < data.data.length;i++)
        {
            data1.push(data.data[i][0]);
            data2.push(data.data[i][1]);
            xAxisData.push(data.data[i][2])
        }
     console.log("xAxisData is :" + xAxisData)
     console.log("data1 is : " + data1)
     console.log("data2 is : " + data2)
//    for (var i = 0; i < 10; i++) {
//        xAxisData.push('类目' + i);
//        data1.push((Math.sin(i / 5) * (i / 5 -10) + i / 6) * 5);
//        data2.push((Math.cos(i / 5) * (i / 5 -10) + i / 6) * 5);
//    }


    option = {
        title: {
            text: '服务器增量展示'
        },
        legend: {
            data: ['总量', '增量']
        },
        toolbox: {
            // y: 'bottom',
            feature: {
                magicType: {
                    type: ['stack', 'tiled']
                },
                dataView: {},
                saveAsImage: {
                    pixelRatio: 2
                }
            }
        },
        tooltip: {},
        xAxis: {
            data: xAxisData,
            splitLine: {
                show: false
            }
        },
        yAxis: {
        },
        series: [{
            name: '总量',
            type: 'bar',
            data: data1,
            animationDelay: function (idx) {
                return idx * 10;
            }
        }, {
            name: '增量',
            type: 'bar',
            data: data2,
            animationDelay: function (idx) {
                return idx * 10 + 100;
            }
        }],
        animationEasing: 'elasticOut',
        animationDelayUpdate: function (idx) {
            return idx * 5;
        }
    };;
    if (option && typeof option === "object") {
        myChart4.setOption(option, true);
    }

});



var dom = document.getElementById("test1");
var myChart5 = echarts.init(dom);
var app = {};
option = null;
option = {
    title: {
        text: '某站点用户访问来源',
        subtext: '纯属虚构',
        left: 'center'
    },
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: ['直接访问', '邮件营销', '联盟广告', '视频广告', '搜索引擎']
    },
    series: [
        {
            name: '访问来源',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [
                {value: 335, name: '直接访问'},
                {value: 310, name: '邮件营销'},
                {value: 135, name: '视频广告'},
                {value: 234, name: '联盟广告'},
                {value: 1548, name: '搜索引擎'}
            ],
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};
;
if (option && typeof option === "object") {
    myChart5.setOption(option, true);
}
