
document.addEventListener('DOMContentLoaded', function() {

    // POPOVER EVENT LISTENER
    document.addEventListener('popoverShown', () => {
        const textInput = document.getElementById('post-input-text');
        const charCountDisplay = document.getElementById('char-count-display');
        
        if(textInput && charCountDisplay) {
            textInput.addEventListener('input', () => {
                const charCount = textInput.value.length;
                charCountDisplay.innerHTML = 300 - charCount;
            });
        }
    });

    // EDIT POST
    const editButton = document.getElementById('edit-post');

    editButton.addEventListener('click', () => {
        console.log('This event listener is working');   
    })


    // // Like Function
    // const likeButton = document.getElementsByClassName('post-metrics');
    // const likeCountDisplay = document.getElementsByClassName('like-count-display');
    
    // console.log(likeButton);
    // typeof (likeButton);

    // for (let i = 0; i < likeButton.length; i++) {
    //     let counter = 0;
    //     likeButton[i].addEventListener('click', () => {
    //         counter++;
    //         likeCountDisplay[i].innerHTML = counter;
    //     })
    // };
});
  
  