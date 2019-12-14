$(function() {
  // $(function() {
  //   $('#showCreateButton').bind('click', function() {
  //     $.getJSON('/',
  //       function(data) {
  //           console.log('showCreateButton', data)
  //           showCreate()
  //     });
  //     return false;
  //   });
  // });

  // function showViewAll(){
  //   document.getElementById('showCreateButton').style.display="block"
  //   document.getElementById('bookTable').style.display="block"
  //   document.getElementById('createUpdateForm').style.display="none"
  // }

  // function addBookToTable(book){
  //   console.log('book ', book.ID)
  //   var tableElement = document.getElementById('bookTable')
  //   var rowElement = tableElement.insertRow(-1)
  //   rowElement.setAttribute('ID', book.ID)
  //   var cell1 = rowElement.insertCell(0);
  //   cell1.innerHTML = book.ID
  //   var cell2 = rowElement.insertCell(1);
  //   cell2.innerHTML = book.Author
  //   var cell3 = rowElement.insertCell(2);
  //   cell3.innerHTML = book.Title
  //   var cell4 = rowElement.insertCell(3);
  //   cell4.innerHTML = book.DatePosted
  //   // cell5.innerHTML = '<button onclick="showUpdate(this)">Update</button>'
  //   // var cell6 = rowElement.insertCell(5);
  //   // cell6.innerHTML = '<button onclick=doDelete(this)>delete</button>'
  // }

  // $.ajax({
  //     url: '/api/books',
  //     method: "GET",
  //     success: function(data) {
  //         // console.log('get info');
  //         // console.log(typeof data);
  //         for (key in data){
  //             // console.log(key + data[key].Title)
  //             addBookToTable(data[key]);
  //         }
  //         // $('#info').html(JSON.stringify(data, null, '   '));
  //         // $('#description').html(data['description']);
  //     }
  // });

  // function createBookAjax(book){
  //     //var car = {"reg":"12 D 1234","make":"Fiat","model":"Punto","price":3000}
  //     console.log('createBookAjax', JSON.stringify(book));
  //     $.ajax({
  //         url: "/api/books",
  //         method:"POST",
  //         data : JSON.stringify(book),
  //         // dataType: "JSON",
  //         // contentType: "application/json; charset=utf-8",
  //         success: function(result){
  //             console.log('create book ', result);
  //             book.id = result.id
  //             addBookToTable(book)
  //             clearForm()
  //             showViewAll()   
  //         },
  //         error: function(xhr,status,error){
  //             console.log("error: "+status+" msg:"+error);
  //         }
  //     });
  // }

})