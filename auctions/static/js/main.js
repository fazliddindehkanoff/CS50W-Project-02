function validateBidding() {
    var current_bid = document.getElementById("current_bid").getAttribute("data-bid")
    var new_bid = document.getElementById("bid").value
    if (current_bid >= new_bid) {
        alert("Your bid is not enough!")
    }
    console.log(bidding_amount)
}