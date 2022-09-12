function validateBidding() {
    var current_bid = document.getElementById("current_bid").getAttribute("data-bid")
    var new_bid = document.getElementById("bid").value
    if (current_bid >= new_bid) {
        alert("Your bid is not enough!")
    }
    console.log(bidding_amount)
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function makeComment() {
    var comment = document.getElementById("floatingTextarea2")
    var comment_text = comment.value
    comment.value = ""
    var listing_pk = document.getElementById("comment-btn").getAttribute("data-listing")
    var user = document.getElementById("comment-btn").getAttribute("data-user")
    var comments = document.getElementById("comments")
    form = "<form class='form-floating' style='margin-bottom: 1%;'>\
    <input type='text' readonly class='form-control' id='floatingInputValue'\
            value="+'"'+ comment_text + '"'+">\
    <label for='floatingInputValue'>" + user + "</label>\
    </form>"
    var url = "http://localhost:8000" + document.getElementById("comment-btn").getAttribute("data-url")
    console.log(url);
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({listing_pk: listing_pk, comment_text: comment_text})
    })

    comments.innerHTML += form
}