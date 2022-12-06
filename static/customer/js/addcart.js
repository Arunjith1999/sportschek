//Add to Cart
$('#addtoCartBtn').on('click',function(){

     var _qty=$('#productQty').val();
     var _productId=$('.product-id').val();
     var _customerId=$('.customer-id').val();
     console.log(_qty,_productId,_customerId)
});

//end