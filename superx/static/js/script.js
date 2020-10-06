// JavaScripts functions

// adding Items from "myTable" table to "mycart" table
// function addItem(product_id, product_name){
//   $.ajax({
//     url: "/addItem",
//     method: "POST",
//     data: {input: $("#myInput").val()},
//     success: function (res) {
//       $('#cartbody').html(decodeURI(res));
//     }
//   })
// }

// function that removes table row and if there are no items in cart - disabled 'comparebutton' button
function removeItem(product_id) {
  $('#' + product_id).remove();
  if ($('#cartbody tr').length === 0) {
    $("#comperbutton").attr('disabled', '');
  }
}

// live search
function search() {
      $.ajax({
        url: "/livesearch",
        method: "POST",
        data: {input: $("#myInput").val()},
        success: function (res) {
          $('#tbody').html(decodeURI(res));
        }
      })
}
