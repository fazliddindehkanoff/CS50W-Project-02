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


function validateBidding() {
  var current_bid = document.getElementById("current_bid").getAttribute("data-bid")
  var new_bid = document.getElementById("bid").value
  var starting_price = document.getElementById("current_bid").getAttribute("data-start-price")
  var user = document.getElementById("url").getAttribute("data-user")
  var url = document.getElementById("url").getAttribute("data-url")
  if (current_bid >= new_bid || starting_price > new_bid) {
    swal({
      title: "Your bid is not enough!",
      icon: "error",
    });
  }
  else {
    console.log(url);
    fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({"bid_amount": new_bid, "user": user })
    })
  swal({
      title: "Your have bidded successfully!",
      icon: "success",
  });
  document.getElementById("bid").value = ""
  document.getElementById("bid").placeholder = "Current bid: " + new_bid + "$"
  document.getElementById("bid-info").innerText = "Your bid is the highest one!"
  }
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
            value="+ '"' + comment_text + '"' + ">\
    <label for='floatingInputValue'>" + user + "</label>\
    </form>"
  var url = document.getElementById("comment-btn").getAttribute("data-url")
  fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ listing_pk: listing_pk, comment_text: comment_text })
  })

  comments.innerHTML += form
}