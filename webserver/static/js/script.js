document.addEventListener('DOMContentLoaded', () => {
  // Get all elements with class "del"
  const deleteElements = document.querySelectorAll('.del');

  // Iterate over each element and attach an event listener
  deleteElements.forEach(element => {
    element.addEventListener('click', () => {
      const id = element.id; // Get the ID attribute of the clicked element

      // Send a request to the Django backend
      fetch(`/delArrivEmp?id=${id}`)
        .then(response => response.json())
        .then(data => {
          // Handle the response
          if (data.success) {
            // Perform the desired action for a successful response
            console.log('Successful response received.');

            // Delete the row in which the button is located
            const row = element.closest('tr');
            row.style.display = 'none';

            // Optionally, you can add additional actions here
          } else {
            // Handle the case where the response is not successful
            console.error('Unsuccessful response received.');
            // Do something else here
          }
        })
        .catch(error => {
          // Handle any errors that occur during the request
          console.error('An error occurred:', error);
          // Do something else to handle the error
        });
    });
  });



  // Get all elements with class "del"
  const deleteuser = document.querySelectorAll('.usr');

  // Iterate over each element and attach an event listener
  deleteuser.forEach(element => {
    element.addEventListener('click', () => {
      const id = element.id; // Get the ID attribute of the clicked element

      // Send a request to the Django backend
      fetch(`/delUser?id=${id}`)
        .then(response => response.json())
        .then(data => {
          // Handle the response
          if (data.success) {
            // Perform the desired action for a successful response
            console.log('Successful response received.');

            // Delete the row in which the button is located
            const row = element.closest('tr');
            row.style.display = 'none';

            // Optionally, you can add additional actions here
          } else {
            // Handle the case where the response is not successful
            console.error('Unsuccessful response received.');
            // Do something else here
          }
        })
        .catch(error => {
          // Handle any errors that occur during the request
          console.error('An error occurred:', error);
          // Do something else to handle the error
        });
    });
  });
});