document.addEventListener('DOMContentLoaded', function() {
    
    const toastBox = document.getElementById('toast-box');
    
    // Defined messages with FontAwesome icons
    let successMsg = '<i class="fa-solid fa-circle-check"></i> Added to favorites';
    let errorMsg = '<i class="fa-solid fa-circle-xmark"></i> Removed from favorites';

    // --- Function to Create and Show Toast ---
    function showToast(msg, type) {
        let toast = document.createElement('div');
        toast.classList.add('toast');
        toast.classList.add(type); // Adds 'success' or 'error'
        toast.innerHTML = msg;
        toastBox.appendChild(toast);

        // Remove after 4 seconds (matches CSS animation)
        setTimeout(() => {
            toast.remove();
        }, 4000);
    }

    // --- Handle Heart Clicks on Home/Detail Pages ---
    const favoriteButtons = document.querySelectorAll('.favorite-icon');
    favoriteButtons.forEach(btn => {
        btn.addEventListener('click', function(event) {
            event.preventDefault(); 
            const icon = this.querySelector('i');
            if (icon.classList.contains('fas')) {
                icon.classList.remove('fas');
                icon.classList.add('far');
                showToast('<i class="fa-solid fa-circle-xmark"></i> Removed from favorites', 'error');
            } else {
                icon.classList.remove('far');
                icon.classList.add('fas');
                showToast('<i class="fa-solid fa-circle-check"></i> Added to favorites', 'success');
            }
        });
    });


    const removeButtons = document.querySelectorAll('.remove-btn');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', function(event) {
            // We DON'T use preventDefault() here because we want the form to submit 
            // and actually remove the item from the database.
            // However, the page will reload quickly. 
            
            // To see the animation properly, we can show it immediately:
            showToast('<i class="fa-solid fa-circle-xmark"></i> Removed from favorites', 'error');
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
  const shoppingListContainer = document.querySelector('.shopping-list-container');

  if (shoppingListContainer) {
    // Handle checkbox toggling
    shoppingListContainer.addEventListener('change', function (event) {
      if (event.target.matches('input[type="checkbox"]')) {
        const itemId = event.target.id.replace('item-', '');
        // You'll need to send an AJAX request to your Django view to update 'is_purchased'
        fetch(`/shopping-list/toggle/${itemId}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Get CSRF token for Django POST requests
            'Content-Type': 'application/json',
          },
          // body: JSON.stringify({ is_purchased: event.target.checked }) // If sending JSON
        })
          .then((response) => {
            if (!response.ok) {
              console.error('Failed to toggle item');
              // Revert checkbox state if update failed
              event.target.checked = !event.target.checked;
            }
          })
          .catch((error) => {
            console.error('Error:', error);
            event.target.checked = !event.target.checked;
          });
      }
    });

    // Handle delete item button
    shoppingListContainer.addEventListener('click', function (event) {
      if (event.target.closest('.delete-item')) {
        const deleteButton = event.target.closest('.delete-item');
        const itemId = deleteButton.dataset.itemId;
        if (confirm('Are you sure you want to delete this item?')) {
          fetch(`/shopping-list/delete/${itemId}/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': getCookie('csrftoken'),
            },
          })
            .then((response) => {
              if (response.ok) {
                deleteButton.closest('.list-item').remove();
                // Optionally, add logic to show empty list message if no items remain
              } else {
                console.error('Failed to delete item');
              }
            })
            .catch((error) => console.error('Error:', error));
        }
      }
    });

    // Handle add custom item
    const addCustomItemBtn = document.getElementById('add-custom-item-btn');
    const customItemInput = document.getElementById('custom-item-input');
    if (addCustomItemBtn && customItemInput) {
      addCustomItemBtn.addEventListener('click', function () {
        const itemName = customItemInput.value.trim();
        if (itemName) {
          fetch(`/shopping-list/add-custom/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': getCookie('csrftoken'),
              'Content-Type': 'application/x-www-form-urlencoded', // For form-encoded data
            },
            body: `item_name=${encodeURIComponent(itemName)}`,
          })
            .then((response) => response.json()) // Assuming your Django view returns JSON
            .then((data) => {
              if (data.success) {
                // You would typically re-render the list or add the item dynamically
                window.location.reload(); // Simple reload for now
                customItemInput.value = '';
              } else {
                console.error('Failed to add custom item:', data.error);
              }
            })
            .catch((error) => console.error('Error:', error));
        }
      });
    }

    // Handle clear list button
    const clearListBtn = document.querySelector('.clear-list-btn');
    if (clearListBtn) {
      clearListBtn.addEventListener('click', function () {
        if (confirm('Are you sure you want to clear your entire shopping list?')) {
          fetch(`/shopping-list/clear/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': getCookie('csrftoken'),
            },
          })
            .then((response) => {
              if (response.ok) {
                window.location.reload(); // Reload to show empty list
              } else {
                console.error('Failed to clear list');
              }
            })
            .catch((error) => console.error('Error:', error));
        }
      });
    }

    // Helper function to get CSRF token
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  }
});


document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    // Assuming you add a toggle button with the class 'menu-toggle' to your base.html
    const menuToggle = document.querySelector('.menu-toggle'); 
    
    if (menuToggle && navbar) {
        menuToggle.addEventListener('click', function() {
            navbar.classList.toggle('open');
        });
        
        // Optional: Close menu when a link is clicked
        const navLinks = navbar.querySelectorAll('nav a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    navbar.classList.remove('open');
                }
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const navbar = document.querySelector('.navbar');

    if (menuToggle && navbar) {
        menuToggle.addEventListener('click', function() {
            navbar.classList.toggle('active');
        });
    }
});