// JavaScripts functions

// adding Items from "myTable" table to "mycart" table
function addItem(product_id, product_name){
  $.ajax({
    url: "/addItem",
    method: "POST",
    data: {id: product_id, name: product_name},
    success: function (res) {
      const tableBody = $('#cartbody');
      tableBody.append($(`<tr id="${product_id}">
          <td colspan="2">${product_id}</td>
          <td colspan="2">${product_name}</td>
          <td><button onclick="removeItem(${product_id})" type="button" class="btn btn-outline-danger">הסר מהעגלה</button></td>
          <td colspan="0"><input type="hidden" name="${product_id}"></td>
            </tr>`));
      $('#comperbutton').removeAttr('disabled');
    }
  })
}


// function that removes table row and if there are no items in cart - disabled 'comparebutton' button
function removeItem(product_id) {
  $.ajax({
    url: "/removeItem",
    method: "POST",
    data: {id: product_id},
    success: function (res) {
      $('#' + product_id).remove();
  if ($('#cartbody tr').length === 0) {
    $("#comperbutton").attr('disabled', '');
  }
}
})
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
