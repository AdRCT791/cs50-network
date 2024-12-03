
document.addEventListener('DOMContentLoaded', function() {
    
    function createEditForm (postText) {
        const form=document.createElement('form');
        form.method = 'post';

        const textArea = document.createElement('textarea');
        textArea.value = postText.trimStart();
        textArea.maxLength = 300;
        textArea.className = 'form-post-textarea';
        form.appendChild(textArea);

        const saveButton = document.createElement('button');
        saveButton.textContent = 'Save';
        saveButton.type = 'submit';
        form.appendChild(saveButton);

        const cancelButton = document.createElement('button');
        cancelButton.textContent = 'Cancel';
        cancelButton.type = 'button';
        cancelButton.className = 'cancel-edit';
        cancelButton.addEventListener('click', () => {
            form.remove();
        });
        form.appendChild(cancelButton);

        return form;
    }
    

    // Event Handler for edit post button
    document.getElementById('posts-container').addEventListener('click', (event) => {
        if (event.target.classList.contains('edit-post')) {

            const postContainer = event.target.closest('.post-container');
            const postBody = postContainer.querySelector('.post-body');

            const form = createEditForm(postBody.textContent);
            postBody.replaceWith(form);

            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const newText = form.querySelector('textarea').value;
                const updatedPostBody = document.createElement('div');

                if (newText === '') {
                    alert('Post content cannot be empty!');
                    return;
                }

                updatedPostBody.className = 'post-body';
                updatedPostBody.textContent = newText;
                form.replaceWith(updatedPostBody);
            });

            const cancelButton = form.querySelector('.cancel-edit');
            cancelButton.addEventListener('click', () => {
                form.replaceWith(postBody);
            })
        }
    })


    // Query all elements with the class 'like-button' on the page
    document.querySelectorAll('.like-button').forEach(button => {
        
        // Add a 'click' event listener to each 'like-button'
        button.addEventListener('click', async function() {
            // Retrieve the post ID from the 'data-post-id' attribute of the clicked button
            const postId = this.dataset.postId; 
            const HeartIcon = this.querySelector('.ph-heart');

             // Attempt to send a POST request to the server to toggle the like for the given post
            try {
                const response = await fetch(`/like/${postId}/`, {
                    method: 'POST'
                });

                // Check if the server response indicates success
                if (response.ok) {
                     // Parse the JSON response from the server
                    const data = await response.json();

                    // Locate the element displaying the like count for this post
                    const likeCountElement = document.querySelector(`#like-count-${postId}`);
                    
                    // Toggle the 'red' class on the heart icon to visually indicate the like state
                    HeartIcon.classList.toggle('red'); 
                    
                    // Update the like count displayed in the DOM with the value from the server
                    likeCountElement.innerHTML = data.likes_count;
                    
                } else {
                    console.error('Failed to toggle like');
                }

            } catch (error) {
                // Log any network or other errors that occur during the fetch call
                console.error('Error', error);
            } 
        });
    });

});
  
  