async function startPayment(orderId){
    try{
        const response = await ApiClient.post(
            "payments/api/create/",
            {
                order_id: orderId,
                payment_method:"SSLCOMMERZ"
            }
        );
        console.log("PAYMENT RESPONSE:", response);
        if(response.gateway.GatewayPageURL){
            window.location.href = response.gateway.GatewayPageURL;
        }
        else{
            alert("Gateway URL missing. Check SSLCommerz response");
        }
    }
    catch(error){
        console.log(error);
    }
}