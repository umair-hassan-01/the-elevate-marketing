const product_id = {
    "SOUND_CLOUD": "price_1Pc98mRpdWCgKVCA4EZ2XnWB",
    "GENIUS_BLOG": "price_1PbLvCRpdWCgKVCA5ULIgTQQ",
    "YOUTUBE_PLAN": "price_1Pc99iRpdWCgKVCAfxADl9WP",
    "SPOTIFY_PLAN": "price_1PbLwhRpdWCgKVCAPUUPCgQI",
    "GOLD_PLAN": "price_1Pc9A6RpdWCgKVCAQVyPAux6",
    "PLATINUM_PLAN": "price_1Pc9APRpdWCgKVCAx8hXzPCj",
    "THE_ELEVATE_PLAN": "price_1Pc9AgRpdWCgKVCA9JMfoDDV",
    "DIAMOND_PLAN": "price_1Pc9B8RpdWCgKVCAjBXMQ42B"
}

const stripe = Stripe("pk_test_51PbJAlRpdWCgKVCA9srthb9mwm18EQq0y2foHE9zM9wKTsn5vgicHatUQFRJ9X3d4cODH99VuIOfYzNNTp516ygi00aNtM6ax2");


async function getStripeSession(productId){
    const response = await fetch("./create-checkout-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            productId: productId
        })
    });
    return response.json();
}

async function redirectToCheckout(productId){
    const { sessionId } = await getStripeSession(productId);
    console.log(`session id = ${sessionId}`);
    if(sessionId === "wrong"){
        window.location.replace("./payment-cancel");
        return;
    }
    const { error } = await stripe.redirectToCheckout({
        sessionId
    });
    if(error){
        console.error(error);
    }
}

const elems = document.getElementsByClassName('payment-button');
for(let i = 0;i < elems.length;i++){
    elems[i].addEventListener('click' , (event)=>{
        event.preventDefault();
        const current_id = elems[i].id;
        redirectToCheckout(product_id[current_id]);
    })
}