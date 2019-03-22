$(document).ready(function(){


            function renderChart(id, data, labels, ctip, etiket){
                // var ctx = document.getElementById("myChart").getContext('2d');
                Chart.defaults.global.defaultFontColor = 'black';
                Chart.defaults.global.defaultFontSize = 12;
                var ctx = $('#' + id);
                var myChart = new Chart(ctx, {
                    type: ctip,
                    data: {
                        labels: labels,
                        datasets: [{
                            label: etiket,
                            data: data,
                            backgroundColor: 'rgba(113, 255, 31, 1)',
                            borderColor: 'rgba(47, 128, 0, 1)',
                        }],
                        borderWidth: 1,

                    },
                    options: {
                              // title: {
                              //   display: true,
                              //   text: ''
                              //    },


                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero:true
                                }
                            }]
                        },
                        // backgroundColor: 'rgba(113, 255, 31, 1.5)'#
                    }
                });
            }


            function getSalesData(id, type){
                var url = '/analytics/sales/data/';
                var method = 'GET';
                var data = {"type":type};
                $.ajax({
                    url: url,
                    method: method,
                    data: data,
                    success: function(responseData){
                        renderChart(id, responseData.data, responseData.labels, responseData.ctip, responseData.etiket )
                    }, error: function(error){
                        $.alert("Bir hata oluştu")
                    }

                })

            }

            var chartsToRender = $('.cfe-render-chart')
            $.each(chartsToRender, function(index, html){
                var $this = $(this)
                if ($this.attr('id') && $this.attr('data-type')){
                    getSalesData($this.attr('id'),$this.attr('data-type'))
                }


            })

            })

// function renderChart1(id, data, labels){
//                 // var ctx = document.getElementById("myChart").getContext('2d');
//                 var ctx = document.getElementById("product").getContext('2d');
//                 var myChart = new Chart(ctx, {
//                     type: 'bar',
//                     data: {
//                         labels: ["tolga","bekir"],
//                         datasets: [{
//                             label: 'Satışlar(TL)',
//                             data: ["20","20"],
//                             backgroundColor: 'rgba(113, 255, 31, 1)',
//                             borderColor: 'rgba(47, 128, 0, 1)'
//                         }]
//                     },
//                     options: {
//                         scales: {
//                             yAxes: [{
//                                 ticks: {
//                                     beginAtZero:true
//                                 }
//                             }]
//                         },
//                         // backgroundColor: 'rgba(113, 255, 31, 1.5)'#
//                     }
//                 });
//             }
//
//
//             function getSalesData1(id, type){
//                 var url = '/analytics/sales/data/';
//                 var method = 'GET';
//                 var data = {"type":type};
//                 $.ajax({
//                     url: url,
//                     method: method,
//                     data: data,
//                     success: function(responseData){
//                         renderChart1(id, responseData.data, responseData.labels)
//                     }, error: function(error){
//                         $.alert("Bir hata oluştu")
//                     }
//
//                 })
//
//             }
//              var chartsToRender = $('.cfe-render-chart')
//             $.each(chartsToRender, function(index, html){
//                 var $this = $(this)
//                 if ($this.attr('id') && $this.attr('data-type')){
//                     getSalesData($this.attr('id'),$this.attr('data-type'))
//                 }
//
//
//             })
//
//             })