// JavaScripts functions

// Search function that show only matching elements from search box
function search() {
  // Declare variables
  var input, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  table = document.getElementById("tbody");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.indexOf(input.value) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

// adding Items from "myTable" table to "mycart" table
function addItem(product_id, product_name){
  console.log("someone click");
  const tableBody = $('#cartbody');
  tableBody.append($(`<tr id="${product_id}">
      <td scope="col" colspan="2">${product_id}</td>
      <td scope="col" colspan="2">${product_name}</td>
      <td> <button onclick="removeItem(${product_id})" type="button" class="btn btn-outline-danger">הסר מהעגלה</button> </td>
        </tr>`));
  $("#comperbutton").removeAttr('disabled');
}

// function that removes table row and if there are no items in cart - disabled 'comparebutton' button
function removeItem(product_id) {
  $('#' + product_id).remove();
  if ($('#cartbody tr').length === 0) {
    $("#comperbutton").attr('disabled', '');
  }
}