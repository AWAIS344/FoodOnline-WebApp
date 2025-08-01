let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['pk']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields

    var geocoder=new google.maps.Geocoder()
    var address=document.getElementById("id_address").value

    geocoder.geocode({'address:':address},function(results,status){

        if( status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            $("#id_latitude").val(latitude);
            $("#id_longitude").val(longitude);

            $("#id_address").val(address);

        }
        
    });
    for(var i=0;i<place.address_compinents.lenght;i++){
        for ( var j=0;j<place.address.components[i].types.lenght;j++){
            // get country
            if (place.address_components[i].types[j] == "country"){
                $("id_country").val(place.address_components[i].long_name);
            }

            //get state
            if (place.address_components[i].types[j] == "adminstrative_area_level_1"){
                $("id_state").val(place.address_components[i].long_name);
            }

            //get city

            if (place.address_components[i].types[j] == "locality"){
                $("id_city").val(place.address_components[i].long_name);
            }

            //get pincode
            if (place.address_components[i].types[j] == "postal_code"){
                $("id_pin_code").val(place.address_components[i].long_name);
            }else{
                $("id_pin_code").val("");
            }



        }
    }
}


$(document).ready(function(){

    // ADD TO CART
    $(".add_to_cart").on("click",function(e){
        e.preventDefault();
        
        food_id=$(this).attr("data-id");
        url=$(this).attr("data-url");

        
        $.ajax({
            type:"GET",
            url:url,
            
            success : function(response){
                console.log(response.cart_counter['cart_count'])
                $("#cart_counter").html(response.cart_counter['cart_count']);
                $("#qty-"+food_id).html(response.qty);
            }

        })
    })

    $(".item_qty").each(function(){

        var the_id=$(this).attr("id")
        var qty=$(this).attr("data-qty")
        console.log(qty)

        $("#"+the_id).html(qty)


    })


    // DECREASE CART

    $(".decrease_cart").on("click",function(e){
        e.preventDefault();
        
        food_id=$(this).attr("data-id");
        url=$(this).attr("data-url");

        
        // $.ajax({
        //     type:"GET",
        //     url:url,
        //     success : function(response){
        //         console.log(response)
                
        //         $("#cart_counter").html(response.cart_counter['cart_count']);
        //         $("#qty-"+food_id).html(response.qty);
        //     }

        // })
    })

    



});