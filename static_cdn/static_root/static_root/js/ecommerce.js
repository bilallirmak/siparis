 $(document).ready(function(){
            // {#Auto Search#}

            var searchForm = $(".search-form")
            var searchInput = searchForm.find("[name='q']")
            var typingTimer;
            var typingInterval = 500; //.5-seconds
            var searchBtn = searchForm.find("[type='submit']")

            // searchInput.keyup(function(event){
            //     // key-released
            //     clearTimeout(typingTimer)
            //     typingTimer = setTimeout(performSearch, typingInterval)
            // })
            searchInput.keydown(function(event){
                // key-pressed
                clearTimeout(typingTimer)

            })
            function displaySearching(){
                searchBtn.addClass("disabled")
                searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Aranıyor..")

            }

            function performSearch(){
                displaySearching()
                var query = searchInput.val()
                setTimeout(function(){
                    window.location.href = '/search/?q=' + query

                }, 1000)
            }



            // Cart-and-Add-Products
            var productForm = $(".form-product-ajax")

            productForm.submit(function(event){
                event.preventDefault();
                // {#console.log("Form Gönderilemedi")#}
                var thisForm = $(this)
                // {#var actionEndpoint = thisForm.attr("action");#}
                var actionEndpoint = thisForm.attr("data-endpoint");
                var httpMethod = thisForm.attr("method");
                var formData = thisForm.serialize();

                $.ajax({
                    url: actionEndpoint,
                    method: httpMethod,
                    data: formData,
                    success: function(data){
                        var submitSpan = thisForm.find(".submit-span")
                        if (data.added){
                            submitSpan.html("<button type=\"submit\" class=\"btn btn-sm\">Sepetten Çıkar</button>")
                        } else{
                            submitSpan.html("<button type=\"submit\" class=\"btn btn-success\">Sepete Ekle</button>")
                        }
                        var navbarCount = $(".navbar-cart-count")
                        navbarCount.text(data.cartItemCount)
                        var currentPath = window.location.href
                        if (currentPath.indexOf("cart") != -1){
                            refreshCart()
                        }
                    },
                    error: function(errorData){
                        $.alert({ title:"Oops", content: "Bir hata oluştu", theme: "modern",})

                    }
                })

            })
            function refreshCart(){
                console.log("in current cart")
                var cartTable = $(".cart-table")
                var cartBody = cartTable.find(".cart-body")
                // {#cartBody.html("<h1>Changed</h1>")#}
                var productRows = cartBody.find(".cart-product")
                var currentUrl = window.location.href

                var refreshCartUrl = "/api/cart"
                var refreshCartMethod = "GET"
                var data = {}

                $.ajax({
                    url: refreshCartUrl,
                    method: refreshCartMethod,
                    data: data,

                    success: function(data){

                        var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                        if (data.products.length > 0){
                            productRows.html(" ")
                            i = data.products.length
                            $.each(data.products,  function(index, value){
                                console.log(value)
                                var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                                newCartItemRemove.css("display", "block")
                                // newCartItemRemove.removeClass("hidden-class")
                                newCartItemRemove.find(".cart-item-product-id").val(value.id)
                                cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href=''" + value.url + "'>" + value.name + "</a>" + newCartItemRemove1.html() + "</td> <td>" + value.quantity + "</td><td>" + value.line_total + "</td></tr>")
                                i --
                                 // cartBody.find(".cart-total").text(value.total)
                            })
                            // cartBody.find(".cart-subtotal").text(data.subtotal)
                            cartBody.find(".cart-total").text(data.total)
                        } else {
                            window.location.href = currentUrl
                        }

                    },
                    error: function(errorData){
                        $.alert({ title:"Oops", content: "Bir hata oluştu", theme: "modern"})
                    }

                })

            }
 })

