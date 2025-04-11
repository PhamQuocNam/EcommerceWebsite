console.log("working fine");

$("#commentForm").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url : $(this).attr("action"),

        dataType: "json",

        success: function(response){
            console.log("Comment Saved to DB");

            if(response.bool == true){
                $("#review-res").html("Review successfully")
                $(".hide-comment-form").hide()
            }
        }
        })

})

$(".add-to-cart-btn").on("click", function(){

    let this_val =  $(this)
    let index = this_val.attr("data-index")
    
    let  quantity = $(".product-quantity-"+ index).val()
    let product_name = $(".product-name-" +index).val()

    let product_pid = $(".product-pid-"+index).val()
    let product_price = $(".current-product-price-" + index).text()
    let product_image = $(".product-image-" + index).val()
    

    console.log("Quantity:", quantity);
    console.log("Name:", product_name);
    console.log("ID:", product_pid);
    console.log("Price:", product_price);
    console.log("Image:", product_image);
    console.log("Index", index);
    console.log("Current Element:", this_val)
  
    $.ajax({
      url: '/add-to-cart',
      data: {
            'Image': product_image,
          'ID_Product': product_pid,
          'Quantity': quantity,
          'Price': product_price,
          'Name': product_name
      },
      dataType: 'json',
      beforeSend: function(){
          console.log("Adding Product to Cart...");
      },
      success: function(response){
          this_val.html("Done!")
          console.log("Added Product to Cart!");
          $(".cart-items-count").text(response.totalcartitems)
          $(".total-price").text("$"+response.totalmoney)
      }
    })
  })




$(".delete-product").on("click", function () {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);

    console.log("Product ID:", product_id);

    $.ajax({
        url: "/delete-from-cart",
        data: {"id": product_id },
        dataType: "json",
        beforeSend: function () {
            this_val.hide();
        },
        success: function (response) {

            this_val.show();
            $(".cart-items-count").text(response.totalcartitems);
            console.log("It works!");
            $("#cart-list").html(response.data);
        },
        
        })
    });


    $(".update-product").on("click", function () {
            
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        let quantity = this_val.closest("tr").find(".quantity-number").val();
    
        console.log("Product ID:", product_id);
        console.log("Quantity:", quantity);
        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "Quantity": quantity,
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide();
            },
            success: function (response) {
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data);
            }
        });
    });


    $(".update-prod").on("click", function () {
        let this_val = $(this);
        const products = document.querySelectorAll('.product');
        const ids = [];
        const quantities=[];
        products.forEach(product => {
        const id = product.getAttribute('data-id');
        const quantity = document.querySelector('.product-quantity-'+id).value;
        quantities.push(quantity);
        ids.push(id);
      });


      $.ajax({
        url: "/update-items-cart",
        data: {
            "ids": ids.join(','),
            "quantities": quantities.join(','),
        },
        dataType: "json",
        beforeSend: function () {
            this_val.hide();
        },
        success: function (response) {
            this_val.show();
            $(".cart-items-count").text(response.totalcartitems);
            $("#cart-list").html(response.data);
        }
    });

    });




// $(".add-to-cart-btn").on("click", function(){
//   let  quantity = $("#product-quantity").val()
//   let product_name = $(".product-name").val()
//   let product_id = $(".product-id").val()
//   let product_price = $(".curent-product-price").val()
//   let this_val = $(this)
//   console.log("Quantity:", quantity);
//   console.log("Name:", product_name);
//   console.log("ID:", product_id);
//   console.log("Price:", product_price);
//   console.log("Current Element:", this_val)

//   $.ajax({
//     url: '/add-to-cart',
//     data: {
//         'ID_Product': product_id,
//         'Quantity': quantity,
//         'Price': product_price
//     },
//     dataType: 'json',
//     beforeSend: function(){
//         console.log("Adding Product to Cart...");
//     },
//     success: function(response){
//         this_val.html("Item added to cart");
//         console.log("Added Product to Cart!");
//         $(".cart-items.count").text(response.totalcartitems)
//     }
//   })
// })

