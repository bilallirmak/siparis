$(document).ready(function(){
            function renderChart(id, data, labels){
                // var ctx = document.getElementById("myChart").getContext('2d');
                var ctx = $('#' + id);
                var myChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Satışlar(TL)',
                            data: data,
                            backgroundColor: 'rgba(113, 255, 31, 1)',
                            borderColor: 'rgba(47, 128, 0, 1)'
                        }]
                    },
                    options: {
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
                        renderChart(id, responseData.data, responseData.labels)
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