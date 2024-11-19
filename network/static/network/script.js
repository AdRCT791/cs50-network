


document.addEventListener('DOMContentLoaded', function() {

    const textInput = document.getElementById('post-input-text');
    const charCountDisplay = document.getElementById('char-count-display');

    // Character count post input
    textInput.addEventListener('input', ()=>{
        const charCount = textInput.value.length;
        charCountDisplay.innerHTML = 300 - charCount;
    })

    // Like Function
    const likeButton = document.getElementsByClassName('post-metrics');
    const likeCountDisplay = document.getElementsByClassName('like-count-display');
    
    console.log(likeButton);
    typeof (likeButton);

    for (let i = 0; i < likeButton.length; i++) {
        let counter = 0;
        likeButton[i].addEventListener('click', () => {
            counter++;
            likeCountDisplay[i].innerHTML = counter;
        })
    };
});
  
  